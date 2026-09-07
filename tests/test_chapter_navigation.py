from dataclasses import replace
from datetime import UTC, datetime, timedelta

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
    reviews = tuple(
        replace(lesson, id=lesson.id + "--review", review_of=lesson.id, project=False)
        for lesson in lessons
        if lesson.project
    )
    catalog = {lesson.id: lesson for lesson in (*lessons, *reviews)}
    monkeypatch.setattr(curriculum, "LESSONS", lessons)
    monkeypatch.setattr(curriculum, "CHAPTERS", chapters)
    monkeypatch.setattr(curriculum, "REVIEWS", reviews)
    monkeypatch.setattr(curriculum, "BY_ID", catalog)
    monkeypatch.setattr(screens, "BY_ID", catalog)
    return chapters, lessons, reviews


@pytest.mark.parametrize("size", [(80, 24), (140, 44)])
async def test_dashboard_browses_one_chapter_and_continue_uses_whole_path(
    tmp_path, compact_course, size
):
    chapters, lessons, _ = compact_course
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
        for control in ("#chapter-picker", "#review", "#study-notes", "#restart"):
            assert app.screen.query_one(control).region.bottom <= size[1] - 1
        await pilot.press("c")
        assert app.screen.lesson.id == lessons[5].id


async def test_review_preserves_unfinished_draft_and_resets_completed_attempt(
    tmp_path, compact_course
):
    _, lessons, reviews = compact_course
    project, review = lessons[4], reviews[0]
    app = TutorApp(tmp_path)
    app.store.data.update(onboarded=True, track="beginner", last_lesson=lessons[0].id)
    app.store.schedule_review(project)
    app.store.entry(review)["code"] = "print('my unfinished practice')"
    schedule = app.store.data["reviews"][project.id].copy()
    async with app.run_test(size=(80, 24)) as pilot:
        await pilot.click("#review")
        listing = app.screen.query_one("#review-list", OptionList)
        assert listing.option_count == 1
        assert "Scheduled" in str(listing.get_option_at_index(0).prompt)
        await pilot.press("enter")
        assert app.screen.lesson.id == review.id
        assert app.screen.query_one("#editor").text == "print('my unfinished practice')"
        assert app.store.data["last_lesson"] == lessons[0].id
        await pilot.press("ctrl+b")
        app.store.entry(review)["completed"] = True
        await pilot.click("#review")
        await pilot.press("enter")
        assert app.screen.query_one("#editor").text == ""
        assert app.store.data["reviews"][project.id] == schedule


async def test_due_practice_count_and_local_feedback_are_discoverable(tmp_path, compact_course):
    _, lessons, _ = compact_course
    app = TutorApp(tmp_path)
    app.store.data.update(onboarded=True, track="beginner")
    app.store.schedule_review(lessons[4])
    app.store.data["reviews"][lessons[4].id]["due"] = (
        datetime.now(UTC) - timedelta(days=1)
    ).isoformat()
    async with app.run_test(size=(80, 24)) as pilot:
        assert "1" in str(app.screen.query_one("#review").label)
        await pilot.click("#study-notes")
        assert app.screen.query("#feedback-opt-in")
        await pilot.press("escape")
        await pilot.click("#review")
        listing = app.screen.query_one("#review-list", OptionList)
        assert "Due now" in str(listing.get_option_at_index(0).prompt)


async def test_onboarding_previews_chapters_and_outcomes(tmp_path, compact_course):
    chapters, _, _ = compact_course
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
