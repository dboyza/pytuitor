import pytest
from textual.widgets import Button, OptionList, Static

from pytuitor.app import TutorApp
from pytuitor.curriculum import CHAPTERS, LESSONS, chapter_lessons
from pytuitor.screens import Dashboard


@pytest.mark.parametrize("legacy_track", ["beginner", "experienced", "custom"])
async def test_dashboard_has_one_curriculum_regardless_of_legacy_path(tmp_path, legacy_track):
    app = TutorApp(tmp_path)
    app.store.data.update(onboarded=True, track=legacy_track)
    async with app.run_test(size=(80, 24)):
        assert not app.screen.query(
            "#track-beginner, #track-experienced, #track-custom, #projects, #rail"
        )
        assert str(app.screen.query_one("#path-title", Static).content) == "Learning"
        listing = app.screen.query_one("#lesson-list", OptionList)
        assert [listing.get_option_at_index(i).id for i in range(listing.option_count)] == [
            lesson.id for lesson in chapter_lessons(CHAPTERS[0].id)
        ]
        assert f"0 of {len(LESSONS)}" in str(
            app.screen.query_one("#dashboard-summary", Static).content
        )


async def test_known_topics_settings_remain_available(tmp_path):
    app = TutorApp(tmp_path)
    app.store.data.update(onboarded=True)
    async with app.run_test(size=(80, 24)) as pilot:
        assert str(app.screen.query_one("#preferences", Button).label) == "Known topics"
        await pilot.click("#preferences")
        assert not app.screen.query("#path")
        assert app.screen.query("#onboarding-concepts")
        await pilot.press("escape")
        assert isinstance(app.screen, Dashboard)


async def test_completed_curriculum_keeps_lessons_and_settings_available(tmp_path):
    app = TutorApp(tmp_path)
    app.store.data.update(onboarded=True)
    for lesson in LESSONS:
        app.store.entry(lesson)["completed"] = True
    async with app.run_test(size=(80, 24)) as pilot:
        assert app.screen.query_one("#continue", Button).disabled
        assert "CHOOSE YOUR NEXT CHAPTER" in str(
            app.screen.query_one("#continue-summary", Static).content
        )
        await pilot.press("c")
        assert isinstance(app.screen, Dashboard)
        await pilot.press("home", "enter")
        assert app.screen.lesson.id == "first-light"


@pytest.mark.parametrize("size", [(80, 24), (140, 44)])
async def test_dashboard_centers_continue_and_omits_retired_features(tmp_path, size):
    app = TutorApp(tmp_path)
    app.store.data.update(onboarded=True)
    async with app.run_test(size=size) as pilot:
        await pilot.pause()
        assert not app.screen.query("#review, #study-notes")
        button = app.screen.query_one("#continue")
        rows = [strip.text.strip() for strip in button.render_lines(button.size.region)]
        assert [index for index, text in enumerate(rows) if text] == [len(rows) // 2]
        assert len(rows) % 2 == 1
        await pilot.click("#continue")
        assert app.screen.lesson.id == "first-light"
