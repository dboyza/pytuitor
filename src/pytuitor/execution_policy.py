"""Shared subprocess boundaries, independent of the UI and third-party packages."""

import asyncio
import contextlib
import os
import signal

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
    if temporary:
        environment["TMPDIR"] = home
    return environment


async def terminate_group(process: asyncio.subprocess.Process) -> None:
    """Join the parent and kill descendants even if the parent already exited."""
    with contextlib.suppress(ProcessLookupError):
        os.killpg(process.pid, signal.SIGKILL)
    await process.wait()
