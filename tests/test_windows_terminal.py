"""Real Windows console input through PowerShell 5.1/7 and native ConPTY."""

import base64
import json
import os
import select
import shutil
import sys
import time
from pathlib import Path

import pytest

pytestmark = pytest.mark.skipif(os.name != "nt", reason="Requires native Windows ConPTY")


@pytest.mark.parametrize("shell", ["powershell.exe", "pwsh.exe"])
@pytest.mark.parametrize("size", [(80, 24), (140, 44)])
def test_powershell_learning_journey(tmp_path, shell, size):
    from winpty import PtyProcess

    from pytuitor.curriculum import LESSONS
    from pytuitor.state import Store

    executable = shutil.which(shell)
    assert executable, f"Install {shell} to exercise the supported PowerShell host"
    profile = tmp_path / "learner profile café"
    state = tmp_path / "observation.json"
    store = Store(profile)
    store.data["onboarded"] = True
    store.save()
    store.close()
    arguments = [
        sys.executable,
        str(Path(__file__).with_name("windows_terminal_probe.py")),
        str(profile),
        str(state),
    ]
    command = "& " + " ".join("'" + arg.replace("'", "''") + "'" for arg in arguments)
    command += "; exit $LASTEXITCODE"
    encoded = base64.b64encode(command.encode("utf-16-le")).decode("ascii")
    terminal = PtyProcess.spawn(
        [executable, "-NoLogo", "-NoProfile", "-EncodedCommand", encoded],
        dimensions=(size[1], size[0]),
        backend=0,
    )
    output = ""

    def drain():
        nonlocal output
        if select.select([terminal.fileobj], [], [], 0.05)[0]:
            try:
                output = (output + terminal.read(65536))[-12000:]
            except EOFError:
                pass

    def wait_for(**expected):
        observed = None
        deadline = time.monotonic() + 20
        while time.monotonic() < deadline:
            drain()
            try:
                observed = json.loads(state.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            if all(observed.get(key) == value for key, value in expected.items()):
                return observed
        raise AssertionError(f"Expected {expected}; got {observed}; terminal={output!r}")

    try:
        wait_for(pane="dashboard")
        terminal.write("c")
        wait_for(pane="lesson", focus="reading-panel")
        terminal.write("\x14")
        wait_for(pane="editor", focus="editor")
        solution = LESSONS[0].solution
        terminal.write("\x1b[200~" + solution + "\x1b[201~")
        wait_for(code=solution)
        terminal.write("\x1b[15~")  # F5 Check
        wait_for(passed=True)
        terminal.write("\x0e")  # Ctrl+N: move to Repair
        wait_for(stage="repair", passed=False)
        terminal.write("\x1bOS")  # F4 requirements
        wait_for(focus="exercise-scroll")
        terminal.write("\x14")
        wait_for(pane="console", focus="results-scroll")
        terminal.write("\x14")
        wait_for(pane="lesson", focus="reading-panel")
        terminal.write("\x14")
        wait_for(pane="editor", focus="editor")

        def replace_code(source):
            terminal.write("\x01")  # Ctrl+A
            terminal.write("\x1b[200~" + source + "\x1b[201~")
            wait_for(code=source)

        replace_code("print(input('Name: '))\n")
        terminal.write("\x12")  # Ctrl+R Run
        wait_for(waiting=True, focus="console-input")
        terminal.write("Zoë\r")
        observed = wait_for(running=False, waiting=False)
        assert "Zoë" in observed["transcript"]
        assert "Program finished" in observed["transcript"]
        terminal.write("\x14\x14")
        wait_for(pane="editor", focus="editor")
        replace_code("import sys\nprint(sys.stdin.read())\n")
        terminal.write("\x12")
        wait_for(waiting=True, focus="console-input")
        terminal.write("\x04")  # Ctrl+D is the tutor's explicit EOF on Windows too.
        observed = wait_for(running=False, waiting=False)
        assert "[end of input]" in observed["transcript"]
        assert "Program finished" in observed["transcript"]
        terminal.write("\x14\x14")
        wait_for(pane="editor", focus="editor")
        replace_code("while True:\n    pass\n")
        terminal.write("\x12")
        wait_for(running=True)
        terminal.write("\x1b[19~")  # F8 Stop
        wait_for(running=False)
        resized = (140, 44) if size == (80, 24) else (80, 24)
        terminal.setwinsize(resized[1], resized[0])
        wait_for(size=list(resized))
        terminal.write("\x11")
        deadline = time.monotonic() + 10
        while terminal.isalive() and time.monotonic() < deadline:
            drain()
        assert not terminal.isalive(), output
        assert terminal.exitstatus == 0, output
        restored = Store(profile)
        assert restored.entry(LESSONS[0])["code"] == solution
        assert restored.entry(LESSONS[0])["stage"] == "repair"
        restored.close()
    finally:
        artifacts = Path(".artifacts")
        artifacts.mkdir(exist_ok=True)
        (artifacts / f"windows-{shell}-{size[0]}.txt").write_text(output, encoding="utf-8")
        terminal.close(force=True)
