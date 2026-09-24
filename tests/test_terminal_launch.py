"""Real CLI launches emit at most one grow-only terminal request."""

import os
import re
import select
import signal
import struct
import subprocess
import sys
import time

import pytest

from pytuitor.state import Store

fcntl = pytest.importorskip("fcntl", reason="Resize-request coverage uses a Unix PTY")
pty = pytest.importorskip("pty")
termios = pytest.importorskip("termios")


@pytest.mark.parametrize(
    "size,program,arguments,expected",
    [
        ((80, 24), "Apple_Terminal", [], (120, 30)),
        ((140, 24), "Apple_Terminal", [], (140, 30)),
        ((80, 44), "iTerm.app", [], (120, 44)),
        ((120, 30), "Apple_Terminal", [], None),
        ((180, 49), "iTerm.app", [], None),
        ((80, 24), "Apple_Terminal", ["--no-resize"], None),
        ((80, 24), "vscode", [], None),
        ((80, 24), "Apple_Terminal", ["--help"], None),
        ((80, 24), "Apple_Terminal", ["--version"], None),
    ],
    ids=["small", "short", "narrow", "comfortable", "large", "opt-out", "host", "help", "version"],
)
def test_cli_requests_size_only_when_needed(tmp_path, size, program, arguments, expected):
    with_profile = Store(tmp_path / "profile")
    with_profile.data["onboarded"] = True
    with_profile.save()
    with_profile.close()
    master, slave = pty.openpty()
    fcntl.ioctl(slave, termios.TIOCSWINSZ, struct.pack("HHHH", size[1], size[0], 0, 0))
    env = dict(os.environ, TERM="xterm-256color", TERM_PROGRAM=program)
    for name in ("CI", "SSH_CONNECTION", "SSH_TTY", "TMUX", "STY"):
        env.pop(name, None)
    # These stale shell variables must not override the actual terminal dimensions.
    env.update(COLUMNS="999", LINES="999")
    process = subprocess.Popen(
        [sys.executable, "-m", "pytuitor", "--data-dir", str(tmp_path / "profile"), *arguments],
        stdin=slave,
        stdout=slave,
        stderr=slave,
        env=env,
    )
    os.close(slave)
    output = bytearray()
    resized = False
    quit_sent = False
    pattern = rb"\x1b\[8;(\d+);(\d+)t"
    try:
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline:
            if select.select([master], [], [], 0.05)[0]:
                try:
                    chunk = os.read(master, 65536)
                except OSError:
                    break
                if not chunk:
                    break
                output.extend(chunk)
            request = re.search(pattern, output)
            if request and not resized:
                rows, columns = map(int, request.groups())
                # Emulate a host accepting the request, including the real resize signal.
                fcntl.ioctl(master, termios.TIOCSWINSZ, struct.pack("HHHH", rows, columns, 0, 0))
                os.kill(process.pid, signal.SIGWINCH)
                resized = True
            if b"Learning" in output and not quit_sent:
                os.write(master, b"\x11")
                quit_sent = True
            if process.poll() is not None:
                break
        process.wait(timeout=2)
        assert process.returncode == 0, bytes(output[-2000:])
        requests = [(int(columns), int(rows)) for rows, columns in re.findall(pattern, output)]
        assert requests == ([expected] if expected else [])
        if not set(arguments) & {"--help", "--version"}:
            assert quit_sent, "The learner dashboard must launch successfully"
    finally:
        if process.poll() is None:
            process.kill()
            process.wait()
        os.close(master)
