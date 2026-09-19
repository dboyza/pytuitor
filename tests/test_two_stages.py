import asyncio
from pathlib import Path

import pytest
from textual.widgets import Button, Static, TextArea

from pytuitor.app import TutorApp
from pytuitor.curriculum import LESSONS, default_input
from pytuitor.runner import execute
from pytuitor.screens import Dashboard


async def finish(pilot, screen):
    for _ in range(150):
        await pilot.pause(0.04)
        if not screen.running:
            return
    raise AssertionError("Check did not finish")


@pytest.mark.parametrize("lesson", LESSONS, ids=lambda lesson: lesson.id)
async def test_repair_contains_a_real_bug(lesson):
    assert lesson.starter == ""
    repair = lesson.stage_contract("repair")
    result = await execute(
        lesson,
        repair.starter_files[lesson.entrypoint],
        default_input(lesson, "repair"),
        files=repair.starter_files,
        stage=repair,
    )
    assert not result.passed
    assert result.checks
    assert any(not case["passed"] for case in result.checks)


async def test_mouse_selection_and_focus_outline(tmp_path):
    app = TutorApp(tmp_path)
    app.store.data["onboarded"] = True
    async with app.run_test(size=(140, 44)) as pilot:
        await pilot.click("#lesson-list", offset=(5, 3))
        await pilot.pause()
        assert isinstance(app.screen, Dashboard)
        assert app.screen.current.id == "names-and-voices"
        await pilot.click("#lesson-list", offset=(5, 3), times=2)
        await pilot.pause()
        assert app.screen.lesson.id == "names-and-voices"
        assert app.screen.query_one("#editor", TextArea).text == ""
        for key, pane, selector in [
            ("ctrl+t", "editor", "#editor"),
            ("ctrl+t", "console", "#console-pane"),
            ("ctrl+t", "lesson", "#reading-panel"),
        ]:
            await pilot.press(key)
            await pilot.pause()
            assert app.screen.active_pane == pane
            assert app.screen.query_one(selector).styles.border_top[1].hex == "#3776AB"
        await pilot.click("#editor")
        assert app.screen.active_pane == "editor"
        await pilot.click("#reading-panel", offset=(3, 2))
        assert app.screen.active_pane == "lesson"


async def test_two_stages_save_independently_and_report_every_case(tmp_path):
    app = TutorApp(tmp_path)
    app.store.data.update(onboarded=True, last_lesson="names-and-voices")
    lesson = LESSONS[1]
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("c")
        screen = app.screen
        assert screen.query_one("#stage-repair", Button).disabled
        await pilot.press("ctrl+n")
        assert screen.stage == "build"
        screen.query_one("#editor", TextArea).load_text(lesson.solution)
        await pilot.press("f5")
        await finish(pilot, screen)
        result = str(screen.query_one("#results", Static).content)
        assert result.count("PASS ·") == len(lesson.stage_contract("build").checks)
        for label in (
            "Keyboard input:",
            "Expected result:",
            "Actual result:",
            "Expected printed output:",
            "Printed output:",
        ):
            assert result.count(label) == len(lesson.stage_contract("build").checks)
        assert "Ada" in result and "Lin" in result and "Alex Chen" in result
        assert app.store.status(lesson) != "completed"
        await pilot.press("ctrl+n")
        assert screen.stage == "repair"
        assert screen.query_one("#editor", TextArea).text == lesson.repair
        await pilot.press("f5")
        await finish(pilot, screen)
        assert "FAIL ·" in str(screen.query_one("#results", Static).content)
        screen.action_hint()
        assert "Read two answers" in str(screen.query_one("#hint-copy", Static).content)
        screen.action_solution()
        await pilot.pause()
        assert (
            screen.app.screen.query_one("#solution-code", TextArea).text
            == lesson.stage_contract("repair").reference_files[lesson.entrypoint]
        )
        await pilot.press("escape")
        await pilot.press("ctrl+b", "c")
        screen = app.screen
        assert screen.stage == "repair"
        repair = lesson.stage_contract("repair")
        screen.query_one("#editor", TextArea).load_text(
            repair.reference_files[lesson.entrypoint] + "# repaired\n"
        )
        await pilot.press("f5")
        await finish(pilot, screen)
        assert app.store.status(lesson) == "completed"
        assert not app.store.entry(lesson).get("prediction")
        await pilot.click("#stage-build")
        assert screen.query_one("#editor", TextArea).text == lesson.solution
        await pilot.click("#stage-repair")
        assert screen.query_one("#editor", TextArea).text.endswith("# repaired\n")
        Path(".artifacts").mkdir(exist_ok=True)
        app.save_screenshot("two-stages-120.svg", ".artifacts")
    resumed = TutorApp(tmp_path)
    async with resumed.run_test() as pilot:
        assert resumed.store.data["lessons"][lesson.id]["repair"]["code"].endswith("# repaired\n")


async def test_repair_reset_uses_its_contract_and_backs_up_the_draft(tmp_path):
    app = TutorApp(tmp_path)
    app.store.data.update(onboarded=True, last_lesson="names-and-voices")
    lesson = LESSONS[1]
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("c")
        screen = app.screen
        build = lesson.stage_contract("build")
        screen.query_one("#editor", TextArea).load_text(build.reference_files[lesson.entrypoint])
        await pilot.press("f5")
        await finish(pilot, screen)
        await pilot.press("ctrl+n")
        await pilot.pause()
        repair = lesson.stage_contract("repair")
        screen.query_one("#editor", TextArea).load_text("# keep this repair draft\n")
        screen.action_reset()
        await pilot.pause()
        await pilot.click("#confirm-reset")
        await pilot.pause()
        assert screen.query_one("#editor", TextArea).text == repair.starter_files[lesson.entrypoint]
        assert "checked_code" not in app.store.entry(lesson)["repair"]
        backups = list((tmp_path / "exports").glob("names-and-voices-repair-*.py"))
        assert backups and backups[0].read_text() == "# keep this repair draft\n"


async def test_late_edit_cannot_mark_an_earlier_stage_draft_passed(tmp_path, monkeypatch):
    from pytuitor import lesson_screen as lesson_screen_module
    from pytuitor.runner import execute as real_execute

    started = asyncio.Event()
    release = asyncio.Event()

    async def delayed_execute(*args, **kwargs):
        started.set()
        await release.wait()
        return await real_execute(*args, **kwargs)

    monkeypatch.setattr(lesson_screen_module, "execute", delayed_execute)
    app = TutorApp(tmp_path)
    app.store.data.update(onboarded=True, last_lesson="names-and-voices")
    lesson = LESSONS[1]
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("c")
        screen = app.screen
        editor = screen.query_one("#editor", TextArea)
        editor.load_text(lesson.stage_contract("build").reference_files[lesson.entrypoint])
        screen.action_check()
        await asyncio.wait_for(started.wait(), 1)
        editor.load_text(
            lesson.stage_contract("build").reference_files[lesson.entrypoint] + "# newer\n"
        )
        release.set()
        await finish(pilot, screen)
        assert not screen.stage_passed("build")
        assert "earlier draft" in str(screen.query_one("#results", Static).content)


async def test_check_streams_start_and_result_and_isolates_cases():
    events = []
    lesson = LESSONS[1]
    result = await execute(lesson, lesson.solution, default_input(lesson), on_check=events.append)
    assert result.passed
    assert [event["status"] for event in events] == ["running", "finished"] * 3
    assert [case["actual"] for case in result.checks] == [
        repr(f"Welcome, {name}!") for name in ("Ada", "Lin", "Alex Chen")
    ]
