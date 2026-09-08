"""Run against an installed wheel with python -I, outside editable imports."""

import asyncio
import tempfile
from importlib.metadata import version
from importlib.resources import files
from pathlib import Path

from textual.widgets import TextArea

from pytuitor.app import TutorApp
from pytuitor.curriculum import CHAPTERS, LESSONS, default_input
from pytuitor.runner import execute
from pytuitor.screens import Dashboard, LessonScreen


async def main():
    assert len(LESSONS) == 60
    assert sum(lesson.project for lesson in LESSONS) == 12
    assert len(CHAPTERS) == 12
    assert files("pytuitor").joinpath("theme.tcss").is_file()
    for lesson in LESSONS:
        assert lesson.body.strip()
        result = await execute(
            lesson, lesson.solution, default_input(lesson), files=lesson.solution_files
        )
        assert result.passed, (lesson.id, result.error, result.checks)
    with tempfile.TemporaryDirectory() as directory:
        app = TutorApp(Path(directory))
        async with app.run_test(size=(80, 24)) as pilot:
            await pilot.press("f5")
            await pilot.pause()
            assert isinstance(app.screen, Dashboard)
            await pilot.press("c")
            await pilot.pause()
            assert isinstance(app.screen, LessonScreen)
            screen = app.screen
            for stage in ("build", "repair"):
                screen.query_one("#editor", TextArea).load_text(screen.lesson.solution)
                await pilot.pause()
                await pilot.press("f5")
                await app.workers.wait_for_complete()
                assert screen.stage_passed(stage)
                if stage == "build":
                    await pilot.press("ctrl+n")
                    await pilot.pause()
            assert app.store.status(screen.lesson) == "completed"
    print(
        f"Pytuitor {version('pytuitor')}: installed content and all 60 reference programs passed."
    )


if __name__ == "__main__":
    asyncio.run(main())
