from copy import deepcopy

import pytest
from textual.containers import VerticalScroll
from textual.widgets import Markdown, Select

from pytuitor.app import TutorApp
from pytuitor.curriculum import track_chapters, track_lessons
from pytuitor.screens import Dashboard
from pytuitor.syllabus import Syllabus


def assert_path_content(screen, track):
    source = screen.query_one("#syllabus-content", Markdown).source
    for chapter in track_chapters(track):
        assert chapter.title in source
        assert chapter.outcome in source
    for lesson in track_lessons(track):
        assert lesson.title in source
        assert f"{lesson.minutes} min" in source
        for concept in lesson.concepts:
            assert concept in source
    if track != "custom":
        other = "experienced" if track == "beginner" else "beginner"
        for chapter in track_chapters(other):
            assert chapter.title not in source


@pytest.mark.parametrize("size", [(80, 24), (140, 44)])
async def test_syllabus_browsing_is_keyboard_accessible_and_preserves_progress(tmp_path, size):
    app = TutorApp(tmp_path)
    app.store.data.update(onboarded=True, track="beginner")
    lesson = track_lessons("beginner")[0]
    app.store.entry(lesson)["code"] = "print('my saved draft')"
    async with app.run_test(size=size) as pilot:
        chapter_picker = app.screen.query_one("#chapter-picker", Select)
        chapter_picker.value = track_chapters("beginner")[2].id
        await pilot.pause()
        before = deepcopy(app.store.data)
        await pilot.click("#syllabus")
        assert isinstance(app.screen, Syllabus)
        assert_path_content(app.screen, "beginner")
        picker = app.screen.query_one("#syllabus-path", Select)
        assert picker.value == "beginner"
        for control in ("#syllabus-path", "#syllabus-back"):
            region = app.screen.query_one(control).region
            assert region.width > 0 and region.height > 0
            assert region.x >= 0 and region.right <= size[0]
            assert region.y >= 0 and region.bottom <= size[1] - 1
        scroll = app.screen.query_one("#syllabus-scroll", VerticalScroll)
        assert app.focused is scroll
        assert scroll.max_scroll_y > 0
        assert scroll.max_scroll_x == 0
        await pilot.press("end")
        await pilot.pause()
        assert scroll.scroll_y == scroll.max_scroll_y
        picker.focus()
        await pilot.press("enter", "down", "enter")
        await pilot.pause()
        assert picker.value == "experienced"
        assert scroll.scroll_y == 0
        assert_path_content(app.screen, "experienced")
        await pilot.press("enter", "down", "enter")
        await pilot.pause()
        assert picker.value == "custom"
        assert_path_content(app.screen, "custom")
        assert app.store.data == before
        await pilot.press("escape")
        assert isinstance(app.screen, Dashboard)
        assert app.screen.query_one("#chapter-picker", Select).value == chapter_picker.value
        assert app.store.data == before
        await pilot.press("s")
        assert isinstance(app.screen, Syllabus)
        assert app.screen.query_one("#syllabus-path", Select).value == "beginner"
        await pilot.click("#syllabus-back")
        assert isinstance(app.screen, Dashboard)
        assert app.store.data == before


@pytest.mark.parametrize("track", ["experienced", "custom"])
async def test_syllabus_defaults_to_saved_path(tmp_path, track):
    app = TutorApp(tmp_path)
    app.store.data.update(onboarded=True, track=track)
    async with app.run_test(size=(80, 24)) as pilot:
        await pilot.press("s")
        assert isinstance(app.screen, Syllabus)
        assert app.screen.query_one("#syllabus-path", Select).value == track
        assert_path_content(app.screen, track)
