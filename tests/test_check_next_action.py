"""Check guidance stays honest when a learner edits a previously passing draft."""

from textual.widgets import Button, Static, TextArea

from pytuitor.app import TutorApp
from pytuitor.curriculum import LESSONS


async def test_edited_draft_does_not_reuse_the_success_message(tmp_path):
    app = TutorApp(tmp_path)
    app.store.data.update(onboarded=True, last_lesson=LESSONS[0].id)
    async with app.run_test(size=(80, 24)) as pilot:
        await pilot.press("c")
        screen = app.screen
        editor = screen.query_one("#editor", TextArea)
        editor.load_text(LESSONS[0].solution)
        await pilot.press("f5")
        await app.workers.wait_for_complete()
        assert "Build passed" in str(screen.query_one("#check-summary", Static).content)
        editor.load_text('print("changed")\n')
        await pilot.pause()
        assert screen.stage_passed("build")
        assert not screen.query_one("#stage-repair", Button).disabled
        assert "Check" in str(screen.query_one("#check-summary", Static).content)
        assert "Build passed" not in str(screen.query_one("#check-summary", Static).content)
