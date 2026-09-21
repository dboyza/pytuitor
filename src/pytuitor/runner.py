"""Bounded local execution. Process isolation is not an OS security sandbox."""

import asyncio
import codecs
import json
import sys
import tempfile
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from pathlib import Path

from pytuitor.execution_policy import (
    EXECUTION_SECONDS,
    OUTPUT_BYTES,
    WORKER_LIMITS,
    clean_environment,
    start_process,
)
from pytuitor.models import Lesson, StageContract
from pytuitor.progress_types import CheckEvent, check_event
from pytuitor.run_files import collect_run_files as _collect_run_files

MAX_OUTPUT = OUTPUT_BYTES


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
    checks: list[CheckEvent] = field(default_factory=list)
    files: dict[str, str] = field(default_factory=dict)
    files_notice: str = ""

    @property
    def passed(self) -> bool:
        return (
            not self.error
            and bool(self.checks)
            and all(c.get("passed", False) for c in self.checks)
        )


async def execute(
    lesson: Lesson,
    source: str,
    stdin: str | None = None,
    *,
    check: bool = True,
    timeout: float = EXECUTION_SECONDS,
    console: ConsoleSession | None = None,
    on_check: Callable[[CheckEvent], None] | None = None,
    files: dict[str, str] | None = None,
    python: Path | None = None,
    stage: StageContract | None = None,
) -> RunResult:
    from pytuitor.workspace import validate_files

    contract = stage or lesson.stage_contract("build")
    if stdin is None:
        stdin = contract.stdin
    sources = validate_files(files if files is not None else {lesson.entrypoint: source})
    if lesson.entrypoint not in sources:
        return RunResult(error=f"Missing entry point: {lesson.entrypoint}")
    with tempfile.TemporaryDirectory(prefix="pytuitor-run-") as folder:
        root = Path(folder)

        (root / "request.json").write_text(
            json.dumps(
                {
                    "limits": WORKER_LIMITS,
                    "checks": [asdict(c) for c in contract.checks] if check else [],
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
        tree = None
        reason = ""
        waiting_path = root / "waiting-for-input"
        offset = 0
        decoder = codecs.getincrementaldecoder("utf-8")("replace")
        check_offset = 0

        def report_checks() -> None:
            nonlocal check_offset
            path = root / "checks.jsonl"
            if on_check and path.exists():
                with path.open(encoding="utf-8", newline="") as stream:
                    stream.seek(check_offset)
                    for line in stream:
                        if not line.endswith("\n"):
                            break
                        check_offset += len(line.encode())
                        try:
                            on_check(check_event(json.loads(line)))
                        except (ValueError, TypeError):
                            continue

        try:
            with output_path.open("wb") as output:
                tree = await start_process(
                    str(python or sys.executable),
                    "-I",
                    str(Path(__file__).with_name("_worker.py")),
                    str(root),
                    cwd=root,
                    stdin=asyncio.subprocess.PIPE if console else asyncio.subprocess.DEVNULL,
                    stdout=output,
                    stderr=output,
                    limits=WORKER_LIMITS,
                    env=clean_environment(folder, temporary=True),
                )
                process = tree.process
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
            if tree is not None:
                await tree.close()
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

        def finish(error: str = "", checks: list[CheckEvent] | None = None) -> RunResult:
            return RunResult(output_text, error, checks or [], run_files, files_notice)

        if reason:
            return finish(reason)
        if output_path.stat().st_size > MAX_OUTPUT:
            return finish("Output limit reached. Reduce repeated printing.")
        if not result_path.exists():
            return finish("Python exited before finishing. Check for exit() or a resource limit.")
        try:
            result = json.loads(result_path.read_text())
            if not isinstance(result["error"], str) or not isinstance(result["checks"], list):
                raise ValueError("Invalid execution result")
            checks = [check_event(case) for case in result["checks"]]
            if any(case["status"] != "finished" for case in checks):
                raise ValueError("Incomplete final check result")
            return finish(result["error"], checks)
        except (ValueError, KeyError, TypeError):
            return finish("Python could not return its results. Try running again.")
