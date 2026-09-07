"""Standalone standard-library learner process, launched with Python isolated mode."""

import asyncio
import contextlib
import importlib
import io
import json
import os
import resource
import shutil
import sys
import traceback
from pathlib import Path


def session_check(factory, fail):
    events = []
    try:
        with factory(events) as active:
            if active is not events:
                return ["The context manager must yield events"]
            if fail:
                raise ValueError("Practice failure")
    except ValueError:
        if not fail:
            raise
    return events


def raises_value_error(fn, argument):
    try:
        fn(argument)
    except ValueError:
        return True
    return False


def mutation_check(test):
    namespace = test.__globals__
    original = namespace["parse_count"]
    mutants = (lambda _: 0, lambda _: 12, lambda text: abs(int(text)))
    try:
        for mutant in mutants:
            namespace["parse_count"] = mutant
            try:
                test()
            except AssertionError:
                continue
            return False
        return True
    finally:
        namespace["parse_count"] = original


def concurrency_check(fn):
    namespace = fn.__globals__
    original = namespace["double"]

    async def exercise():
        started = 0
        gate = asyncio.Event()

        async def probe(value):
            nonlocal started
            started += 1
            if started == 3:
                gate.set()
            await gate.wait()
            return value * 2

        namespace["double"] = probe
        try:
            return await asyncio.wait_for(fn([1, 2, 3]), 0.5) == [2, 4, 6]
        except TimeoutError:
            return False

    try:
        return asyncio.run(exercise())
    finally:
        namespace["double"] = original


def cli_check(fn, text):
    original = sys.stdin
    output = io.StringIO()
    try:
        sys.stdin = io.StringIO(text)
        with contextlib.redirect_stdout(output):
            fn()
        return json.loads(output.getvalue())
    finally:
        sys.stdin = original


class Tee:
    def __init__(self, target):
        self.target = target
        self.captured = ""

    def write(self, text):
        self.target.write(text)
        self.target.flush()
        self.captured = (self.captured + text)[:65536]
        return len(text)

    def flush(self):
        self.target.flush()


class KeyboardInput:
    """Signal actual stdin reads so time spent typing is not execution time."""

    def __init__(self, stream, waiting_path):
        self.stream = stream
        self.waiting_path = waiting_path

    def readline(self, size=-1):
        self.waiting_path.touch()
        try:
            return self.stream.readline(size)
        finally:
            self.waiting_path.unlink(missing_ok=True)

    def read(self, size=-1):
        self.waiting_path.touch()
        try:
            return self.stream.read(size)
        finally:
            self.waiting_path.unlink(missing_ok=True)

    def __iter__(self):
        return self

    def __next__(self):
        line = self.readline()
        if not line:
            raise StopIteration
        return line

    def isatty(self):
        return False


def main():
    resource.setrlimit(resource.RLIMIT_CPU, (4, 4))
    resource.setrlimit(resource.RLIMIT_FSIZE, (1024 * 1024, 1024 * 1024))
    if sys.platform == "linux":
        resource.setrlimit(resource.RLIMIT_AS, (512 * 1024 * 1024, 512 * 1024 * 1024))
    root = Path(sys.argv[1])
    request = json.loads((root / "request.json").read_text())
    result = {"error": "", "checks": []}

    workspace = root / "workspace"
    entrypoint = request["entrypoint"]
    initial_path = list(sys.path)
    initial_modules = set(sys.modules)

    def prepare():
        os.chdir(root)
        if workspace.exists():
            shutil.rmtree(workspace)
        workspace.mkdir()
        for name, source in request["files"].items():
            path = workspace / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(source, encoding="utf-8")
        for name in set(sys.modules) - initial_modules:
            del sys.modules[name]
        sys.path[:] = [str(workspace / Path(entrypoint).parent), str(workspace), *initial_path]
        sys.argv[:] = [entrypoint]
        importlib.invalidate_caches()
        os.chdir(workspace)

    def program():
        return compile((workspace / entrypoint).read_text(encoding="utf-8"), entrypoint, "exec")

    def describe_error(exc):
        frames = [
            f
            for f in traceback.extract_tb(exc.__traceback__)
            if f.filename in request["files"] or str(workspace) in f.filename
        ]
        locations = "".join(
            f"  {Path(f.filename).name}, line {f.lineno}, in {f.name}\n" for f in frames
        )
        message = locations + "".join(traceback.format_exception_only(exc))
        if isinstance(exc, EOFError):
            message += (
                "\nThe program expected another answer. Run again and type it in the console.\n"
            )
        return message

    def namespace():
        return {
            "__name__": "__main__",
            "__file__": str(workspace / entrypoint),
            "__session_check__": session_check,
            "__raises_value_error__": raises_value_error,
            "__mutation_check__": mutation_check,
            "__cli_check__": cli_check,
            "__concurrency_check__": concurrency_check,
        }

    if not request["checks"]:
        prepare()
        sys.stdin = (
            KeyboardInput(sys.stdin, root / "waiting-for-input")
            if request.get("interactive")
            else io.StringIO(request["stdin"])
        )
        try:
            with contextlib.redirect_stdout(Tee(sys.stdout)):
                exec(program(), namespace())
        except BaseException as exc:
            result["error"] = describe_error(exc)
    else:
        with (root / "checks.jsonl").open("w") as events:

            def emit(event):
                events.write(json.dumps(event) + "\n")
                events.flush()

            for index, check in enumerate(request["checks"], 1):
                supplied = check.get("stdin")
                supplied = request["stdin"] if supplied is None else supplied
                case = {
                    "number": index,
                    "label": check["label"],
                    "input": supplied,
                    "operation": check.get("description") or check["expression"],
                    "expected": repr(check["expected"]),
                    "expected_output": check.get("expected_output"),
                    "nudge": check["nudge"],
                    "status": "running",
                }
                emit(case)
                capture = Tee(sys.stdout)
                expected = check["expected"]
                prepare()
                scope = namespace()
                try:
                    sys.stdin = io.StringIO(supplied)
                    with contextlib.redirect_stdout(capture):
                        exec(program(), scope)
                        scope["__stdout__"] = capture.captured
                        if isinstance(expected, dict) and set(expected) == {"expr"}:
                            expected = eval(expected["expr"], scope)
                        actual = eval(check["expression"], scope)
                        actual = json.loads(json.dumps(actual))
                    case["passed"] = actual == expected
                    if check.get("expected_output") is not None:
                        case["passed"] &= capture.captured.rstrip().endswith(
                            check["expected_output"]
                        )
                    case["actual"] = repr(actual)[:1000]
                except BaseException as exc:
                    case["passed"] = False
                    case["actual"] = describe_error(exc)
                    # Preserve a top-level error for syntax and program startup failures.
                    if isinstance(exc, (SyntaxError, EOFError)):
                        result["error"] = case["actual"]
                case.update(
                    status="finished",
                    output=capture.captured[:65536],
                    expected=repr(expected)[:1000],
                )
                result["checks"].append(case)
                emit(case)
    (root / "result.json").write_text(json.dumps(result))


if __name__ == "__main__":
    main()
