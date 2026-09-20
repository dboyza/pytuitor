from textual.widgets import Select, TextArea

from pytuitor.app import TutorApp
from pytuitor.curriculum import BY_ID


async def fill_workspace(screen, pilot, files):
    for name, source in files.items():
        screen.query_one("#project-file", Select).value = name
        await pilot.pause()
        screen.query_one("#editor", TextArea).load_text(source)
        await pilot.pause()


async def test_project_build_and_repair_keep_course_progress(tmp_path):
    app = TutorApp(tmp_path)
    app.store.data["onboarded"] = True
    lesson = BY_ID["task-workspace"]
    async with app.run_test(size=(80, 24)) as pilot:
        app.screen.open_lesson(lesson)
        await pilot.pause()
        screen = app.screen
        await fill_workspace(screen, pilot, lesson.stage_contract(screen.stage).reference_files)
        await pilot.press("f5")
        await app.workers.wait_for_complete()
        assert screen.stage_passed("build")
        await pilot.press("ctrl+n")
        await pilot.pause()
        assert screen.stage == "repair"
        await fill_workspace(screen, pilot, lesson.stage_contract(screen.stage).reference_files)
        await pilot.press("f5")
        await app.workers.wait_for_complete()
        assert app.store.status(lesson) == "completed"
        next_course = app.store.next_lesson()
        await pilot.press("ctrl+b")
        await pilot.pause()
        assert not app.screen.query("#review, #study-notes")
        assert app.store.next_lesson() == next_course
        assert app.store.data["last_lesson"] == lesson.id
        assert "reviews" not in app.store.data
