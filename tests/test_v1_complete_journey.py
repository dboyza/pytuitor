from textual.widgets import OptionList, Select, TextArea

from pytuitor.app import TutorApp
from pytuitor.curriculum import BY_ID
from pytuitor.lesson_screen import LessonScreen


async def fill_workspace(screen, pilot, files):
    for name, source in files.items():
        screen.query_one("#project-file", Select).value = name
        await pilot.pause()
        screen.query_one("#editor", TextArea).load_text(source)
        await pilot.pause()


async def test_project_build_repair_and_optional_review_keep_course_progress(tmp_path):
    app = TutorApp(tmp_path)
    app.store.data["onboarded"] = True
    lesson = BY_ID["task-workspace"]
    async with app.run_test(size=(80, 24)) as pilot:
        app.screen.open_lesson(lesson)
        await pilot.pause()
        screen = app.screen
        await fill_workspace(screen, pilot, lesson.solution_files)
        await pilot.press("f5")
        await app.workers.wait_for_complete()
        assert screen.stage_passed("build")
        await pilot.press("ctrl+n")
        await pilot.pause()
        assert screen.stage == "repair"
        await fill_workspace(screen, pilot, lesson.solution_files)
        await pilot.press("f5")
        await app.workers.wait_for_complete()
        assert app.store.status(lesson) == "completed"
        assert lesson.id in app.store.data["reviews"]
        next_course = app.store.next_lesson()
        await pilot.press("ctrl+b")
        await pilot.pause()
        app.screen.review()
        await pilot.pause()
        listing = app.screen.query_one("#review-list", OptionList)
        listing.highlighted = 0
        listing.focus()
        await pilot.press("enter")
        await pilot.pause()
        practice = app.screen
        assert isinstance(practice, LessonScreen)
        assert practice.lesson.review_of == lesson.id
        assert practice.query_one("#editor", TextArea).text == ""
        assert not practice.query_one("#stage-navigation").display
        practice.query_one("#editor", TextArea).load_text(practice.lesson.solution)
        await pilot.pause()
        await pilot.press("f5")
        await app.workers.wait_for_complete()
        assert practice.stage_passed("build")
        assert app.store.data["reviews"][lesson.id]["level"] == 1
        assert app.store.next_lesson() == next_course
        assert app.store.data["last_lesson"] == lesson.id
