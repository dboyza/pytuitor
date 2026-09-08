"""Behavioral checks for the complete beginner course."""

import ast
import re

import pytest

from pytuitor.beginner_course import CHAPTERS, LESSONS
from pytuitor.runner import execute


def test_beginner_course_has_six_coherent_chapters():
    assert len(LESSONS) == 46
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
        assert len(units) >= 5
        assert units[-1].project
        assert set(units[-1].concepts) == {
            concept for lesson in units[:-1] for concept in lesson.concepts
        }
    assert sum(lesson.project and len(lesson.files) > 1 for lesson in LESSONS) >= 2


@pytest.mark.parametrize("lesson", LESSONS, ids=lambda lesson: lesson.id)
async def test_beginner_reference_passes_and_repair_has_a_real_defect(lesson):
    reference = await execute(lesson, lesson.solution, lesson.stdin, files=lesson.solution_files)
    assert reference.passed, (lesson.id, reference.error, reference.checks)
    repair = await execute(lesson, lesson.repair, lesson.stdin, files=lesson.repair_files)
    assert not repair.passed, lesson.id


def test_beginner_worked_examples_have_valid_python_syntax():
    for lesson in LESSONS:
        for block in re.findall(r"```python\n(.*?)```", lesson.body, re.DOTALL):
            ast.parse(block, filename=lesson.id + ".md")
