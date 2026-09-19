"""Run against an installed wheel with python -I, outside editable imports."""

import asyncio
import tempfile
from importlib.metadata import version
from importlib.resources import files
from pathlib import Path

from textual.widgets import TextArea

from pytuitor.app import TutorApp
from pytuitor.curriculum import CHAPTERS, LESSONS, SECTIONS, default_input
from pytuitor.runner import execute
from pytuitor.screens import LessonScreen


async def main():
    assert len(LESSONS) == 87
    assert sum(lesson.project for lesson in LESSONS) == 12
    assert len(CHAPTERS) == 21
    assert len(SECTIONS) == 5
    assert files("pytuitor").joinpath("theme.tcss").is_file()
    for lesson in LESSONS:
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
    print(
        f"Pytuitor {version('pytuitor')}: installed content and all "
        f"{len(LESSONS) * 2} Build and Repair reference programs passed."
    )


if __name__ == "__main__":
    asyncio.run(main())
