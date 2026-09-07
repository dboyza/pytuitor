"""Bounded local execution. Process isolation is not an OS security sandbox."""

import asyncio
import codecs
import json
import os
import signal
import stat
import sys
import tempfile
from collections import Counter
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from pathlib import Path

from pytuitor.models import Lesson

MAX_OUTPUT = 64 * 1024


class ConsoleSession:
    """One running program's stdin and streaming output callbacks."""

    def __init__(self, output: Callable[[str], None], waiting: Callable[[bool], None]):
        self.on_output = output
        self.on_waiting = waiting
        self.process: asyncio.subprocess.Process | None = None
        self.waiting = False
        self.eof = False

    def set_waiting(self, waiting: bool) -> None:
        if self.waiting != waiting:
            self.waiting = waiting
            self.on_waiting(waiting)

    def submit(self, value: str) -> bool:
        if not self.waiting or self.eof or not self.process or not self.process.stdin:
            return False
        try:
            self.process.stdin.write((value + "\n").encode())
        except (BrokenPipeError, ConnectionResetError):
            return False
        return True

    def end_input(self) -> None:
        if self.process and self.process.stdin and not self.eof:
            self.eof = True
            self.process.stdin.close()


@dataclass
class RunResult:
    output: str = ""
    error: str = ""
    checks: list[dict] = field(default_factory=list)
    files: dict[str, str] = field(default_factory=dict)
    files_notice: str = ""

    @property
    def passed(self) -> bool:
        return not self.error and bool(self.checks) and all(c["passed"] for c in self.checks)


def _collect_run_files(directory: Path) -> tuple[dict[str, str], str]:
    """Read a bounded text snapshot without following links or special files."""
    from pytuitor.workspace import MAX_FILE_BYTES, MAX_FILES, WorkspaceError, validate_files

    snapshot: dict[str, str] = {}
    skipped: Counter[str] = Counter()
    inspected = 0
    directory_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW

    def scan(descriptor: int, prefix: str = "", depth: int = 0) -> None:
        nonlocal inspected
        if depth > 16:
            skipped["deep folders"] += 1
            return
        with os.scandir(descriptor) as entries:
            for entry in entries:
                inspected += 1
                if inspected > 512:
                    skipped["scan limit"] += 1
                    return
                if entry.name == "__pycache__":
                    continue
                name = prefix + entry.name
                try:
                    if entry.is_symlink():
                        skipped["symbolic links"] += 1
                        continue
                    validate_files({name: ""})
                    if entry.is_dir(follow_symlinks=False):
                        child = os.open(entry.name, directory_flags, dir_fd=descriptor)
                        try:
                            scan(child, name + "/", depth + 1)
                        finally:
                            os.close(child)
                        continue
                    if len(snapshot) >= MAX_FILES:
                        skipped["file-count limit"] += 1
                        continue
                    child = os.open(
                        entry.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=descriptor
                    )
                    with os.fdopen(child, "rb") as stream:
                        information = os.fstat(stream.fileno())
                        if not stat.S_ISREG(information.st_mode):
                            skipped["non-text file types"] += 1
                            continue
                        if information.st_size > MAX_FILE_BYTES:
                            skipped["oversized files"] += 1
                            continue
                        content = stream.read(MAX_FILE_BYTES + 1)
                    if len(content) > MAX_FILE_BYTES:
                        skipped["oversized files"] += 1
                        continue
                    if b"\0" in content:
                        skipped["binary files"] += 1
                        continue
                    source = content.decode("utf-8")
                    validate_files({**snapshot, name: source})
                    snapshot[name] = source
                except UnicodeDecodeError:
                    skipped["binary files"] += 1
                except WorkspaceError:
                    skipped["invalid names or workspace limits"] += 1
                except OSError:
                    skipped["unreadable files or folders"] += 1

    try:
        descriptor = os.open(directory, directory_flags)
    except FileNotFoundError:
        return {}, ""
    except OSError:
        return {}, "Run files were unavailable or the workspace was replaced with a symbolic link."
    try:
        scan(descriptor)
    except OSError:
        skipped["unreadable folders"] += 1
    finally:
        os.close(descriptor)
    notice = "Some run files were omitted: " + ", ".join(sorted(skipped)) + "." if skipped else ""
    return snapshot, notice


