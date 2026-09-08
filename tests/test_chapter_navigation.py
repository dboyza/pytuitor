from dataclasses import replace

import pytest
from textual.widgets import OptionList, Select, Static

from pytuitor import curriculum, screens
from pytuitor.app import TutorApp
from pytuitor.models import Chapter


@pytest.fixture
def compact_course(monkeypatch):
    chapters = tuple(
        Chapter(
            f"{track}-{number}", track, f"{track.title()} chapter {number}", "Build useful tools."
        )
        for track in ("beginner", "experienced")
        for number in (1, 2)
    )
    base = curriculum.LESSONS[0]
    lessons = tuple(
        replace(
            base,
            id=f"{chapter.id}-{number}",
            title=f"Lesson {chapter.id}-{number}",
            track=chapter.track,
            chapter_id=chapter.id,
            project=number == 5,
            prerequisites=(),
        )
        for chapter in chapters
        for number in range(1, 6)
    )
    catalog = {lesson.id: lesson for lesson in lessons}
    monkeypatch.setattr(curriculum, "LESSONS", lessons)
    monkeypatch.setattr(curriculum, "CHAPTERS", chapters)
    monkeypatch.setattr(curriculum, "BY_ID", catalog)
    monkeypatch.setattr(screens, "BY_ID", catalog)
    return chapters, lessons


@pytest.mark.parametrize("size", [(80, 24), (140, 44)])
async def test_dashboard_browses_one_chapter_and_continue_uses_whole_path(
    tmp_path, compact_course, size
):
    chapters, lessons = compact_course
    app = TutorApp(tmp_path)
    app.store.data.update(onboarded=True, track="beginner")
    for lesson in lessons[:5]:
        app.store.entry(lesson)["completed"] = True
    async with app.run_test(size=size) as pilot:
        picker = app.screen.query_one("#chapter-picker", Select)
        assert picker.value == chapters[1].id
        listing = app.screen.query_one("#lesson-list", OptionList)
        assert listing.option_count == 5
        assert listing.get_option_at_index(0).id == lessons[5].id
        picker.value = chapters[0].id
        await pilot.pause()
        assert listing.get_option_at_index(0).id == lessons[0].id
        for control in ("#chapter-picker", "#syllabus", "#restart"):
            assert app.screen.query_one(control).region.bottom <= size[1] - 1
        await pilot.press("c")
        assert app.screen.lesson.id == lessons[5].id


async def test_onboarding_previews_chapters_and_outcomes(tmp_path, compact_course):
    chapters, _ = compact_course
    app = TutorApp(tmp_path)
    async with app.run_test(size=(80, 24)) as pilot:
        preview = str(app.screen.query_one("#path-topics", Static).content)
        assert chapters[0].title in preview
        assert chapters[0].outcome in preview
        assert chapters[2].title not in preview
        app.screen.query_one("#path", Select).value = "experienced"
        await pilot.pause()
        preview = str(app.screen.query_one("#path-topics", Static).content)
        assert chapters[2].title in preview
        assert chapters[0].title not in preview
