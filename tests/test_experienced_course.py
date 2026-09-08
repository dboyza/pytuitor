import pytest

from pytuitor.experienced_course import CHAPTERS, LESSONS
from pytuitor.legacy import default_input
from pytuitor.runner import execute


def test_experienced_course_has_six_complete_chapters():
    assert len(LESSONS) == 41
    assert len({lesson.id for lesson in LESSONS}) == 41
    assert sum(lesson.project for lesson in LESSONS) == 6
    seen = set()
    for chapter in CHAPTERS:
        units = [lesson for lesson in LESSONS if lesson.chapter_id == chapter.id]
        assert len(units) >= 5
        assert [lesson.project for lesson in units] == [False] * (len(units) - 1) + [True]
        for lesson in units:
            assert set(lesson.prerequisites) <= seen
            assert not lesson.starter
            assert lesson.body and lesson.hints
            seen.add(lesson.id)
    assert sum(lesson.project and len(lesson.files) > 1 for lesson in LESSONS) >= 2


@pytest.mark.parametrize("lesson", LESSONS, ids=lambda lesson: lesson.id)
async def test_experienced_references_and_repairs(lesson):
    correct = await execute(
        lesson, lesson.solution, default_input(lesson), files=lesson.solution_files
    )
    assert correct.passed, (correct.error, correct.checks)
    broken = await execute(lesson, lesson.repair, default_input(lesson), files=lesson.repair_files)
    assert not broken.passed, lesson.id


@pytest.mark.parametrize("lesson_id", ["metaclasses", "async-streams"])
async def test_deep_checks_reject_subtle_contract_regressions(lesson_id):
    lesson = next(lesson for lesson in LESSONS if lesson.id == lesson_id)
    if lesson_id == "metaclasses":
        source = lesson.solution.replace(
            '                raise ValueError("Duplicate kind")',
            "                mcls.registry[key] = cls\n"
            '                raise ValueError("Duplicate kind")',
        )
    else:
        source = lesson.solution.replace("if cleaned:", "if cleaned and cleaned not in result:")
    assert source != lesson.solution
    result = await execute(lesson, source)
    assert not result.passed
    assert not result.error, "The mutation must fail behaviorally, not because it cannot run."