async def execute(
    lesson: Lesson,
    source: str,
    stdin: str = "",
    *,
    check: bool = True,
    timeout: float = 5.0,
    console: ConsoleSession | None = None,
    on_check: Callable[[dict], None] | None = None,
    files: dict[str, str] | None = None,
    python: Path | None = None,
) -> RunResult:
    from pytuitor.workspace import validate_files

    sources = validate_files(files if files is not None else {lesson.entrypoint: source})
    if lesson.entrypoint not in sources:
        return RunResult(error=f"Missing entry point: {lesson.entrypoint}")
    with tempfile.TemporaryDirectory(prefix="pytuitor-run-") as folder:
        root = Path(folder)

        (root / "request.json").write_text(
            json.dumps(
                {
                    "checks": [asdict(c) for c in lesson.checks] if check else [],
                    "stdin": stdin,
                    "interactive": console is not None,
                    "files": sources,
                    "entrypoint": lesson.entrypoint,
                }
            )
        )
        output_path = root / "output.txt"
        result_path = root / "result.json"
        process = None
        reason = ""
        waiting_path = root / "waiting-for-input"
        offset = 0
        decoder = codecs.getincrementaldecoder("utf-8")("replace")
        check_offset = 0

        def report_checks() -> None:
            nonlocal check_offset
            path = root / "checks.jsonl"
            if on_check and path.exists():
                with path.open() as stream:
                    stream.seek(check_offset)
                    for line in stream:
                        if not line.endswith("\n"):
                            break
                        on_check(json.loads(line))
                        check_offset += len(line.encode())

        try:
            with output_path.open("wb") as output:
                process = await asyncio.create_subprocess_exec(
                    str(python or sys.executable),
                    "-I",
                    str(Path(__file__).with_name("_worker.py")),
                    str(root),
                    cwd=root,
                    stdin=asyncio.subprocess.PIPE if console else asyncio.subprocess.DEVNULL,
                    stdout=output,
                    stderr=output,
                    start_new_session=True,
                    env={
                        "PATH": os.defpath,
                        "HOME": folder,
                        "TMPDIR": folder,
                        "PYTHONIOENCODING": "utf-8",
                    },
                )
                if console:
                    console.process = process
                previous = asyncio.get_running_loop().time()
                active_seconds = 0.0
                was_waiting = False
                while process.returncode is None:
                    report_checks()
                    if output_path.stat().st_size > MAX_OUTPUT:
                        reason = "Output limit reached. Check for a loop that prints endlessly."
                        break
                    now = asyncio.get_running_loop().time()
                    waiting = bool(console and waiting_path.exists() and not console.eof)
                    if not waiting and not was_waiting:
                        active_seconds += now - previous
                    previous, was_waiting = now, waiting
                    if console:
                        with output_path.open("rb") as stream:
                            stream.seek(offset)
                            chunk = stream.read(MAX_OUTPUT - offset)
                        offset += len(chunk)
                        if chunk:
                            console.on_output(decoder.decode(chunk))
                        console.set_waiting(waiting)
                    if active_seconds > timeout:
                        reason = (
                            f"Stopped after {timeout:g} seconds of execution. "
                            "Check for a loop that never finishes."
                        )
                        break
                    await asyncio.sleep(0.025)
        finally:
            if process is not None:
                # Kill descendants too, including after a parent exits normally.
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                await process.wait()
            if console:
                console.process = None
                console.set_waiting(False)
        with output_path.open("rb") as stream:
            output_text = stream.read(MAX_OUTPUT).decode("utf-8", errors="replace")
        report_checks()
        if console:
            with output_path.open("rb") as stream:
                stream.seek(offset)
                tail = stream.read(MAX_OUTPUT - offset)
            remaining = decoder.decode(tail, final=True)
            if remaining:
                console.on_output(remaining)
        run_files, files_notice = _collect_run_files(root / "workspace") if not check else ({}, "")

        def finish(error: str = "", checks: list[dict] | None = None) -> RunResult:
            return RunResult(output_text, error, checks or [], run_files, files_notice)

        if reason:
            return finish(reason)
        if output_path.stat().st_size > MAX_OUTPUT:
            return finish("Output limit reached. Reduce repeated printing.")
        if not result_path.exists():
            return finish("Python exited before finishing. Check for exit() or a resource limit.")
        try:
            result = json.loads(result_path.read_text())
            return finish(result["error"], result["checks"])
        except (ValueError, KeyError):
            return finish("Python could not return its results. Try running again.")
