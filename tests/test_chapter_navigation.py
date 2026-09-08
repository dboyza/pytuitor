import pytest
from textual.widgets import OptionList, Select

from pytuitor.app import TutorApp
from pytuitor.curriculum import CHAPTERS, chapter_lessons


@pytest.mark.parametrize("size", [(80, 24), (140, 44)])
async def test_dashboard_browsing_does_not_change_active_chapter(tmp_path, size):
    app = TutorApp(tmp_path)
    active = chapter_lessons(CHAPTERS[2].id)
    app.store.data.update(onboarded=True, last_lesson=active[0].id)
    app.store.entry(active[0])["completed"] = True
    async with app.run_test(size=size) as pilot:
        picker = app.screen.query_one("#chapter-picker", Select)
        assert picker.value == CHAPTERS[2].id
        listing = app.screen.query_one("#lesson-list", OptionList)
        assert listing.get_option_at_index(0).id == active[0].id
        picker.value = CHAPTERS[-1].id
        await pilot.pause()
        assert listing.get_option_at_index(0).id == chapter_lessons(CHAPTERS[-1].id)[0].id
        assert app.store.data["last_lesson"] == active[0].id
        for control in ("#chapter-picker", "#syllabus", "#restart"):
            assert app.screen.query_one(control).region.bottom <= size[1] - 1
        await pilot.press("c")
        assert app.screen.lesson.id == active[1].id
