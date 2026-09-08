"""Direct entry and recoverable save errors at the welcome/preferences boundary."""

import pytest
from textual.widgets import SelectionList

from pytuitor.app import TutorApp
from pytuitor.curriculum import LESSONS
from pytuitor.setup import Onboarding


@pytest.mark.parametrize("button", ["#begin", "#browse-syllabus"])
async def test_failed_welcome_save_stays_on_welcome(tmp_path, monkeypatch, button):
    app = TutorApp(tmp_path)
    async with app.run_test(size=(80, 24)) as pilot:
        monkeypatch.setattr(app, "persist", lambda: False)
        await pilot.click(button)
        await pilot.pause()
        assert isinstance(app.screen, Onboarding)
        assert not app.store.data["onboarded"]
        assert app.store.data["last_lesson"] is None


@pytest.mark.parametrize("size", [(80, 24), (140, 44)])
async def test_known_topics_controls_fit_and_failed_save_keeps_previous_choices(
    tmp_path, monkeypatch, size
):
    app = TutorApp(tmp_path)
    app.store.data["onboarded"] = True
    async with app.run_test(size=size) as pilot:
        await pilot.press("p")
        await pilot.pause()
        for selector in ("#begin", "#cancel-preferences"):
            assert app.screen.query_one(selector).region.bottom < size[1]
        app.screen.query_one("#onboarding-concepts", SelectionList).select(LESSONS[0].concepts[0])
        monkeypatch.setattr(app, "persist", lambda: False)
        await pilot.press("f5")
        await pilot.pause()
        assert isinstance(app.screen, Onboarding)
        assert app.store.data["familiar"] == []
        assert app.screen.query_one("#onboarding-concepts", SelectionList).selected
