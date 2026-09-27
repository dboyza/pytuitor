"""Run against an installed wheel with python -I, outside editable imports."""

import asyncio
import tempfile
from importlib.metadata import version
from importlib.resources import files
from pathlib import Path

from textual.widgets import TextArea

from pytuitor.app import TutorApp
from pytuitor.content.reviews import REVIEWS
from pytuitor.curriculum import CHAPTERS, LESSONS, SECTIONS, default_input
from pytuitor.project_catalog import MILESTONES
from pytuitor.project_workspace import ProjectWorkspace
from pytuitor.runner import execute
from pytuitor.screens import LessonScreen
from pytuitor.state import Store


async def main():
    assert len(LESSONS) == 87
    assert sum(lesson.project for lesson in LESSONS) == 12
    assert len(CHAPTERS) == 21
    assert len(SECTIONS) == 5
    assert files("pytuitor").joinpath("theme.tcss").is_file()
    units = (*LESSONS, *(item.lesson for item in MILESTONES))
    assert len(units) == 108
    for lesson in units:
        assert lesson.body.strip()
        for stage_name in ("build", "repair"):
            contract = lesson.stage_contract(stage_name)
            result = await execute(
                lesson,
                contract.reference_files[lesson.entrypoint],
                default_input(lesson, stage_name),
                files=contract.reference_files,
                stage=contract,
            )
            assert result.passed, (lesson.id, stage_name, result.error, result.checks)
    for tasks in REVIEWS.values():
        for task in tasks:
            if task.kind != "predict":
                result = await execute(task.lesson(), task.reference)
                assert result.passed, (task.id, result.error, result.checks)
    with tempfile.TemporaryDirectory() as directory:
        app = TutorApp(Path(directory))
        async with app.run_test(size=(80, 24)) as pilot:
            await pilot.press("f5")
            await pilot.pause()
            assert isinstance(app.screen, LessonScreen)
            screen = app.screen
            for stage in ("build", "repair"):
                contract = screen.lesson.stage_contract(stage)
                screen.query_one("#editor", TextArea).load_text(
                    contract.reference_files[screen.lesson.entrypoint]
                )
                await pilot.pause()
                await pilot.press("f5")
                await app.workers.wait_for_complete()
                assert screen.stage_passed(stage)
                if stage == "build":
                    await pilot.press("ctrl+n")
                    await pilot.pause()
            assert app.store.status(screen.lesson) == "completed"
            app.action_dashboard()
            app.open_activity(MILESTONES[0].lesson)
            await pilot.pause()
            screen = app.screen
            screen.query_one("#editor", TextArea).load_text(screen.lesson.solution)
            await pilot.press("f5")
            await app.workers.wait_for_complete()
            assert screen.stage_passed("build")
            checkpoint = ProjectWorkspace(app.store).data["checkpoints"][0]
            app.action_dashboard()
            app.open_activity(MILESTONES[1].lesson)
            await pilot.pause()
            assert app.store.entry(app.screen.lesson)["parent"] == checkpoint["id"]
        reopened = Store(Path(directory))
        workspace = ProjectWorkspace(reopened)
        assert workspace.read_checkpoint(checkpoint["id"])["files"]["game.py"]
        destination = workspace.export_checkpoint(checkpoint["id"])
        assert (destination / "game.py").is_file()
        reopened.close()
    print(
        f"Pytuitor {version('pytuitor')}: installed content and all "
        f"{len(units) * 2} stage references and 42 review references passed; "
        "game continuation, reopen, and export passed."
    )


if __name__ == "__main__":
    asyncio.run(main())
