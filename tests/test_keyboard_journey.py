import json
from pathlib import Path

import pytest
from textual.widgets import Input, Select, Static, TextArea

from pytuitor.app import TutorApp
from pytuitor.curriculum import BY_ID, LESSONS
from pytuitor.dialogs import ConfirmRestart, KeyboardHelp
from pytuitor.screens import Dashboard
from pytuitor.setup import Onboarding


async def until(pilot, condition):
    for _ in range(150):
        if condition():
            return
        await pilot.pause(0.04)
    raise AssertionError("The UI did not reach the expected state")


async def tab_to(pilot, app, widget_id):
    for _ in range(30):
        if app.focused and app.focused.id == widget_id:
            return
        await pilot.press("tab")
    raise AssertionError(f"Cannot reach {widget_id} with Tab")


async def command(pilot, name):
    await pilot.press("ctrl+p")
    await pilot.pause()
    await pilot.press(*name)
    await pilot.pause(0.2)
    await pilot.press("enter")
    await pilot.pause()


@pytest.mark.parametrize("size", [(80, 24), (140, 44)])
async def test_beginner_can_complete_lessons_using_only_keyboard(tmp_path, size):
    app = TutorApp(tmp_path)
    async with app.run_test(size=size) as pilot:
        assert app.screen.query_one("#path", Select).value == "beginner"
        await pilot.press("f10")
        await pilot.pause()
        assert isinstance(app.screen, KeyboardHelp)
        await pilot.press("escape", "f5")
        await pilot.pause()
        assert isinstance(app.screen, Dashboard)
        await pilot.press("c")
        await pilot.pause()
        await pilot.press(
            "ctrl+t", "ctrl+a", *'print("Hello, explorer!")', "enter", *"print(6 * 7)"
        )
        await pilot.press("f5")
        await until(pilot, lambda: not app.screen.running)
        assert "BUILD PASSED" in str(app.screen.query_one("#results", Static).content)
        await pilot.press("f7", "home", "down", "enter")
        await pilot.pause()
        assert app.store.status(LESSONS[0]) != "completed"
        await pilot.press(
            "ctrl+n", "ctrl+a", *'print("Hello, explorer!")', "enter", *"print(6 * 7)"
        )
        await pilot.press("f5")
        await until(pilot, lambda: not app.screen.running)
        assert app.store.status(LESSONS[0]) == "completed"
        await pilot.press("ctrl+n")
        await pilot.pause()
        assert app.screen.lesson.id == "names-and-voices"
        await pilot.press("ctrl+t", "ctrl+a")
        for index, line in enumerate(BY_ID["names-and-voices"].solution.splitlines()):
            if index:
                await pilot.press("enter")
            await pilot.press(*line)
        await pilot.press("ctrl+r")
        await until(pilot, lambda: app.screen.console and app.screen.console.waiting)
        assert app.focused.id == "console-input"
        assert "What is your name?" in str(app.screen.query_one("#results", Static).content)
        await pilot.press(*"Renée Chen", "enter")
        await until(pilot, lambda: not app.screen.running)
        assert "Welcome, Renée Chen!" in str(app.screen.query_one("#results", Static).content)
        await pilot.press("f5")
        await until(pilot, lambda: not app.screen.running)
        assert app.screen.query_one("#console-input", Input).is_disabled
        await pilot.press("f7", "home", "down", "enter")
        await pilot.pause()
        assert app.store.status(BY_ID["names-and-voices"]) != "completed"
        await pilot.press("ctrl+n", "ctrl+a")
        for index, line in enumerate(BY_ID["names-and-voices"].solution.splitlines()):
            if index:
                await pilot.press("enter")
            await pilot.press(*line)
        await pilot.press("f5")
        await until(pilot, lambda: not app.screen.running)
        assert app.store.status(BY_ID["names-and-voices"]) == "completed"
        await pilot.press("ctrl+b")
        await pilot.pause()
        assert isinstance(app.screen, Dashboard)


