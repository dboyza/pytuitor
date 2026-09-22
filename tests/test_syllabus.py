from copy import deepcopy

import pytest
from textual.containers import VerticalScroll
from textual.widgets import Button, Collapsible, Select, Static

from pytuitor.app import TutorApp
from pytuitor.curriculum import CHAPTERS, LESSONS, SECTIONS, chapter_lessons
from pytuitor.screens import Dashboard
from pytuitor.syllabus import Syllabus


@pytest.mark.parametrize("size", [(80, 24), (140, 44)])
async def test_syllabus_browsing_is_keyboard_accessible_and_preserves_progress(tmp_path, size):
    app = TutorApp(tmp_path)
    app.store.data.update(onboarded=True)
    app.store.entry(LESSONS[0])["code"] = "print('my saved draft')"
    async with app.run_test(size=size) as pilot:
        picker = app.screen.query_one("#chapter-picker", Select)
        picker.value = CHAPTERS[2].id
        await pilot.pause()
        before = deepcopy(app.store.data)
        await pilot.click("#syllabus")
        assert isinstance(app.screen, Syllabus)
        assert not app.screen.query("#syllabus-path")
        source = "\n".join(
            str(item.content) for item in app.screen.query("#syllabus-content Static")
        )
        chapters = list(app.screen.query(Collapsible))
        assert len(chapters) == len(CHAPTERS)
        assert all(chapter.collapsed for chapter in chapters)
        for section in SECTIONS:
            assert section.title in source
        for lesson in LESSONS:
            assert lesson.title in source
        first = chapters[0]
        first.query_one("CollapsibleTitle").focus()
        await pilot.press("enter")
        await pilot.pause()
        assert not first.collapsed
        assert first.query_one(".syllabus-lesson", Static).region.height >= 3
        await pilot.press("enter")
        await pilot.pause()
        assert first.collapsed
        scroll = app.screen.query_one("#syllabus-scroll", VerticalScroll)
        scroll.focus()
        await pilot.press("end")
        await pilot.wait_for_scheduled_animations()
        assert scroll.scroll_y == scroll.max_scroll_y
        assert scroll.max_scroll_x == 0
        assert app.store.data == before
        await pilot.press("escape")
        assert isinstance(app.screen, Dashboard)
        assert app.screen.query_one("#chapter-picker", Select).value == CHAPTERS[2].id
        assert app.store.data == before


@pytest.mark.parametrize("completed", [False, True])
async def test_start_chapter_opens_first_unfinished_or_revisits_completed(tmp_path, completed):
    app = TutorApp(tmp_path)
    app.store.data.update(onboarded=True)
    chapter = CHAPTERS[-1]
    units = chapter_lessons(chapter.id)
    for lesson in units if completed else units[:1]:
        app.store.entry(lesson)["completed"] = True
    async with app.run_test(size=(80, 24)) as pilot:
        await pilot.press("s")
        detail = app.screen.query_one(f"#syllabus-{chapter.id}", Collapsible)
        detail.collapsed = False
        button = detail.query_one(".start-chapter", Button)
        button.focus()
        await pilot.pause()
        await pilot.press("enter")
        await pilot.pause()
        expected = units[0] if completed else units[1]
        assert app.screen.lesson.id == expected.id
        assert app.store.data["last_lesson"] == expected.id


async def test_opened_syllabus_chapter_becomes_dashboard_selection(tmp_path):
    app = TutorApp(tmp_path)
    app.store.data.update(onboarded=True)
    async with app.run_test(size=(80, 24)) as pilot:
        await pilot.press("s")
        chapter = CHAPTERS[-1]
        detail = app.screen.query_one(f"#syllabus-{chapter.id}", Collapsible)
        detail.collapsed = False
        detail.query_one(".start-chapter", Button).focus()
        await pilot.pause()
        await pilot.press("enter", "ctrl+b")
        await pilot.pause()
        assert isinstance(app.screen, Dashboard)
        assert app.screen.query_one("#chapter-picker", Select).value == chapter.id


async def test_failed_save_does_not_change_active_chapter(tmp_path, monkeypatch):
    app = TutorApp(tmp_path)
    app.store.data.update(onboarded=True, last_lesson=LESSONS[0].id)
    async with app.run_test(size=(80, 24)) as pilot:
        await pilot.press("s")
        chapter = CHAPTERS[-1]
        detail = app.screen.query_one(f"#syllabus-{chapter.id}", Collapsible)
        detail.collapsed = False
        detail.query_one(".start-chapter", Button).focus()
        await pilot.pause()
        monkeypatch.setattr(app, "persist", lambda: False)
        await pilot.press("enter")
        assert isinstance(app.screen, Syllabus)
        assert app.store.data["last_lesson"] == LESSONS[0].id


async def test_continue_chapter_resumes_current_draft_before_earlier_lessons(tmp_path):
    app = TutorApp(tmp_path)
    chapter = CHAPTERS[0]
    active = chapter_lessons(chapter.id)[2]
    app.store.data.update(onboarded=True, last_lesson=active.id)
    app.store.entry(active)["code"] = "print('saved draft')"
    async with app.run_test(size=(80, 24)) as pilot:
        await pilot.press("s")
        detail = app.screen.query_one(f"#syllabus-{chapter.id}", Collapsible)
        detail.collapsed = False
        button = detail.query_one(".start-chapter", Button)
        assert str(button.label) == "Continue chapter"
        button.focus()
        await pilot.pause()
        await pilot.press("enter")
        assert app.screen.lesson.id == active.id
