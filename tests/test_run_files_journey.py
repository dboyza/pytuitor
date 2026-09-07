from textual.widgets import Button, TextArea

from pytuitor.app import TutorApp
from pytuitor.curriculum import LESSONS
from pytuitor.lesson_screen import LessonScreen


async def test_run_output_files_are_explicitly_previewed_saved_and_exported(tmp_path):
    app = TutorApp(tmp_path)
    async with app.run_test(size=(80, 24)) as pilot:
        await app.push_screen(LessonScreen(LESSONS[0]))
        await pilot.pause()
        screen = app.screen
        source = "from pathlib import Path\nPath('notes.txt').write_text('Hello, file!')\n"
        screen.query_one("#editor", TextArea).load_text(source)
        await pilot.pause()
        screen.action_run()
        await app.workers.wait_for_complete()
        assert "notes.txt" not in screen.project_files()
        assert screen.query_one("#run-files", Button).display
        screen.action_run_files()
        await pilot.pause()
        assert app.screen.query_one("#run-file-code", TextArea).text == "Hello, file!"
        assert app.screen.query_one("#run-file-code", TextArea).read_only
        await pilot.click("#keep-run-files")
        await pilot.pause()
        assert screen.project_files()["notes.txt"] == "Hello, file!"
        assert screen.project_files()["lesson.py"] == source
        exported = screen.export_code()
        assert (exported / "notes.txt").read_text() == "Hello, file!"
        assert len(list((tmp_path / "exports").iterdir())) == 2


async def test_run_files_do_not_overwrite_newer_user_edits(tmp_path):
    app = TutorApp(tmp_path)
    async with app.run_test() as pilot:
        await app.push_screen(LessonScreen(LESSONS[0]))
        await pilot.pause()
        screen = app.screen
        source = "from pathlib import Path\nPath('lesson.py').write_text('# generated')\n"
        screen.query_one("#editor", TextArea).load_text(source)
        await pilot.pause()
        screen.action_run()
        await app.workers.wait_for_complete()
        assert screen.run_files["lesson.py"] == "# generated"
        screen.query_one("#editor", TextArea).load_text("# new work")
        await pilot.pause()
        screen.keep_run_files(screen.run_files)
        assert screen.query_one("#editor", TextArea).text == "# new work"
        assert not (tmp_path / "exports").exists()
