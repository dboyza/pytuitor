"""Real runner and learner journeys for optional mixed review."""

import pytest
from textual.widgets import Button, OptionList, TextArea
from textual.worker import WorkerCancelled

from pytuitor import review_progress as progress
from pytuitor.app import TutorApp
from pytuitor.content.reviews import REVIEWS
from pytuitor.curriculum import CHAPTERS
from pytuitor.review_screen import ReviewHub, ReviewScreen
from pytuitor.runner import execute

TASKS = [task for tasks in REVIEWS.values() for task in tasks]


def test_every_chapter_has_a_mixed_session():
    assert set(REVIEWS) == {chapter.id for chapter in CHAPTERS}
    assert len({task.id for task in TASKS}) == 63
    for tasks in REVIEWS.values():
        assert [task.kind for task in tasks] == ["predict", "debug", "code"]


@pytest.mark.parametrize("task", TASKS, ids=lambda task: task.id)
async def test_authored_review_contract(task):
    if task.kind == "predict":
        source = task.prompt.split("```python\n", 1)[1].split("```", 1)[0]
        result = await execute(task.lesson(), source, check=False)
        assert not result.error
        assert result.output.strip() == task.choices[task.answer]
        return
    result = await execute(task.lesson(), task.reference)
    assert result.passed, result
    if task.kind == "debug":
        broken = await execute(task.lesson(), task.starter)
        assert not broken.passed


async def finish(pilot, screen):
    for _ in range(150):
        await pilot.pause(0.03)
        if not screen.running:
            return
    raise AssertionError("Review did not finish")


async def test_review_round_trip_keeps_course_anchor(tmp_path):
    app = TutorApp(tmp_path)
    app.store.data.update(onboarded=True, last_lesson="names-and-voices")
    async with app.run_test(size=(80, 24)) as pilot:
        await pilot.click("#review")
        assert isinstance(app.screen, ReviewHub)
        await pilot.click("#review-open")
        screen = app.screen
        assert isinstance(screen, ReviewScreen)
        screen.query_one("#review-choices", OptionList).highlighted = screen.task.answer
        await pilot.press("f5")
        await finish(pilot, screen)
        assert screen.attempt["passed"]
        await pilot.press("ctrl+n")
        await pilot.pause()
        assert screen.task.kind == "debug"
        screen.query_one("#review-editor", TextArea).load_text(screen.task.reference)
        await pilot.pause()
        await pilot.press("f5")
        await finish(pilot, screen)
        assert screen.attempt["passed"]
        await pilot.press("escape")
        await pilot.click("#review-open")
        screen = app.screen
        assert screen.index == 1
        assert screen.query_one("#review-editor", TextArea).text == screen.task.reference
        await pilot.press("ctrl+n")
        await pilot.pause()
        screen.query_one("#review-editor", TextArea).load_text(screen.task.reference)
        await pilot.pause()
        await pilot.press("f5")
        await finish(pilot, screen)
        assert not screen.query_one("#review-next", Button).disabled
        await pilot.press("ctrl+n")
        await pilot.pause()
        assert isinstance(app.screen, ReviewHub)
        assert progress.entry(app.store, "first-programs")["sessions"] == 1
        assert app.store.data["last_lesson"] == "names-and-voices"
        assert not app.store.data["lessons"]
        app.save_screenshot("review-hub-80.svg", ".artifacts")


