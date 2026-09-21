"""Behavioral coverage for Windows and Unix execution and persistence boundaries."""

import asyncio
import json
import os
import subprocess
import sys

import pytest

from pytuitor.curriculum import BY_ID, LESSONS
from pytuitor.runner import execute
from pytuitor.state import Store
from pytuitor.workspace import WorkspaceError, _run_command, export_workspace, validate_files


@pytest.mark.parametrize(
    "name",
    [
        "CON.py",
        "CONIN$",
        "CONOUT$.txt",
        "aux",
        "NUL.txt",
        "Com1/data.py",
        "lpt².log",
        "a?.py",
        "a*.py",
        'a".py',
        "a|b.py",
        "a<b.py",
    ],
)
def test_reject_windows_devices_and_invalid_characters_on_every_platform(name):
    with pytest.raises(WorkspaceError):
        validate_files({name: ""})


async def test_unicode_paths_input_output_and_generated_files(tmp_path):
    source = "from pathlib import Path\nname = input('Name: ')\nprint('Hello, ' + name)\n"
    source += "Path('résumé.txt').write_text(name + '\\n', encoding='utf-8')\n"
    result = await execute(LESSONS[0], source, "Zoë 🐍\n", check=False)
    assert not result.error
    assert result.output == "Name: Hello, Zoë 🐍\n"
    assert result.files["résumé.txt"] == "Zoë 🐍\n"
    destination = export_workspace(tmp_path / "project café", result.files)
    assert (destination / "résumé.txt").read_text(encoding="utf-8") == "Zoë 🐍\n"


@pytest.mark.parametrize("stage_name", ["build", "repair"])
async def test_archiver_checks_work_without_symlink_privileges(stage_name):
    lesson = BY_ID["notes-archiver"]
    stage = lesson.stage_contract(stage_name)
    files = dict(stage.reference_files)
    files[lesson.entrypoint] = (
        "from pathlib import Path\n"
        "def denied(*args, **kwargs):\n    raise PermissionError('No symlink privilege')\n"
        "Path.symlink_to = denied\n" + files[lesson.entrypoint]
    )
    result = await execute(lesson, files[lesson.entrypoint], files=files, stage=stage)
    assert result.passed, result
    # Find the author-defined selector file, without assuming its filename.
    selection = next(name for name, code in files.items() if "not path.is_symlink()" in code)
    files[selection] = files[selection].replace(" and not path.is_symlink()", "")
    result = await execute(lesson, files[lesson.entrypoint], files=files, stage=stage)
    assert not result.passed, "A selector accepting links must still fail without symlink privilege"


@pytest.mark.parametrize("cancel", [False, True], ids=["parent-exits", "cancelled"])
async def test_process_tree_stops_descendants(tmp_path, process_is_running, cancel):
    pid_file = tmp_path / "grandchild.pid"
    child = (
        "import os, pathlib, time; "
        f"pathlib.Path({str(pid_file)!r}).write_text(str(os.getpid())); time.sleep(60)"
    )
    wait_for_child = (
        f"from pathlib import Path\nwhile not Path({str(pid_file)!r}).exists(): time.sleep(.01)"
    )
    parent = (
        "import subprocess, sys, time; "
        f"subprocess.Popen([sys.executable, '-c', {child!r}], "
        "stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); "
        + ("time.sleep(60)" if cancel else f"exec({wait_for_child!r})")
    )
    task = asyncio.create_task(_run_command(sys.executable, "-c", parent))
    async with asyncio.timeout(15):
        while not pid_file.exists():
            await asyncio.sleep(0.02)
        if cancel:
            task.cancel()
            with pytest.raises(asyncio.CancelledError):
                await task
        else:
            await task
        pid = int(pid_file.read_text())
        while process_is_running(pid):
            await asyncio.sleep(0.02)


def test_profile_lock_is_released_after_process_crash(tmp_path):
    code = (
        "import os, sys; from pathlib import Path; from pytuitor.state import Store; "
        "store = Store(Path(sys.argv[1])); store.data['onboarded'] = True; "
        "store.save(); os._exit(7)"
    )
    result = subprocess.run([sys.executable, "-c", code, str(tmp_path)], timeout=15)
    assert result.returncode == 7
    store = Store(tmp_path)
    assert store.data["onboarded"]
    assert not store.durability_warning
    store.close()


@pytest.mark.skipif(os.name != "nt", reason="Native Windows write-through replacement")
def test_windows_failed_replace_preserves_profile(tmp_path, monkeypatch):
    import ctypes

    from pytuitor import _windows

    store = Store(tmp_path)
    store.save()
    before = store.path.read_bytes()

    def deny(*args):
        ctypes.set_last_error(5)
        return False

    monkeypatch.setattr(_windows, "_move", deny)
    store.data["onboarded"] = True
    with pytest.raises(OSError):
        store.save()
    assert store.path.read_bytes() == before
    assert not list(tmp_path.glob(".profile-*"))
    store.close()
    assert not json.loads(before)["onboarded"]


@pytest.mark.skipif(os.name != "nt", reason="Native Windows junctions")
def test_windows_junctions_are_not_export_destinations_or_run_files(tmp_path):
    from pytuitor.run_files import collect_run_files

    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "private.txt").write_text("private")
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    junction = workspace / "junction"
    subprocess.run(
        ["cmd.exe", "/d", "/c", "mklink", "/J", str(junction), str(outside)],
        check=True,
        capture_output=True,
    )
    try:
        with pytest.raises(WorkspaceError, match="symbolic"):
            export_workspace(junction / "export", {"main.py": ""})
        files, notice = collect_run_files(workspace)
        assert files == {}
        assert "symbolic links" in notice
    finally:
        junction.rmdir()


@pytest.mark.skipif(os.name != "nt", reason="Controller-owned Windows Job Objects")
async def test_windows_controller_crash_stops_its_worker(tmp_path, process_is_running):
    pid_file = tmp_path / "worker.pid"
    worker = (
        "import os, pathlib, time; "
        f"pathlib.Path({str(pid_file)!r}).write_text(str(os.getpid())); time.sleep(60)"
    )
    controller = (
        "import asyncio, os, sys\n"
        "from pathlib import Path\n"
        "from pytuitor.workspace import _run_command\n"
        "async def main():\n"
        f"    asyncio.create_task(_run_command(sys.executable, '-c', {worker!r}))\n"
        f"    while not Path({str(pid_file)!r}).exists():\n"
        "        await asyncio.sleep(.01)\n"
        "    os._exit(7)\n"
        "asyncio.run(main())\n"
    )
    process = await asyncio.create_subprocess_exec(sys.executable, "-c", controller)
    async with asyncio.timeout(15):
        await process.wait()
        assert process.returncode == 7
        pid = int(pid_file.read_text())
        while process_is_running(pid):
            await asyncio.sleep(0.02)
