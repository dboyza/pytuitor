import pytest

from pytuitor.curriculum import LESSONS, default_input
from pytuitor.runner import execute


@pytest.mark.parametrize("lesson", LESSONS, ids=lambda lesson: lesson.id)
async def test_reference_solution_meets_contract(lesson):
    result = await execute(
        lesson, lesson.solution, default_input(lesson), files=lesson.solution_files
    )
    assert result.passed, (result.error, result.checks, result.output)


@pytest.mark.parametrize("lesson", LESSONS, ids=lambda lesson: lesson.id)
async def test_starter_needs_work(lesson):
    result = await execute(lesson, lesson.starter, default_input(lesson))
    assert not result.passed


async def test_timeout_and_output_limit():
    result = await execute(LESSONS[0], "while True: pass", timeout=0.3)
    assert "Stopped" in result.error
    result = await execute(LESSONS[0], "while True: print('x' * 1000)")
    assert "limit" in result.error.lower()
    assert len(result.output) <= 65536


async def test_errors_are_actionable_and_next_run_recovers():
    result = await execute(LESSONS[0], 'print("oops)')
    assert "SyntaxError" in result.error
    assert "lesson.py" in result.error
    result = await execute(LESSONS[0], "input()")
    assert "type it in the console" in result.error
    result = await execute(LESSONS[0], LESSONS[0].solution)
    assert result.passed


async def test_run_does_not_mark_passing_checks():
    result = await execute(LESSONS[0], LESSONS[0].solution, check=False)
    assert result.output == "Welcome, explorer!\n13\n"
    assert not result.passed
    assert result.checks == []
