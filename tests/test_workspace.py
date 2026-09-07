import asyncio
import os
import sys

import pytest

from pytuitor import workspace
from pytuitor.workspace import (
    WorkspaceError,
    create_environment,
    environment_python,
    export_workspace,
    install_package,
    validate_files,
)


@pytest.mark.parametrize(
    "name",
    [
        "/tmp/a.py",
        "../a.py",
        "a/../b.py",
        "a//b.py",
        "./a.py",
        "a\\b.py",
        "C:a.py",
        "a\x00.py",
        "a/",
        ".git/config",
        ".venv/a.py",
        "a./b.py",
    ],
)
def test_rejects_unsafe_project_names(name):
    with pytest.raises(WorkspaceError):
        validate_files({name: "print('hello')"})


@pytest.mark.parametrize(
    "files", [{"A.py": "", "a.py": ""}, {"a": "", "a/b.py": ""}, {"é.py": "", "e\u0301.py": ""}]
)
def test_rejects_cross_platform_path_collisions(files):
    with pytest.raises(WorkspaceError):
        validate_files(files)


def test_bounds_use_utf8_bytes_and_total_workspace_size():
    with pytest.raises(WorkspaceError, match="file limit"):
        validate_files({"large.py": "🐍" * (workspace.MAX_FILE_BYTES // 4 + 1)})
    with pytest.raises(WorkspaceError, match="total size"):
        validate_files({f"{index}.py": "a" * workspace.MAX_FILE_BYTES for index in range(5)})
    with pytest.raises(WorkspaceError, match="between"):
        validate_files({f"{index}.py": "" for index in range(workspace.MAX_FILES + 1)})


def test_exports_nested_files_without_replacing_existing_content(tmp_path):
    files = {"main.py": "from helpers.maths import double\n", "helpers/maths.py": "🐍\n"}
    destination = export_workspace(tmp_path / "project", files)
    assert (destination / "helpers/maths.py").read_text() == "🐍\n"
    with pytest.raises(WorkspaceError, match="already exists"):
        export_workspace(destination, {"main.py": "overwritten"})
    assert (destination / "main.py").read_text() == files["main.py"]
    assert sorted(path.name for path in tmp_path.iterdir()) == ["project"]


def test_rejects_symlink_parent_and_destination(tmp_path):
    original = tmp_path / "original"
    original.mkdir()
    alias = tmp_path / "alias"
    alias.symlink_to(original, target_is_directory=True)
    for destination in (alias, alias / "export"):
        with pytest.raises(WorkspaceError, match="symbolic"):
            export_workspace(destination, {"main.py": ""})
    assert not list(original.iterdir())


async def test_creates_real_offline_environment_and_does_not_replace_it(tmp_path):
    path = tmp_path / "environment"
    python = await create_environment(path)
    assert python == environment_python(path)
    result = await workspace._run_command(
        str(python), "-I", "-c", "import sys; print(sys.prefix != sys.base_prefix)"
    )
    assert result == "True"
    with pytest.raises(WorkspaceError, match="already exists"):
        await create_environment(path)


@pytest.mark.parametrize("requirement", ["--help", "a b", "https://a/b.whl", "./a", "a>=1", "a;ls"])
async def test_install_rejects_options_paths_urls_and_shell_syntax(tmp_path, requirement):
    with pytest.raises(WorkspaceError, match="one package"):
        await install_package(tmp_path / "python", requirement)


async def test_install_uses_explicit_isolated_wheel_only_command(tmp_path, monkeypatch):
    python = tmp_path / "bin/python"
    python.parent.mkdir()
    python.touch()
    (tmp_path / "pyvenv.cfg").touch()
    commands = []

    async def run(*arguments):
        commands.append(arguments)
        return "installed"

    monkeypatch.setattr(workspace, "_run_command", run)
    assert await install_package(python, "rich==13.9.4") == "installed"
    command = commands[0]
    assert command[-1] == "rich==13.9.4"
    assert "--only-binary=:all:" in command
    assert "--isolated" in command
    assert "https://pypi.org/simple" in command


async def test_timeout_and_output_limit_are_reported():
    with pytest.raises(WorkspaceError, match="timed out"):
        await workspace._run_command(
            sys.executable, "-c", "import time; time.sleep(20)", timeout=0.1
        )
    with pytest.raises(WorkspaceError, match="too much output"):
        await workspace._run_command(sys.executable, "-c", "print('x' * 100000)")


async def test_cancellation_removes_partial_environment(tmp_path, monkeypatch):
    started = asyncio.Event()

    async def wait(*arguments):
        started.set()
        await asyncio.Future()

    monkeypatch.setattr(workspace, "_run_command", wait)
    destination = tmp_path / "environment"
    task = asyncio.create_task(create_environment(destination))
    await asyncio.wait_for(started.wait(), 2)
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    assert not destination.exists()


async def test_cancellation_kills_real_subprocess(tmp_path):
    pid_file = tmp_path / "pid"
    source = (
        "import os, pathlib, time; pathlib.Path(%r).write_text(str(os.getpid())); time.sleep(20)"
    )
    task = asyncio.create_task(workspace._run_command(sys.executable, "-c", source % str(pid_file)))
    async with asyncio.timeout(5):
        while not pid_file.exists():
            await asyncio.sleep(0.02)
    pid = int(pid_file.read_text())
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    with pytest.raises(ProcessLookupError):
        os.kill(pid, 0)
