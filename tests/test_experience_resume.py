"""Learner-level resume, compact evidence, and optional metadata recovery."""

import copy
from dataclasses import replace

import pytest
from textual.widgets import Static, TextArea

from pytuitor.app import TutorApp
from pytuitor.curriculum import BY_ID
from pytuitor.learning_progress import load_report, report_is_current, safe_view, saved_report
from pytuitor.models import Check
from pytuitor.runner import execute


async def test_reopen_restores_file_cursor_reading_and_selected_check(tmp_path):
    lesson = BY_ID["names-and-voices"]
    app = TutorApp(tmp_path)
    app.store.data.update(onboarded=True, last_lesson=lesson.id)
    async with app.run_test(size=(140, 44)) as pilot:
        await pilot.press("c")
        screen = app.screen
        screen.query_one("#editor", TextArea).load_text(lesson.solution)
        await pilot.press("f5")
        await app.workers.wait_for_complete()
        await pilot.pause()
        screen.check_selected = 2
        screen.check_selection_explicit = True
        screen.check_details = True
        screen.render_checks()
        screen.project_files()["notes.py"] = "\n".join(f"# line {i}" for i in range(100))
        screen.refresh_file_tree()
        screen.open_file("notes.py")
        await pilot.pause()
        screen.select_pane("editor")
        screen.query_one("#editor", TextArea).move_cursor((45, 4), center=True)
        screen.query_one("#reading-panel").scroll_to(y=12, animate=False, immediate=True)
        screen.note_saved("Try an empty name next.")
        screen.save_draft()
        before = copy.deepcopy(screen.stage_entry()["view"])
        await pilot.press("ctrl+b")
        assert "Try an empty name" in str(app.screen.query_one("#continue-summary", Static).content)
        await pilot.press("c")
        await pilot.pause()
        screen = app.screen
        assert screen.active_file == "notes.py"
        assert screen.query_one("#editor", TextArea).cursor_location == (45, 4)
        assert screen.active_pane == "editor"
        assert screen.check_selected == 2 and screen.check_details
        assert int(screen.query_one("#reading-panel").scroll_y) == before["reading"]
        assert "Earlier results" in str(screen.query_one("#check-summary", Static).content)
        screen.save_draft()
    reopened = TutorApp(tmp_path)
    async with reopened.run_test(size=(140, 44)) as pilot:
        await pilot.press("c")
        assert reopened.screen.active_file == "notes.py"
        assert reopened.screen.query_one("#editor", TextArea).cursor_location == (45, 4)


async def test_concrete_failure_does_not_repeat_learner_operation():
    lesson = replace(BY_ID["first-light"], checks=(), build_stage=None)
    check = Check(
        "Mutable counter", "__expect__('Counter value', tick(), 2)", True, "Check the increment."
    )
    contract = replace(lesson.stage_contract("build"), checks=(check,))
    result = await execute(
        lesson,
        "calls = 0\ndef tick():\n    global calls\n    calls += 1\n    return calls",
        stage=contract,
    )
    assert not result.passed
    observation = result.checks[0]["observations"][0]
    assert observation == dict(
        label="Counter value", actual="1", expected="2", comparison="==", passed=False
    )
    report = saved_report(result.checks, {"lesson.py": "x"}, 1)
    entry = {"last_check": report, "files": {"lesson.py": "x"}}
    assert report_is_current(entry, 1)
    assert load_report(entry, 1)[0]["observations"] == [observation]
    assert not load_report(entry, 2)
    entry["files"]["lesson.py"] = "changed"
    assert not report_is_current(entry, 1)


@pytest.mark.parametrize(
    "view",
    [
        None,
        [],
        {"active_file": []},
        {"positions": {"lesson.py": {"cursor": [-1, 5]}}},
        {"reading": float("inf")},
        {"pane": []},
    ],
)
def test_damaged_optional_view_is_ignored(view):
    result = safe_view({"view": view}, {"lesson.py": ""})
    assert "active_file" not in result
    assert "reading" not in result


@pytest.mark.parametrize("size", [(80, 24), (140, 44)], ids=["compact", "wide"])
@pytest.mark.parametrize(
    ("key", "pane", "focus"),
    [("f4", "editor", "exercise-scroll"), ("ctrl+t", "console", "results-scroll")],
    ids=["requirements", "console"],
)
async def test_stage_restore_does_not_override_new_keyboard_focus(
    tmp_path, monkeypatch, size, key, pane, focus
):
    lesson = BY_ID["first-light"]
    app = TutorApp(tmp_path)
    async with app.run_test(size=size) as pilot:
        await pilot.press("f5")
        screen = app.screen
        screen.query_one("#editor", TextArea).load_text(lesson.solution)
        await pilot.press("f5")
        await app.workers.wait_for_complete()
        await pilot.pause()
        callbacks = []
        schedule = screen.call_after_refresh

        def defer_restore(callback, *args, **kwargs):
            if callback == screen.restore_view:
                callbacks.append((callback, args, kwargs))
                return True
            return schedule(callback, *args, **kwargs)

        monkeypatch.setattr(screen, "call_after_refresh", defer_restore)
        await pilot.press("ctrl+n")
        assert screen.stage == "repair"
        assert callbacks
        await pilot.press(key)
        assert app.focused.id == focus
        for callback, args, kwargs in callbacks:
            callback(*args, **kwargs)
        await pilot.pause()
        assert screen.active_pane == pane
        assert app.focused.id == focus
