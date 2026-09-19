from dataclasses import replace

import pytest
from textual.widgets import Select, TextArea

from pytuitor.app import TutorApp
from pytuitor.curriculum import LESSONS
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
        screen.query_one("#project-file", Select).value = "helpers.py"
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
