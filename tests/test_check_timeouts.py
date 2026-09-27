"""A cumulative milestone must not spend one timeout budget across all its checks."""

import asyncio

import pytest

from pytuitor.app import TutorApp
from pytuitor.curriculum import BY_ID
from pytuitor.models import Check, StageContract
from pytuitor.runner import execute


@pytest.mark.parametrize("through_ui", [True, False], ids=["workbench", "headless"])
async def test_correct_game_checks_have_individual_time_budgets(tmp_path, through_ui):
    lesson = BY_ID["reach-caves"]
    contract = lesson.stage_contract("build")
    files = dict(contract.reference_files)
    # Reproduce a slow host: each fresh program takes a modest amount of time,
    # but the eighteen checks together exceed the ordinary five-second limit.
    files[lesson.entrypoint] = "import time\ntime.sleep(0.35)\n" + files[lesson.entrypoint]
    if through_ui:
        app = TutorApp(tmp_path)
        app.store.data["onboarded"] = True
        app.store.entry(lesson).update(files=files, code=files[lesson.entrypoint])
        async with app.run_test(size=(80, 24)) as pilot:
            app.open_activity(lesson)
            await pilot.pause()
            screen = app.screen
            await pilot.press("f5")
            await app.workers.wait_for_complete()
            assert screen.stage_passed("build"), screen.transcript
            assert len(screen.check_results) == len(contract.checks)
    else:
        result = await execute(lesson, files[lesson.entrypoint], files=files, stage=contract)
        assert result.passed, result.error
        assert len(result.checks) == len(contract.checks)


@pytest.mark.parametrize("check", [True, False], ids=["later-check", "run"])
async def test_individual_programs_still_time_out(check):
    lesson = BY_ID["reach-caves"]
    events = []
    contract = StageContract(
        checks=(
            Check("Quick case", "True", True, ""),
            Check("Stalled case", "__import__('time').sleep(20)", None, ""),
        ),
    )
    result = await asyncio.wait_for(
        execute(
            lesson,
            "" if check else "import time\ntime.sleep(20)",
            check=check,
            stage=contract,
            timeout=2,
            on_check=events.append,
        ),
        timeout=10,
    )
    assert "Stopped after 2 seconds" in result.error
    assert not result.passed
    if check:
        assert any(event.get("passed") and event["number"] == 1 for event in events)
        assert events[-1]["number"] == 2
        assert events[-1]["status"] == "running"
