from dataclasses import replace

import pytest
from textual.widgets import Static, TextArea

from pytuitor.app import TutorApp
from pytuitor.curriculum import LESSONS
from pytuitor.file_tree import FileTree
from pytuitor.lesson_screen import LessonScreen
from pytuitor.models import Check
from pytuitor.runner import execute


def project():
    return replace(
        LESSONS[0],
        id="workspace-fixture",
        entrypoint="main.py",
        files=("main.py", "helpers.py"),
        checks=(Check("Imports", "answer", 42, "Import the helper."),),
        solution="from helpers import double\nanswer = double(21)\n",
        solution_files={
            "main.py": "from helpers import double\nanswer = double(21)\n",
            "helpers.py": "def double(value):\n    return value * 2\n",
        },
        repair_files={
            "main.py": "from helpers import double\nanswer = double(21)\n",
            "helpers.py": "def double(value):\n    return value + 2\n",
        },
        build_stage=None,
        repair_stage=None,
    )


async def test_multi_file_stage_drafts_checks_and_export(tmp_path):
    lesson = project()
    app = TutorApp(tmp_path)
    app.store.data["onboarded"] = True
    async with app.run_test(size=(80, 24)) as pilot:
        await app.push_screen(LessonScreen(lesson))
        await pilot.pause()
        screen = app.screen
        editor = screen.query_one("#editor", TextArea)
        assert editor.text == ""
        editor.load_text(lesson.solution)
        await pilot.pause()
        tree = screen.query_one(FileTree)
        tree.select_node(tree.files["helpers.py"])
        await pilot.pause()
        assert editor.text == ""
        editor.load_text(lesson.solution_files["helpers.py"])
        await pilot.pause()
        screen.action_check()
        await app.workers.wait_for_complete()
        assert screen.stage_passed("build")
        assert screen.stage_entry()["files"] == lesson.solution_files
        exported = screen.export_code()
        assert (exported / "helpers.py").read_text() == lesson.solution_files["helpers.py"]
        screen.switch_stage("repair")
        await pilot.pause()
        assert screen.project_files() == lesson.repair_files
        screen.switch_stage("build")
        await pilot.pause()
        assert screen.project_files() == lesson.solution_files
        screen.save_draft()
    app.store.close()
    restored = TutorApp(tmp_path)
    assert restored.store.entry(lesson)["files"] == lesson.solution_files
    restored.store.close()


@pytest.mark.parametrize("size", [(80, 24), (140, 44)], ids=["compact", "wide"])
async def test_file_roles_explain_run_and_follow_stage_requirements(tmp_path, size):
    lesson = project()
    repair = lesson.stage_contract("repair")
    lesson = replace(
        lesson,
        repair_stage=replace(
            repair,
            files=(*repair.files, "notes.txt"),
            starter_files={**repair.starter_files, "notes.txt": "Required repair notes"},
        ),
    )
    app = TutorApp(tmp_path)
    app.store.data["onboarded"] = True
    app.store.entry(lesson)["files"] = {
        **lesson.solution_files,
        "main.py": lesson.solution + "print(answer)\n",
        "notes.txt": "My extra notes",
    }
    async with app.run_test(size=size) as pilot:
        await app.push_screen(LessonScreen(lesson))
        await pilot.pause()
        screen = app.screen
        tree = screen.query_one(FileTree)
        context = screen.query_one("#file-context", Static)
        assert tree.files["main.py"].label.plain == "▶ main.py"
        assert tree.files["helpers.py"].label.plain == "* helpers.py"
        assert tree.files["notes.txt"].label.plain == "  notes.txt"
        await pilot.press("ctrl+e", "up", "enter")
        assert screen.active_file == "helpers.py"
        assert str(context.content) == "Required file · Run starts in main.py"
        await pilot.click("#toggle-files")
        assert not screen.query_one("#file-sidebar").display
        assert context.display
        await pilot.press("ctrl+r")
        await app.workers.wait_for_complete()
        assert screen.transcript.startswith("42\n")
        assert context.display
        assert screen.active_file == "helpers.py"
        await pilot.press("f5")
        await app.workers.wait_for_complete()
        assert screen.stage_passed("build")
        await pilot.press("ctrl+e", "down", "down", "enter")
        assert screen.active_file == "notes.txt"
        assert str(context.content) == "Extra file · Run starts in main.py"
        await pilot.press("ctrl+n")
        await pilot.pause()
        assert screen.stage == "repair"
        assert tree.files["notes.txt"].label.plain == "* notes.txt"
        await pilot.press("ctrl+e", "down", "enter")
        assert str(context.content) == "Required file · Run starts in main.py"
        screen.action_remove_file()
        await pilot.pause()
        assert app.screen is screen
        assert screen.project_files()["notes.txt"] == "Required repair notes"
        assert screen.query_one("#editor").region.height >= 5
        assert screen.query_one("#execution-actions").region.bottom <= size[1] - 1
        await pilot.click("#stage-build")
        await pilot.press("ctrl+e", "down", "enter")
        assert str(context.content) == "Extra file · Run starts in main.py"
        assert screen.query_one(TextArea).text == "My extra notes"


async def test_checks_reset_imports_files_and_working_directory():
    lesson = replace(
        project(),
        checks=(
            Check("First clean run", "answer", 42, "Use a fresh file."),
            Check("Second clean run", "answer", 42, "Use a fresh file."),
        ),
    )
    sources = dict(lesson.solution_files)
    sources["main.py"] += (
        "from pathlib import Path\n"
        "assert not Path('leftover.txt').exists()\n"
        "Path('leftover.txt').write_text('created')\n"
        "import helpers\nhelpers.double = lambda value: 0\n"
    )
    result = await execute(lesson, sources["main.py"], files=sources)
    assert result.passed, result.checks


async def test_solution_is_explicit_and_never_replaces_draft(tmp_path):
    app = TutorApp(tmp_path)
    async with app.run_test() as pilot:
        await app.push_screen(LessonScreen(project()))
        await pilot.pause()
        screen = app.screen
        screen.query_one("#editor", TextArea).load_text("# My work")
        await pilot.pause()
        screen.action_solution()
        await pilot.pause()
        assert app.screen.query_one("#solution-code", TextArea).read_only
        await pilot.press("escape")
        assert screen.query_one("#editor", TextArea).text == "# My work"


@pytest.mark.parametrize("files", [{"../escape.py": ""}, {"/tmp/escape.py": ""}])
async def test_runner_rejects_escaping_paths(files):
    with pytest.raises(ValueError):
        await execute(project(), "", files=files)