async def test_custom_path_selection_and_revisit_are_keyboard_accessible(tmp_path):
    app = TutorApp(tmp_path)
    async with app.run_test(size=(100, 35)) as pilot:
        await pilot.press("enter", "end", "enter")
        await pilot.pause()
        assert app.screen.query_one("#path", Select).value == "custom"
        assert "Build distributable tools" in str(
            app.screen.query_one("#path-topics", Static).content
        )
        await tab_to(pilot, app, "onboarding-concepts")
        await pilot.press("home", "space", "f5")
        await pilot.pause()
        assert app.store.status(LESSONS[0]) == "familiar"
        await pilot.press("c")
        await pilot.pause()
        assert app.screen.lesson.id == "names-and-voices"
        await pilot.press("ctrl+b")
        await pilot.pause()
        await tab_to(pilot, app, "lesson-list")
        await pilot.press("home", "enter")
        await pilot.pause()
        assert app.screen.lesson.id == "first-light"
        await pilot.press("f6")
        assert app.screen.active_pane == "editor"
        await pilot.press("shift+f6")
        assert app.screen.active_pane == "lesson"


async def test_restart_cancels_or_erases_without_autosave_resurrection(tmp_path):
    app = TutorApp(tmp_path)
    app.store.data.update({"onboarded": True, "last_lesson": "names-and-voices"})
    app.store.entry(LESSONS[0])["completed"] = True
    async with app.run_test(size=(100, 35)) as pilot:
        await pilot.press("c", "ctrl+t", "ctrl+a", *'input("Ready? ")')
        await pilot.press("ctrl+r")
        await until(pilot, lambda: app.screen.console and app.screen.console.waiting)
        await command(pilot, "Start over")
        assert isinstance(app.screen, ConfirmRestart)
        await pilot.press("enter")  # The safe default is Keep my progress.
        await pilot.pause()
        assert app.store.status(LESSONS[0]) == "completed"
        await command(pilot, "Start over")
        await pilot.press("tab", "enter")
        await pilot.pause(0.7)
        assert isinstance(app.screen, Onboarding)
        assert not app.store.data["onboarded"]
        assert app.store.data["lessons"] == {}
        assert app.store.data["familiar"] == []
        saved = json.loads((tmp_path / "profile.json").read_text())
        assert saved["lessons"] == {}
    resumed = TutorApp(tmp_path)
    async with resumed.run_test() as pilot:
        assert isinstance(resumed.screen, Onboarding)


async def test_console_eof_and_multiple_answers(tmp_path):
    app = TutorApp(tmp_path)
    app.store.data["onboarded"] = True
    async with app.run_test(size=(80, 24)) as pilot:
        await pilot.press("c")
        await pilot.pause()
        app.screen.query_one("#editor", TextArea).load_text(
            'first = input("First: ")\nsecond = input("Second: ")\nprint(first + second)\n'
        )
        await pilot.press("ctrl+r")
        await until(pilot, lambda: app.screen.console and app.screen.console.waiting)
        await pilot.press(*"one", "enter")
        await until(pilot, lambda: "Second:" in app.screen.transcript)
        await pilot.press(*"two", "enter")
        await until(pilot, lambda: not app.screen.running)
        assert "onetwo" in app.screen.transcript
        app.screen.query_one("#editor", TextArea).load_text(
            'import sys\nprint("Send lines; Ctrl+D finishes.")\nprint(len(list(sys.stdin)))\n'
        )
        await pilot.press("ctrl+r")
        await until(pilot, lambda: app.screen.console and app.screen.console.waiting)
        await pilot.press(*"first", "enter", *"second", "enter", "ctrl+d")
        await until(pilot, lambda: not app.screen.running)
        assert "\n2\n" in app.screen.transcript
        Path(".artifacts").mkdir(exist_ok=True)
        app.save_screenshot("console-80.svg", ".artifacts")


async def test_revised_exercise_preserves_existing_draft(tmp_path):
    app = TutorApp(tmp_path)
    app.store.data.update({"onboarded": True, "last_lesson": "choose-a-door"})
    app.store.entry(BY_ID["choose-a-door"])["code"] = 'def door(key):\n    return "locked"\n'
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.press("c")
        await pilot.pause()
        assert app.screen.query("#updated-notice")
        assert "def door" in app.screen.query_one("#editor", TextArea).text
        await command(pilot, "Reset exercise")
        await pilot.press("enter")
        await pilot.pause()
        assert "def " not in app.screen.query_one("#editor", TextArea).text
        assert "def door" in next((tmp_path / "exports").glob("*.py")).read_text()
