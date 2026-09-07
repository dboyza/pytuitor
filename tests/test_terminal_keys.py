"""Exercise real terminal bytes, not Pilot's synthetic key events."""

import os
import pty
import select
import subprocess
import sys
import time

from pytuitor.state import Store


def test_ctrl_t_cycles_through_terminal_input(tmp_path):
    store = Store(tmp_path / "profile")
    store.data["onboarded"] = True
    store.save()
    store.close()
    state = tmp_path / "terminal-state"
    script = tmp_path / "terminal_app.py"
    script.write_text("""
import sys
from pathlib import Path
from pytuitor.app import TutorApp
import pytuitor.app

class ObservedApp(TutorApp):
    CSS_PATH = Path(pytuitor.app.__file__).with_name("theme.tcss")

    def on_ready(self):
        self.set_interval(0.05, self.record_state)

    def record_state(self):
        pane = getattr(self.screen, "active_pane", "dashboard")
        Path(sys.argv[2]).write_text(pane)

ObservedApp(Path(sys.argv[1])).run()
""")
    master, slave = pty.openpty()
    env = dict(os.environ, TERM="xterm-256color")
    process = subprocess.Popen(
        [sys.executable, str(script), str(tmp_path / "profile"), str(state)],
        stdin=slave,
        stdout=slave,
        stderr=slave,
        env=env,
    )
    os.close(slave)

    def wait_for(expected):
        output = bytearray()
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            if select.select([master], [], [], 0.05)[0]:
                try:
                    output.extend(os.read(master, 65536))
                except OSError:
                    break
            if state.exists() and state.read_text() == expected:
                return
        raise AssertionError(f"Terminal did not reach {expected}: {output[-2000:]!r}")

    try:
        wait_for("dashboard")
        os.write(master, b"c")
        wait_for("lesson")
        for pane in ("editor", "console", "lesson"):
            os.write(master, b"\x14")  # Ctrl+T's standard terminal byte.
            wait_for(pane)
        os.write(master, b"\x11")  # Ctrl+Q.
        deadline = time.monotonic() + 5
        while process.poll() is None and time.monotonic() < deadline:
            if select.select([master], [], [], 0.05)[0]:
                try:
                    os.read(master, 65536)
                except OSError:
                    break
        process.wait(timeout=1)
        assert process.returncode == 0
    finally:
        if process.poll() is None:
            process.kill()
            process.wait()
        os.close(master)
