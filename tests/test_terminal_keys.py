"""Exercise real terminal bytes, not Pilot's synthetic key events."""

import json
import os
import select
import struct
import subprocess
import sys
import time

import pytest

from pytuitor.state import Store

fcntl = pytest.importorskip("fcntl", reason="Unix PTY coverage; Windows uses ConPTY tests")
pty = pytest.importorskip("pty")
termios = pytest.importorskip("termios")


@pytest.mark.parametrize("size", [(80, 24), (140, 44)])
@pytest.mark.parametrize("delay_editor_focus", [False, True], ids=["normal", "delayed-focus"])
def test_ctrl_t_cycles_through_terminal_input(tmp_path, size, delay_editor_focus):
    store = Store(tmp_path / "profile")
    store.data["onboarded"] = True
    store.save()
    store.close()
    state = tmp_path / "terminal-state"
    release = tmp_path / "release-focus"
    script = tmp_path / "terminal_app.py"
    script.write_text("""
import json
import sys
from pathlib import Path
from pytuitor.app import TutorApp
from pytuitor.lesson_screen import LessonScreen
import pytuitor.app
import pytuitor.screens

class ObservedLessonScreen(LessonScreen):
    delayed_focus = None
    focus_delivered = False

    def on_descendant_focus(self, event):
        if sys.argv[4] == "True" and event.widget.id == "editor" and not self.focus_delivered:
            # Hold a genuine focus notification until the next raw terminal key
            # has moved focus, reproducing slow message delivery deterministically.
            self.delayed_focus = event
            event.prevent_default()

    def deliver_focus(self):
        if self.delayed_focus is not None and Path(sys.argv[3]).exists():
            event = self.delayed_focus
            self.delayed_focus = None
            super().on_descendant_focus(event)
            self.call_after_refresh(self.acknowledge_focus)

    def acknowledge_focus(self):
        self.focus_delivered = True

pytuitor.screens.LessonScreen = ObservedLessonScreen

class ObservedApp(TutorApp):
    CSS_PATH = Path(pytuitor.app.__file__).with_name("theme.tcss")

    def on_ready(self):
        self.set_interval(0.05, self.record_state)

    def record_state(self):
        screen = self.screen
        if isinstance(screen, ObservedLessonScreen):
            screen.deliver_focus()
        observation = {
            "pane": getattr(screen, "active_pane", "dashboard"),
            "focused": self.focused.id if self.focused else None,
            "pending": getattr(screen, "delayed_focus", None) is not None,
            "delivered": getattr(screen, "focus_delivered", False),
        }
        target = Path(sys.argv[2])
        temporary = target.with_suffix(".tmp")
        temporary.write_text(json.dumps(observation))
        temporary.replace(target)

ObservedApp(Path(sys.argv[1])).run()
""")
    master, slave = pty.openpty()
    width, height = size
    fcntl.ioctl(slave, termios.TIOCSWINSZ, struct.pack("HHHH", height, width, 0, 0))
    env = dict(os.environ, TERM="xterm-256color")
    process = subprocess.Popen(
        [
            sys.executable,
            str(script),
            str(tmp_path / "profile"),
            str(state),
            str(release),
            str(delay_editor_focus),
        ],
        stdin=slave,
        stdout=slave,
        stderr=slave,
        env=env,
    )
    os.close(slave)

    def wait_for(expected, **details):
        output = bytearray()
        observed = None
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            if select.select([master], [], [], 0.05)[0]:
                try:
                    output.extend(os.read(master, 65536))
                except OSError:
                    break
            if state.exists():
                observed = json.loads(state.read_text())
                if observed["pane"] == expected and all(
                    observed[key] == value for key, value in details.items()
                ):
                    return
        raise AssertionError(
            f"Terminal did not reach {expected} {details}: "
            f"last state={observed}; output={output[-2000:]!r}"
        )

    try:
        wait_for("dashboard")
        os.write(master, b"c")
        wait_for("lesson", focused="reading-panel")
        os.write(master, b"\x14")  # Ctrl+T's standard terminal byte.
        wait_for("editor", focused="editor", pending=delay_editor_focus)
        os.write(master, b"\x14")
        wait_for("console", focused="results-scroll")
        if delay_editor_focus:
            release.touch()
            wait_for("console", focused="results-scroll", delivered=True)
        os.write(master, b"\x14")
        wait_for("lesson", focused="reading-panel")
        os.write(master, b"\x1bOS")  # F4 through the xterm terminal protocol.
        wait_for("editor", focused="exercise-scroll")
        os.write(master, b"\x05")  # Ctrl+E opens the file explorer.
        wait_for("editor", focused="file-tree")
        os.write(master, b"\r")  # Enter opens the selected file in the editor.
        wait_for("editor", focused="editor")
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
