"""Shared subprocess boundaries, independent of the UI and third-party packages."""

import asyncio
import contextlib
import json
import os
import signal
from pathlib import Path

OUTPUT_BYTES = 64 * 1024
EXECUTION_SECONDS = 5.0
WORKER_LIMITS = {
    "cpu_seconds": 4,
    "file_bytes": 1024 * 1024,
    "memory_bytes": 512 * 1024 * 1024,
    "output_bytes": OUTPUT_BYTES,
}


def clean_environment(home: str, *, temporary: bool = False) -> dict[str, str]:
    """Do not forward credentials, Python overrides, or installer configuration."""
    environment = {
        "PATH": os.defpath,
        "HOME": home,
        "PYTHONIOENCODING": "utf-8",
        "PIP_CONFIG_FILE": os.devnull,
    }
    if os.name == "nt":
        for name in ("SystemRoot", "WINDIR", "COMSPEC", "PATHEXT"):
            if name in os.environ:
                environment[name] = os.environ[name]
        environment["USERPROFILE"] = home
        environment["TEMP"] = home
        environment["TMP"] = home
    if temporary:
        environment["TMPDIR"] = home
    return environment


async def terminate_group(process: asyncio.subprocess.Process) -> None:
    """Join the parent and kill descendants even if the parent already exited."""
    with contextlib.suppress(ProcessLookupError):
        if os.name == "nt":
            process.kill()  # Closing the launcher job kills its descendants too.
        else:
            os.killpg(process.pid, signal.SIGKILL)
    await process.wait()


async def start_process(*arguments: str, limits: dict | None = None, **options):
    """Start a process tree with cleanup installed before user code can run."""
    arguments = (arguments[0], "-X", "utf8", *arguments[1:])
    if os.name == "nt":
        arguments = (
            arguments[0],
            "-I",
            "-X",
            "utf8",
            str(Path(__file__).with_name("_windows.py")),
            json.dumps(limits or {}),
            *arguments,
        )
    return await asyncio.create_subprocess_exec(
        *arguments, start_new_session=os.name != "nt", **options
    )
