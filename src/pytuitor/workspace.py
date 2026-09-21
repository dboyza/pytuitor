"""Bounded project files and explicit, isolated environment operations.

These helpers protect tutor-owned paths from accidental traversal and replacement.
A virtual environment and a subprocess are not an operating-system security sandbox.
"""

from __future__ import annotations

import asyncio
import contextlib
import os
import re
import shutil
import sys
import tempfile
import unicodedata
from pathlib import Path, PurePosixPath

from pytuitor.execution_policy import (
    OUTPUT_BYTES,
    clean_environment,
    start_process,
    terminate_group,
)
from pytuitor.platform_files import is_link

MAX_FILES = 32
MAX_FILE_BYTES = 256 * 1024
MAX_WORKSPACE_BYTES = 1024 * 1024
MAX_COMMAND_OUTPUT = OUTPUT_BYTES
COMMAND_TIMEOUT = 180.0
_RESERVED = {".git", ".venv", "__pycache__"}
_REQUIREMENT = re.compile(
    r"[A-Za-z0-9](?:[A-Za-z0-9._-]*[A-Za-z0-9])?"
    r"(?:==[0-9]+(?:\.[0-9]+)*(?:(?:a|b|rc)[0-9]+)?"
    r"(?:\.post[0-9]+)?(?:\.dev[0-9]+)?"
    r"(?:\+[A-Za-z0-9]+(?:[._-][A-Za-z0-9]+)*)?)?"
)


class WorkspaceError(ValueError):
    """An operation could not safely complete; its message is learner-facing."""


def validate_files(files: dict[str, str]) -> dict[str, str]:
    """Return a copy after checking paths, collisions, and UTF-8 size limits."""
    if not isinstance(files, dict) or not files or len(files) > MAX_FILES:
        raise WorkspaceError(f"A workspace needs between 1 and {MAX_FILES} files.")
    result: dict[str, str] = {}
    normalized: set[str] = set()
    total = 0
    for name, source in files.items():
        if not isinstance(name, str) or not isinstance(source, str):
            raise WorkspaceError("File names and contents must be text.")
        try:
            name_size = len(name.encode("utf-8"))
        except UnicodeEncodeError as error:
            raise WorkspaceError("File names must be valid UTF-8 text.") from error
        parts = name.split("/")
        if (
            not name
            or name_size > 240
            or PurePosixPath(name).is_absolute()
            or "\\" in name
            or any(char in name for char in '<>:"|?*')
            or any(ord(char) < 32 or ord(char) == 127 for char in name)
            or any(part in {"", ".", ".."} or part.endswith((" ", ".")) for part in parts)
            or any(part.casefold() in _RESERVED for part in parts)
            or any(
                re.fullmatch(
                    r"(?i:con|prn|aux|nul|com[1-9¹²³]|lpt[1-9¹²³])", part.split(".")[0].rstrip()
                )
                for part in parts
            )
        ):
            raise WorkspaceError(f"Use a relative project file name without traversal: {name!r}.")
        folded = unicodedata.normalize("NFC", name).casefold()
        if folded in normalized:
            raise WorkspaceError("File names must also be unique on case-insensitive systems.")
        normalized.add(folded)
        try:
            size = len(source.encode("utf-8"))
        except UnicodeEncodeError as error:
            raise WorkspaceError("File contents must be valid UTF-8 text.") from error
        if size > MAX_FILE_BYTES:
            raise WorkspaceError(f"{name} exceeds the {MAX_FILE_BYTES // 1024} KiB file limit.")
        total += size
        result[name] = source
    for name in normalized:
        if any(parent.as_posix() in normalized for parent in PurePosixPath(name).parents):
            raise WorkspaceError("A project path cannot be both a file and a directory.")
    if total > MAX_WORKSPACE_BYTES:
        raise WorkspaceError("The workspace exceeds the 1 MiB total size limit.")
    return result


