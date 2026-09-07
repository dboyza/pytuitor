from dataclasses import replace

from textual.widgets import TextArea

from pytuitor.app import TutorApp
from pytuitor.curriculum import LESSONS
from pytuitor.lesson_screen import LessonScreen


async def test_changed_entrypoint_preserves_existing_files_and_legacy_draft(tmp_path):
    lesson = replace(
        LESSONS[0],
        id="workspace-upgrade-fixture",
        entrypoint="main.py",
        files=("main.py", "helpers.py"),
    )
    app = TutorApp(tmp_path)
    app.store.data["onboarded"] = True
    app.store.entry(lesson).update(
        code="print('my original program')",
        files={"lesson.py": "print('my original program')", "notes.txt": "Keep these notes"},
        revision=lesson.revision - 1,
    )
    async with app.run_test(size=(120, 40)) as pilot:
        app.push_screen(LessonScreen(lesson))
        await pilot.pause()
        assert app.screen.query_one("#editor", TextArea).text == "print('my original program')"
        files = app.store.entry(lesson)["files"]
        assert files == {
            "main.py": "print('my original program')",
            "lesson.py": "print('my original program')",
            "notes.txt": "Keep these notes",
            "helpers.py": "",
        }
        assert app.screen.query("#updated-notice")
