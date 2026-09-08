"""New curriculum remains reachable for both new and returning learners."""

from copy import deepcopy

import pytest
from textual.widgets import Collapsible, OptionList, Select, TextArea

from pytuitor.app import TutorApp
from pytuitor.curriculum import BY_ID, track_lessons
from pytuitor.state import Store

NEW_LESSONS = ("decimal-measurements", "tuples-and-sets", "loop-helpers")


@pytest.mark.parametrize("identifier", NEW_LESSONS)
async def test_new_lesson_build_repair_and_saved_drafts(tmp_path, identifier):
    lesson = BY_ID[identifier]
    app = TutorApp(tmp_path)
    app.store.data.update(onboarded=True, track="beginner")
    async with app.run_test(size=(80, 24)) as pilot:
        app.screen.query_one("#chapter-picker", Select).value = lesson.chapter_id
        await pilot.pause()
        listing = app.screen.query_one("#lesson-list", OptionList)
        index = next(
            i
            for i in range(listing.option_count)
            if listing.get_option_at_index(i).id == identifier
        )
        listing.focus()
        await pilot.press("home", *(["down"] * index), "enter")
        await pilot.pause()
        screen = app.screen
        editor = screen.query_one("#editor", TextArea)
        assert editor.text == ""
        editor.load_text(lesson.solution)
        await pilot.pause()
        await pilot.press("f5")
        await app.workers.wait_for_complete()
        assert screen.stage_passed("build")
        assert app.store.status(lesson) != "completed"
        await pilot.press("ctrl+n")
        await pilot.pause()
        assert screen.stage == "repair"
        assert editor.text == lesson.repair
        await pilot.press("f5")
        await app.workers.wait_for_complete()
        assert not screen.stage_passed("repair")
        editor.load_text(lesson.solution)
        await pilot.pause()
        await pilot.press("f5")
        await app.workers.wait_for_complete()
        assert app.store.status(lesson) == "completed"
        await pilot.press("ctrl+b")
    restored = Store(tmp_path)
    entry = restored.entry(lesson)
    assert entry["code"] == lesson.solution
    assert entry["repair"]["code"] == lesson.solution
    assert restored.status(lesson) == "completed"
    restored.close()


async def test_returning_learner_keeps_progress_and_discovers_added_lessons(tmp_path):
    store = Store(tmp_path)
    store.data.update(onboarded=True, track="beginner")
    for lesson in track_lessons("beginner"):
        if lesson.id not in NEW_LESSONS:
            store.entry(lesson).update(completed=True, code=f"# saved {lesson.id}")
    store.data["last_lesson"] = "notes-archiver"
    previous = deepcopy(store.data["lessons"])
    store.save()
    store.close()
    app = TutorApp(tmp_path)
    async with app.run_test(size=(140, 44)) as pilot:
        assert app.store.data["lessons"] == previous
        assert app.store.next_lesson().id == NEW_LESSONS[0]
        await pilot.press("s")
        first = app.screen.query_one("#syllabus-b-foundations", Collapsible)
        second = app.screen.query_one("#syllabus-b-collections", Collapsible)
        assert first.title.split()[-2:] == ["5", "1"]
        assert second.title.split()[-2:] == ["9", "1"]
        await pilot.press("escape", "c")
        assert app.screen.lesson.id == NEW_LESSONS[0]
        assert all(app.store.data["lessons"][key] == value for key, value in previous.items())


@pytest.mark.parametrize(
    ("identifier", "alternative"),
    [
        (
            "decimal-measurements",
            "centimeters = float(input())\nmeters = centimeters * 0.01\n"
            'print(format(meters, ".2f") + " m")\n',
        ),
        (
            "tuples-and-sets",
            "pair = tuple(input().split())\nfirst = pair[0]\nsecond = pair[1]\n"
            "seen = set(input().split())\n"
            "print(first in seen)\nprint(second in seen)\nprint(len(seen))\n",
        ),
        (
            "loop-helpers",
            "count = int(input())\nnames = input().split()\ncolors = input().split()\n"
            "slots = list(range(1, count + 1))\n"
            "numbered = list(enumerate(names, 1))\npairs = list(zip(names, colors))\n",
        ),
    ],
)
async def test_new_checks_accept_alternatives_and_reject_blank_programs(identifier, alternative):
    from pytuitor.runner import execute

    lesson = BY_ID[identifier]
    result = await execute(lesson, alternative, lesson.stdin)
    assert result.passed, (result.error, result.checks)
    blank = await execute(lesson, "", lesson.stdin)
    assert not blank.passed