def _destination(path: Path) -> Path:
    path = Path(os.path.abspath(path.expanduser()))
    if any(is_link(parent) for parent in (path, *path.parents)):
        raise WorkspaceError("Choose a destination without symbolic-link directories.")
    if path.exists():
        raise WorkspaceError(f"Destination already exists: {path.name}.")
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        raise WorkspaceError(f"Could not create the parent directory: {error.strerror}.") from error
    return path


def export_workspace(destination: Path, files: dict[str, str]) -> Path:
    """Export all files atomically into a new directory, never an existing one."""
    checked = validate_files(files)
    path = _destination(destination)
    staging = Path(tempfile.mkdtemp(prefix=f".{path.name}-", dir=path.parent))
    reserved = False
    try:
        for name, source in checked.items():
            target = staging / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(source, encoding="utf-8")
        # Exclusive reservation prevents replacing a directory another export created.
        if os.name == "nt":
            # Windows rename fails if *any* destination exists, including an empty folder.
            staging.rename(path)
        else:
            path.mkdir(mode=0o700)
            reserved = True
            staging.replace(path)
        return path
    except OSError as error:
        if reserved:
            with contextlib.suppress(OSError):
                path.rmdir()
        raise WorkspaceError(f"Could not export the workspace: {error.strerror}.") from error
    finally:
        shutil.rmtree(staging, ignore_errors=True)


def environment_python(path: Path) -> Path:
    """Return the platform interpreter path; existence is checked by operations."""
    return Path(path) / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


async def _run_command(*arguments: str, timeout: float = COMMAND_TIMEOUT) -> str:
    environment = clean_environment(tempfile.gettempdir())
    process = await start_process(
        *arguments,
        stdin=asyncio.subprocess.DEVNULL,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
        env=environment,
    )
    output = bytearray()
    try:
        async with asyncio.timeout(timeout):
            assert process.stdout is not None
            while chunk := await process.stdout.read(8192):
                output.extend(chunk)
                if len(output) > MAX_COMMAND_OUTPUT:
                    raise WorkspaceError("The environment command produced too much output.")
            await process.wait()
        text = output.decode("utf-8", errors="replace").strip()
        if process.returncode:
            raise WorkspaceError(text or f"Environment command exited with {process.returncode}.")
        return text
    except TimeoutError as error:
        raise WorkspaceError("The environment command timed out. You can try again.") from error
    finally:
        await terminate_group(process)


async def create_environment(path: Path) -> Path:
    """Create an offline stdlib venv in a new directory and return its Python."""
    destination = _destination(path)
    try:
        destination.mkdir(mode=0o700)
    except OSError as error:
        raise WorkspaceError(f"Could not create environment: {error.strerror}.") from error
    try:
        await _run_command(sys.executable, "-I", "-m", "venv", str(destination))
        python = environment_python(destination)
        if not python.is_file():
            raise WorkspaceError("The environment did not contain a Python interpreter.")
        return python
    except BaseException:
        shutil.rmtree(destination, ignore_errors=True)
        raise


async def install_package(python: Path, requirement: str) -> str:
    """Explicitly install a named wheel from PyPI into a tutor-created venv.

    No URL, local path, index override, shell syntax, or source build is accepted.
    Installed third-party code must still be trusted by the learner.
    """
    if (
        not isinstance(requirement, str)
        or len(requirement) > 200
        or not _REQUIREMENT.fullmatch(requirement)
    ):
        raise WorkspaceError("Enter one package name, optionally pinned like rich==13.9.4.")
    python = Path(python).absolute()
    if not python.is_file() or not (python.parent.parent / "pyvenv.cfg").is_file():
        raise WorkspaceError("Create a project virtual environment before installing packages.")
    return await _run_command(
        str(python),
        "-I",
        "-m",
        "pip",
        "--isolated",
        "--disable-pip-version-check",
        "--no-input",
        "install",
        "--no-cache-dir",
        "--only-binary=:all:",
        "--index-url",
        "https://pypi.org/simple",
        requirement,
    )
