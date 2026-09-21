"""Reviewed SVG baselines from the real Textual renderer, with fixed cursor state."""

import os
import re
from pathlib import Path

import pytest
from textual.widgets import Button, Static, TextArea

from pytuitor.app import TutorApp
from pytuitor.curriculum import BY_ID

BASELINES = Path(__file__).with_name("visuals")


async def capture(app, pilot, name):
    for editor in app.screen.query(TextArea):
        editor.cursor_blink = False
    await pilot.pause()
    for screen in app.screen_stack:
        if hasattr(screen, "save_draft"):
            screen.save_draft()
    await pilot.pause()
    screenshot = re.sub(
        r"terminal-\d+", "terminal-baseline", app.export_screenshot(title="Pytuitor")
    )
    screenshot = "\n".join(line.rstrip() for line in screenshot.splitlines()) + "\n"
    target = BASELINES / f"{name}.svg"
    if os.environ.get("PYTUITOR_UPDATE_VISUALS") == "1":
        BASELINES.mkdir(exist_ok=True)
        target.write_text(screenshot, encoding="utf-8")
    assert target.exists(), "Generate and inspect the visual baseline before accepting it."
    if target.read_text(encoding="utf-8") != screenshot:
        actual = Path(".artifacts") / f"{name}-actual.svg"
        actual.parent.mkdir(exist_ok=True)
        actual.write_text(screenshot, encoding="utf-8")
        pytest.fail(f"Visual changed: compare {target} with {actual}")


@pytest.mark.parametrize("size", [(80, 24), (140, 44)])
async def test_integrated_learning_visuals(tmp_path, monkeypatch, size):
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.setenv("TERM", "xterm-256color")
    monkeypatch.setenv("COLORTERM", "truecolor")
    app = TutorApp(tmp_path)
    lesson = BY_ID["first-light"]
    app.store.data.update(onboarded=True, last_lesson=lesson.id)
    async with app.run_test(size=size) as pilot:
        await pilot.press("c")
        screen = app.screen
        await capture(app, pilot, f"{size[0]}-teaching")
        screen.query_one("#editor", TextArea).load_text(lesson.solution)
        await pilot.press("f5")
        await app.workers.wait_for_complete()
        assert "Next:" in str(screen.query_one("#check-summary", Static).content)
        await capture(app, pilot, f"{size[0]}-check-next")
        await pilot.press("ctrl+n")
        assert screen.query_one("#editor", TextArea).region.height >= 5
        await capture(app, pilot, f"{size[0]}-repair")
        before = screen.capture_editor()
        screen.action_solution()
        await pilot.pause()
        app.screen.query_one("#compare-solution", Button).active_effect_duration = 0
        await pilot.click("#compare-solution")
        assert app.screen.query_one("#solution-code", TextArea).region.height >= 6
        await capture(app, pilot, f"{size[0]}-comparison")
        await pilot.press("escape")
        assert screen.capture_editor() == before
        await pilot.press("ctrl+b")
        app.screen.open_lesson(BY_ID["notes-archiver"])
        await pilot.pause()
        screen = app.screen
        await pilot.press("f4")
        assert screen.focused.id == "exercise-scroll"
        await capture(app, pilot, f"{size[0]}-long-contract")
        panel = screen.query_one("#exercise-scroll")
        assert panel.max_scroll_y > 0
        await pilot.press("end")
        await pilot.pause()
        assert panel.scroll_y > 0
        assert panel.max_scroll_x == 0
        assert screen.query_one("#editor", TextArea).region.height >= 5