def test_optional_scheduling_and_assistance(tmp_path):
    from datetime import date, timedelta

    from pytuitor.curriculum import chapter_activities
    from pytuitor.state import Store

    store = Store(tmp_path)
    day = date(2026, 1, 1)
    chapter = "first-programs"
    assert progress.suggested(store, day) is None
    for lesson in chapter_activities(chapter):
        store.entry(lesson).update(completed=True, completed_revision=lesson.revision)
    assert progress.suggested(store, day) == chapter
    for interval in (2, 7, 21, 45, 45):
        progress.restart(store, chapter)
        for task in REVIEWS[chapter]:
            progress.task_entry(store, chapter, task)["passed"] = True
        assert progress.complete(store, chapter, day)
        assert not progress.complete(store, chapter, day)
        assert progress.entry(store, chapter)["due"] == (day + timedelta(days=interval)).isoformat()
        assert not progress.due(store, chapter, day)
        day += timedelta(days=interval)
        assert progress.due(store, chapter, day)
    progress.restart(store, chapter)
    for task in REVIEWS[chapter]:
        progress.task_entry(store, chapter, task).update(passed=True, assisted=True)
    progress.complete(store, chapter, day)
    assert progress.entry(store, chapter)["due"] == (day + timedelta(days=2)).isoformat()
    progress.review_data(store)["paused"] = True
    assert progress.suggested(store, day + timedelta(days=5)) is None
    store.close()


async def test_changed_review_draft_cannot_pass_delayed_check(tmp_path, monkeypatch):
    import asyncio

    import pytuitor.review_screen as ui

    original = ui.execute
    started, release = asyncio.Event(), asyncio.Event()

    async def delayed(*args, **kwargs):
        started.set()
        await release.wait()
        return await original(*args, **kwargs)

    monkeypatch.setattr(ui, "execute", delayed)
    app = TutorApp(tmp_path)
    app.store.data["onboarded"] = True
    progress.entry(app.store, "first-programs")["index"] = 1
    async with app.run_test(size=(80, 24)) as pilot:
        app.push_screen(ReviewScreen("first-programs"))
        await pilot.pause()
        screen = app.screen
        editor = screen.query_one("#review-editor", TextArea)
        editor.load_text(screen.task.reference)
        await pilot.pause()
        await pilot.press("f5")
        await started.wait()
        editor.load_text('print("changed")')
        await pilot.pause()
        release.set()
        await app.workers.wait_for_complete()
        assert not screen.attempt.get("passed")
        assert screen.query_one("#review-next", Button).disabled


async def test_review_result_save_failure_keeps_task_incomplete(tmp_path, monkeypatch):
    app = TutorApp(tmp_path)
    app.store.data["onboarded"] = True
    async with app.run_test() as pilot:
        app.push_screen(ReviewScreen("first-programs"))
        await pilot.pause()
        screen = app.screen
        screen.query_one("#review-choices", OptionList).highlighted = screen.task.answer
        await pilot.pause()
        monkeypatch.setattr(app, "persist", lambda: False)
        await pilot.press("f5")
        await app.workers.wait_for_complete()
        assert not screen.attempt.get("passed")
        assert screen.query_one("#review-next", Button).disabled


async def test_start_over_during_review_does_not_restore_erased_progress(tmp_path, monkeypatch):
    import asyncio

    import pytuitor.review_screen as ui

    original = ui.execute
    started, release = asyncio.Event(), asyncio.Event()

    async def delayed(*args, **kwargs):
        started.set()
        await release.wait()
        return await original(*args, **kwargs)

    monkeypatch.setattr(ui, "execute", delayed)
    app = TutorApp(tmp_path)
    app.store.data["onboarded"] = True
    progress.entry(app.store, "first-programs")["index"] = 1
    async with app.run_test() as pilot:
        app.push_screen(ReviewScreen("first-programs"))
        await pilot.pause()
        screen = app.screen
        screen.query_one("#review-editor", TextArea).load_text(screen.task.reference)
        await pilot.pause()
        await pilot.press("f5")
        await started.wait()
        workers = [worker for worker in app.workers if worker.name == "check_answer"]
        assert len(workers) == 1
        app.action_restart()
        await pilot.pause()
        await pilot.click("#confirm-restart")
        release.set()
        # Keep the worker reference: the manager may already have removed it.
        with pytest.raises(WorkerCancelled):
            await workers[0].wait()
        await pilot.pause()
        assert not app.store.data["onboarded"]
        assert "reviews" not in app.store.data
