from textual.widgets import TextArea

from pytuitor.app import TutorApp
from pytuitor.curriculum import BY_ID


async def test_onboarding_is_a_direct_choice(tmp_path):
    app = TutorApp(tmp_path)
    async with app.run_test(size=(120, 40)):
        assert not app.screen.query("#background, #goal, #diagnostic")
        assert app.screen.query("#path")


async def test_run_waits_for_keyboard_input(tmp_path):
    app = TutorApp(tmp_path)
    app.store.data["onboarded"] = True
    app.store.data["last_lesson"] = "names-and-voices"
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("c")
        await pilot.pause()
        app.screen.query_one("#editor", TextArea).load_text(BY_ID["names-and-voices"].solution)
        await pilot.press("ctrl+r")
        await pilot.pause(0.3)
        assert app.screen.running
        assert app.screen.query("#console-input")


async def test_third_lesson_uses_only_introduced_syntax(tmp_path):
    app = TutorApp(tmp_path)
    app.store.data["onboarded"] = True
    app.store.data["last_lesson"] = "choose-a-door"
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("c")
        await pilot.pause()
        assert "def " not in app.screen.query_one("#editor", TextArea).text
        assert "elif " in BY_ID["choose-a-door"].body
        assert not app.screen.query("#reading")
