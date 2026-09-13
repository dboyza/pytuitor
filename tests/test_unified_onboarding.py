"""Direct entry and recoverable save errors at the welcome/preferences boundary."""

import pytest
from textual.widgets import SelectionList

from pytuitor.app import TutorApp
from pytuitor.curriculum import LESSONS
from pytuitor.lesson_screen import LessonScreen
from pytuitor.screens import Dashboard
from pytuitor.setup import Onboarding
from pytuitor.syllabus import Syllabus


@pytest.mark.parametrize("size", [(80, 24), (140, 44)])
@pytest.mark.parametrize(
    ("button", "destination"), [("#begin", LessonScreen), ("#browse-syllabus", Syllabus)]
)
async def test_welcome_renders_destination_without_flashing_dashboard(
    tmp_path, monkeypatch, size, button, destination
):
    app = TutorApp(tmp_path)
    frames = []
    display = app._display

    def record_display(screen, renderable):
        # Observe every repaint, including intermediate frames Pilot.pause would miss.
        if renderable is not None and not app._batch_count:
            frames.append(type(screen))
        return display(screen, renderable)

    monkeypatch.setattr(app, "_display", record_display)
    async with app.run_test(size=size) as pilot:
        assert isinstance(app.screen, Onboarding)
        frames.clear()
        await pilot.click(button)
        await pilot.pause()
        assert isinstance(app.screen, destination)
        assert destination in frames
        assert Dashboard not in frames
        assert app.store.data["onboarded"]
        assert app.store.data["last_lesson"] == (
            LESSONS[0].id if destination is LessonScreen else None
        )

        # The dashboard remains available behind the destination, not onboarding.
        await pilot.press("escape" if destination is Syllabus else "ctrl+b")
        await pilot.pause()
        assert isinstance(app.screen, Dashboard)
        assert not any(isinstance(screen, Onboarding) for screen in app.screen_stack)
        await pilot.click("#syllabus")
        assert isinstance(app.screen, Syllabus)
        await pilot.press("ctrl+b")
        assert isinstance(app.screen, Dashboard)


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
