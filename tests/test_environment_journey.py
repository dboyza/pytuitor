from textual.widgets import Button, TextArea

from pytuitor.app import TutorApp
from pytuitor.curriculum import LESSONS
from pytuitor.lesson_screen import LessonScreen
from pytuitor.workspace import environment_python


async def test_create_environment_through_ui_with_symlinked_profile_and_run(tmp_path):
    target = tmp_path / "real-profile"
    target.mkdir()
    linked = tmp_path / "profile-link"
    linked.symlink_to(target, target_is_directory=True)
    app = TutorApp(linked)
    async with app.run_test(size=(80, 24)) as pilot:
        await app.push_screen(LessonScreen(LESSONS[0]))
        await pilot.pause()
        screen = app.screen
        screen.action_environment()
        await pilot.pause()
        assert await pilot.click("#create-environment")
        await app.workers.wait_for_complete()
        assert environment_python(screen.environment_path).is_file()
        assert not app.screen.query_one("#install-package", Button).disabled
        await pilot.press("escape")
        screen.query_one("#editor", TextArea).load_text("import sys\nprint(sys.prefix)\n")
        await pilot.pause()
        screen.action_run()
        await app.workers.wait_for_complete()
        assert str(screen.environment_path) in screen.transcript
        assert "Program finished" in screen.transcript
