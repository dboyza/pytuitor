import pytest
from textual.widgets import OptionList, Select, SelectionList, Static

from pytuitor.app import TutorApp
from pytuitor.curriculum import track_chapters, track_lessons


@pytest.mark.parametrize("track", ["beginner", "experienced", "custom"])
async def test_dashboard_shows_only_the_saved_path(tmp_path, track):
    app = TutorApp(tmp_path)
    app.store.data.update(onboarded=True, track=track)
    async with app.run_test(size=(80, 24)):
        assert not app.screen.query(
            "#track-beginner, #track-experienced, #track-custom, #projects, #rail"
        )
        listing = app.screen.query_one("#lesson-list", OptionList)
        assert [listing.get_option_at_index(i).id for i in range(listing.option_count)] == [
            lesson.id
            for lesson in track_lessons(track)
            if lesson.chapter_id == track_chapters(track)[0].id
        ]


async def test_path_settings_are_explicit_and_progress_is_path_specific(tmp_path):
    app = TutorApp(tmp_path)
    app.store.data.update(onboarded=True, track="beginner")
    for lesson in track_lessons("experienced"):
        app.store.entry(lesson)["completed"] = True
    async with app.run_test(size=(80, 24)) as pilot:
        assert "0 of 33" in str(app.screen.query_one("#dashboard-summary", Static).content)
        await pilot.click("#preferences")
        app.screen.query_one("#path", Select).value = "experienced"
        await pilot.press("escape")
        assert app.store.data["track"] == "beginner"
        await pilot.click("#preferences")
        app.screen.query_one("#path", Select).value = "custom"
        app.screen.query_one("#onboarding-concepts", SelectionList).select("Values & output")
        await pilot.press("f5")
        assert app.store.data["track"] == "custom"
        assert app.screen.query_one("#lesson-list", OptionList).option_count == 6
        assert "30 of 63" in str(app.screen.query_one("#dashboard-summary", Static).content)
        await pilot.press("c")
        assert app.screen.lesson.id == "names-and-voices"


async def test_completed_path_keeps_lessons_and_settings_available(tmp_path):
    from textual.widgets import Button

    from pytuitor.screens import Dashboard

    app = TutorApp(tmp_path)
    app.store.data.update(onboarded=True, track="beginner")
    for lesson in track_lessons("beginner"):
        app.store.entry(lesson)["completed"] = True
    async with app.run_test(size=(80, 24)) as pilot:
        assert app.screen.query_one("#continue", Button).disabled
        assert "PATH COMPLETE" in str(app.screen.query_one("#continue-summary", Static).content)
        await pilot.press("c")
        assert isinstance(app.screen, Dashboard)
        await pilot.press("home", "enter")
        assert app.screen.lesson.id == "first-light"
        await pilot.press("ctrl+b", "p")
        assert app.screen.query("#path")


@pytest.mark.parametrize("size", [(80, 24), (140, 44)])
async def test_dashboard_centers_continue_and_omits_retired_features(tmp_path, size):
    app = TutorApp(tmp_path)
    app.store.data.update(onboarded=True, track="beginner")
    async with app.run_test(size=size) as pilot:
        await pilot.pause()
        assert not app.screen.query("#review, #study-notes")
        button = app.screen.query_one("#continue")
        rows = [strip.text.strip() for strip in button.render_lines(button.size.region)]
        occupied = [index for index, text in enumerate(rows) if text]
        assert occupied == [len(rows) // 2]
        assert len(rows) % 2 == 1
        await pilot.click("#continue")
        assert app.screen.lesson.id == "first-light"
