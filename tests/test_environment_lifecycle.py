import asyncio

from textual.widgets import Button

from pytuitor.app import TutorApp
from pytuitor.learning_tools import EnvironmentDialog
from pytuitor.screens import Dashboard


async def test_leaving_busy_environment_dialog_cancels_operation(tmp_path, monkeypatch):
    started = asyncio.Event()
    cancelled = asyncio.Event()

    async def wait_for_environment(path):
        started.set()
        try:
            await asyncio.Future()
        finally:
            cancelled.set()

    monkeypatch.setattr("pytuitor.learning_tools.create_environment", wait_for_environment)
    app = TutorApp(tmp_path)
    app.store.data["onboarded"] = True
    async with app.run_test(size=(80, 24)) as pilot:
        app.push_screen(EnvironmentDialog(tmp_path / "environment"))
        await pilot.pause()
        button = app.screen.query_one("#create-environment", Button)
        button.scroll_visible(animate=False)
        await pilot.pause()
        await pilot.click("#create-environment")
        await asyncio.wait_for(started.wait(), 2)
        await pilot.press("ctrl+b")
        await asyncio.wait_for(cancelled.wait(), 2)
        await pilot.pause()
        assert isinstance(app.screen, Dashboard)
