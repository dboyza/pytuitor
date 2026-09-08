"""Coverage promises, new learner journeys, and returning-profile compatibility."""

import re
from copy import deepcopy
from pathlib import Path

import pytest
from textual.widgets import OptionList, Select, TextArea

from pytuitor.app import TutorApp
from pytuitor.curriculum import BY_ID, LESSONS, track_lessons
from pytuitor.runner import execute
from pytuitor.state import Store

NEW_TOPICS = (
    "recursion-basics",
    "recursive-collections",
    "regex-validation",
    "regex-transformations",
    "counting-and-grouping",
    "queues-with-deque",
    "named-states",
    "comparing-sets",
    "nested-collections",
    "editing-collections",
    "date-time-formats",
    "numeric-tools",
    "repeatable-randomness",
    "callable-tools",
    "functional-pipelines",
    "decorator-factories",
    "exception-boundaries",
    "managed-contexts",
    "iterator-recipes",
    "adjacent-groups",
    "dataclass-lifecycle",
    "typed-contracts",
    "practical-object-protocols",
    "class-construction",
)


def test_coverage_map_links_all_31_topic_families_to_active_lessons():
    document = Path("docs/coverage.md").read_text()
    topics = set(re.findall(r"^\| ([a-z_]+) \|", document, re.MULTILINE))
    assert topics == set(
        "variables strings conditionals loops functions lists tuples dictionaries sets "
        "comprehensions exceptions file_io classes functional decorators generators "
        "context_managers dataclasses type_hints regex testing recursion modules collections "
        "itertools json datetime enums pathlib oop_advanced async".split()
    )
    active = {lesson.id for lesson in LESSONS}
    for relative in re.findall(r"\]\((\.\./src/[^)]+)\)", document):
        path = Path("docs") / relative
        assert path.is_file()
        assert path.stem in active
    assert set(NEW_TOPICS) <= active


@pytest.mark.parametrize("identifier", NEW_TOPICS)
async def test_new_topic_checks_reject_empty_programs(identifier):
    lesson = BY_ID[identifier]
    result = await execute(lesson, "", lesson.stdin)
    assert not result.passed


@pytest.mark.parametrize(
    ("identifier", "size"),
    [
        ("regex-validation", (80, 24)),
        ("recursive-collections", (140, 44)),
        ("named-states", (80, 24)),
        ("dataclass-lifecycle", (140, 44)),
        ("managed-contexts", (80, 24)),
        ("functional-pipelines", (140, 44)),
    ],
)
async def test_new_topics_are_reachable_and_complete_both_stages(tmp_path, identifier, size):
    lesson = BY_ID[identifier]
    app = TutorApp(tmp_path)
    app.store.data.update(onboarded=True, track=lesson.track)
    async with app.run_test(size=size) as pilot:
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
        assert screen.lesson.id == identifier
        editor = screen.query_one("#editor", TextArea)
        assert not editor.text
        for stage in ("build", "repair"):
            assert screen.stage == stage
            editor.load_text(lesson.solution)
            await pilot.pause()
            await pilot.press("f5")
            await app.workers.wait_for_complete()
            assert screen.stage_passed(stage)
            if stage == "build":
                assert app.store.status(lesson) != "completed"
                await pilot.press("ctrl+n")
                await pilot.pause()
                assert editor.text == lesson.repair
        assert app.store.status(lesson) == "completed"
        await pilot.press("ctrl+b")
    restored = Store(tmp_path)
    assert restored.status(lesson) == "completed"
    assert restored.entry(lesson)["code"] == lesson.solution
    assert restored.entry(lesson)["repair"]["code"] == lesson.solution
    restored.close()


@pytest.mark.parametrize("track", ["beginner", "experienced"])
def test_previous_completions_and_drafts_survive_the_topic_expansion(tmp_path, track):
    store = Store(tmp_path)
    store.data.update(onboarded=True, track=track)
    for lesson in track_lessons(track):
        if lesson.id not in NEW_TOPICS:
            store.entry(lesson).update(completed=True, code=f"# saved {lesson.id}")
    previous = deepcopy(store.data["lessons"])
    store.save()
    store.close()
    store = Store(tmp_path)
    assert store.data["lessons"] == previous
    assert store.next_lesson().id in NEW_TOPICS
    assert all(store.status(BY_ID[identifier]) == "completed" for identifier in previous)
    store.close()


@pytest.mark.parametrize(
    ("identifier", "needle"),
    [("exception-boundaries", "stream.close()"), ("managed-contexts", "self.resource.close()")],
)
async def test_resource_checks_reject_duplicate_cleanup(identifier, needle):
    lesson = BY_ID[identifier]
    source = lesson.solution.replace(needle, needle + "; " + needle)
    assert source != lesson.solution
    result = await execute(lesson, source)
    assert not result.passed
    assert not result.error


async def test_random_checks_reject_a_generator_shared_between_calls():
    lesson = BY_ID["repeatable-randomness"]
    source = lesson.solution.replace(
        "rng = random.Random(seed)",
        "if not hasattr(draw, 'rng'):\n        draw.rng = random.Random(seed)\n    rng = draw.rng",
    )
    result = await execute(lesson, source)
    assert not result.passed
    assert not result.error


@pytest.mark.parametrize(
    ("identifier", "source"),
    [
        (
            "comparing-sets",
            "required = set(input().split())\navailable = set(input().split())\n"
            "shared = required.intersection(available)\nmissing = required.difference(available)\n"
            "combined = required.union(available)\n"
            "exclusive = required.symmetric_difference(available)\n"
            "ready = required.issubset(available)\n",
        ),
        (
            "numeric-tools",
            "def summarize(values, capacity):\n"
            "    if capacity <= 0 or not values:\n        raise ValueError('Invalid')\n"
            "    ordered = sorted(values)\n    n = len(values)\n"
            "    median = (ordered[(n - 1) // 2] + ordered[n // 2]) / 2\n"
            "    return (sum(values) / n, median, (n + capacity - 1) // capacity)\n",
        ),
    ],
)
async def test_topic_checks_accept_equivalent_implementations(identifier, source):
    lesson = BY_ID[identifier]
    result = await execute(lesson, source, lesson.stdin)
    assert result.passed, (result.error, result.checks)
