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


@pytest.mark.parametrize("size", [(80, 24), (140, 44)])
async def test_chapter_dropdown_identifies_sections_and_preserves_resume(tmp_path, size):
    from pytuitor.curriculum import SECTIONS

    app = TutorApp(tmp_path)
    app.store.data.update(onboarded=True, last_lesson="first-light")
    async with app.run_test(size=size) as pilot:
        picker = app.screen.query_one("#chapter-picker", Select)
        picker.focus()
        await pilot.press("enter")
        await pilot.pause()
        options = picker.query_one(OptionList)
        titles = {section.id: section.title for section in SECTIONS}
        chapter_columns = set()
        title_columns = set()
        for index, chapter in enumerate(CHAPTERS):
            label = str(options.get_option_at_index(index).prompt)
            assert label.split(" · ")[0].rstrip() == titles[chapter.section_id]
            assert chapter.title in label
            assert len(label) <= options.scrollable_content_region.width
            chapter_columns.add(label.index("Chapter"))
            title_columns.add(label.index(": ") + 2)
        assert len(chapter_columns) == len(title_columns) == 1
        await pilot.press("end", "enter")
        await pilot.pause()
        assert picker.value == CHAPTERS[-1].id
        assert app.store.data["last_lesson"] == "first-light"
