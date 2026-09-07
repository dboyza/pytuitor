from collections import Counter

import pytest

from pytuitor.curriculum import BY_ID, CHAPTERS, CONCEPTS, LESSONS, REVIEWS, default_input
from pytuitor.runner import execute


def test_catalog_has_complete_chapters_and_ordered_prerequisites():
    assert len(LESSONS) == len({lesson.id for lesson in LESSONS}) == 60
    assert sum(lesson.project for lesson in LESSONS) == 12
    assert Counter(lesson.track for lesson in LESSONS) == {"beginner": 30, "experienced": 30}
    assert len(CHAPTERS) == len(REVIEWS) == 12
    seen = set()
    for lesson in LESSONS:
        assert set(lesson.prerequisites) <= seen, lesson.id
        assert lesson.body.strip() and lesson.checks and lesson.hints
        assert lesson.entrypoint in lesson.files
        assert set(lesson.concepts) <= set(CONCEPTS)
        seen.add(lesson.id)
    for chapter in CHAPTERS:
        units = [lesson for lesson in LESSONS if lesson.chapter_id == chapter.id]
        assert len(units) == 5
        assert sum(lesson.project for lesson in units) == 1
        assert units[-1].project


@pytest.mark.parametrize("lesson", REVIEWS, ids=lambda lesson: lesson.id)
async def test_review_contract_is_executable_and_requires_work(lesson):
    assert lesson.body != BY_ID[lesson.review_of].body
    result = await execute(lesson, lesson.solution, default_input(lesson))
    assert result.passed, (lesson.id, result.checks, result.error)
    empty = await execute(lesson, "", default_input(lesson))
    assert not empty.passed
