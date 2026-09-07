"""Behavioral checks for the complete beginner course and its fresh practice."""

import ast
import re
from dataclasses import replace

import pytest

from pytuitor.beginner_course import CHAPTERS, LESSONS
from pytuitor.runner import execute


def test_beginner_course_has_six_coherent_chapters():
    assert len(LESSONS) == 30
    assert sum(lesson.project for lesson in LESSONS) == 6
    seen = set()
    for lesson in LESSONS:
        assert set(lesson.prerequisites) <= seen
        seen.add(lesson.id)
        assert lesson.starter == ""
        assert lesson.body.strip()
        assert len(lesson.hints) >= 2
    for chapter in CHAPTERS:
        units = [lesson for lesson in LESSONS if lesson.chapter_id == chapter.id]
        assert len(units) == 5
        assert units[-1].project
        assert set(units[-1].concepts) == {
            concept for lesson in units[:-1] for concept in lesson.concepts
        }
        assert units[-1].review is not None
        assert units[-1].review.solution != units[-1].solution
    assert sum(lesson.project and len(lesson.files) > 1 for lesson in LESSONS) >= 2


@pytest.mark.parametrize("lesson", LESSONS, ids=lambda lesson: lesson.id)
async def test_beginner_reference_passes_and_repair_has_a_real_defect(lesson):
    reference = await execute(lesson, lesson.solution, lesson.stdin, files=lesson.solution_files)
    assert reference.passed, (lesson.id, reference.error, reference.checks)
    repair = await execute(lesson, lesson.repair, lesson.stdin, files=lesson.repair_files)
    assert not repair.passed, lesson.id


@pytest.mark.parametrize(
    "lesson", [lesson for lesson in LESSONS if lesson.review], ids=lambda lesson: lesson.id
)
async def test_beginner_review_reference_and_blank_attempt(lesson):
    review = lesson.review
    practice = replace(
        lesson,
        id=lesson.id + "--practice",
        body=review.body,
        solution=review.solution,
        checks=review.checks,
        entrypoint="lesson.py",
        files=("lesson.py",),
        solution_files=None,
        repair_files=None,
    )
    result = await execute(practice, practice.solution, review.stdin)
    assert result.passed, (lesson.id, result.error, result.checks)
    blank = await execute(practice, "", review.stdin)
    assert not blank.passed


def test_beginner_worked_examples_have_valid_python_syntax():
    for lesson in LESSONS:
        for block in re.findall(r"```python\n(.*?)```", lesson.body, re.DOTALL):
            ast.parse(block, filename=lesson.id + ".md")
