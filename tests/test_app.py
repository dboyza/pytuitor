from pathlib import Path

import pytest
from textual.widgets import Button, OptionList, Select, SelectionList, Static, TextArea

from pytuitor.app import TutorApp
from pytuitor.curriculum import BY_ID, LESSONS
from pytuitor.dialogs import KeyboardHelp
from pytuitor.screens import Dashboard, LessonScreen, Onboarding


async def wait_for_run(pilot, screen):
    for _ in range(150):
        await pilot.pause(0.05)
        if not screen.running:
            return
    raise AssertionError("Execution did not finish")


async def test_beginner_journey_and_resume(tmp_path):
    app = TutorApp(tmp_path)
    async with app.run_test(size=(120, 40)) as pilot:
        assert isinstance(app.screen, Onboarding)
        app.screen.query_one("#begin").scroll_visible(animate=False)
        await pilot.pause()
        await pilot.click("#begin")
        await pilot.pause()
        screen = app.screen
        assert isinstance(screen, LessonScreen)
        editor = screen.query_one("#editor", TextArea)
        # Build begins blank; checks explain what the learner still needs to implement.
        await pilot.click("#check")
        await wait_for_run(pilot, screen)
        assert "Expected" in str(screen.query_one("#results", Static).content)
        editor.focus()
        await pilot.press("ctrl+a")
        await pilot.press(*'print("Welcome, explorer!")', "enter", *"print(8 + 5)")
        await pilot.press("f5")
        await wait_for_run(pilot, screen)
        assert "BUILD PASSED" in str(screen.query_one("#results", Static).content)
        choices = screen.query_one("#prediction-choices", OptionList)
        choices.scroll_visible(animate=False)
        choices.focus()
        await pilot.press("home", "down", "enter")
        await pilot.pause()
        assert not app.store.entry(LESSONS[0]).get("completed")
        await pilot.press("ctrl+n")
        await pilot.pause()
        assert screen.stage == "repair"
        repair = LESSONS[0].stage_contract("repair")
        editor.load_text(repair.reference_files[LESSONS[0].entrypoint])
        await pilot.press("f5")
        await wait_for_run(pilot, screen)
        assert app.store.entry(LESSONS[0])["completed"]
        await pilot.click("#next")
        await pilot.pause()
        assert app.screen.lesson.id == "names-and-voices"
        app.screen.query_one("#editor", TextArea).load_text("# A draft I want to keep\n")
        await pilot.press("ctrl+b")
        await pilot.pause()
        assert isinstance(app.screen, Dashboard)
    app.store.close()
    resumed = TutorApp(tmp_path)
    async with resumed.run_test(size=(120, 40)) as pilot:
        assert isinstance(resumed.screen, Dashboard)
        await pilot.click("#continue")
        await pilot.pause()
        assert resumed.screen.lesson.id == "names-and-voices"
        assert resumed.screen.query_one("#editor", TextArea).text == "# A draft I want to keep\n"


async def test_known_topics_skip_and_revisit(tmp_path):
    app = TutorApp(tmp_path)
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.click("#browse-syllabus")
        await pilot.pause()
        await pilot.press("escape")
        await pilot.click("#preferences")
        await pilot.pause()
        known = LESSONS[0]
        for concept in known.concepts:
            app.screen.query_one("#onboarding-concepts", SelectionList).select(concept)
        await pilot.press("f5")
        await pilot.pause()
        assert isinstance(app.screen, Dashboard)
        await pilot.click("#continue")
        await pilot.pause()
        assert app.screen.lesson.id == LESSONS[1].id
        await pilot.press("ctrl+b")
        await pilot.pause()
        listing = app.screen.query_one("#lesson-list", OptionList)
        listing.focus()
        await pilot.press("home", "enter")
        await pilot.pause()
        assert app.screen.lesson.id == known.id
        assert app.store.status(app.screen.lesson) == "familiar"


async def test_small_terminal_and_visual_artifacts(tmp_path):
    app = TutorApp(tmp_path)
    artifacts = Path(".artifacts")
    artifacts.mkdir(exist_ok=True)
    async with app.run_test(size=(80, 24)) as pilot:
        app.save_screenshot("onboarding-80.svg", str(artifacts))
        app.screen.query_one("#begin").scroll_visible(animate=False)
        await pilot.pause()
        await pilot.click("#begin")
        await pilot.pause()
        assert app.screen.active_pane == "lesson"
        await pilot.press("ctrl+b")
        await pilot.pause()
        app.save_screenshot("dashboard-80.svg", str(artifacts))
        await pilot.click("#continue")
        await pilot.pause()
        app.save_screenshot("reading-80.svg", str(artifacts))
        await pilot.press("ctrl+t")
        await pilot.pause()
        assert app.screen.query_one("#editor").region.width >= 70
        assert app.screen.query_one("#editor").region.height >= 5
        app.save_screenshot("lesson-80.svg", str(artifacts))
        await pilot.press("ctrl+t", "ctrl+t")
        await pilot.pause()
        assert app.screen.query_one("#reading-panel").display
        await pilot.press("ctrl+t")
        await pilot.resize_terminal(140, 44)
        await pilot.pause()
        app.save_screenshot("lesson-140.svg", str(artifacts))
        await pilot.press("ctrl+b")
        await pilot.pause()
        app.save_screenshot("dashboard-140.svg", str(artifacts))


async def test_reset_backup_and_cancel(tmp_path):
    app = TutorApp(tmp_path)
    app.store.data["onboarded"] = True
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.click("#continue")
        await pilot.pause()
        screen = app.screen
        screen.query_one("#editor", TextArea).load_text("# valuable draft\n")
        screen.action_reset()
        await pilot.pause()
        await pilot.click("#cancel")
        await pilot.pause()
        assert screen.query_one("#editor", TextArea).text == "# valuable draft\n"
        screen.action_reset()
        await pilot.pause()
        await pilot.click("#confirm-reset")
        await pilot.pause()
        assert screen.query_one("#editor", TextArea).text == LESSONS[0].starter
        assert list((tmp_path / "exports").glob("*.py"))[0].read_text() == "# valuable draft\n"
        assert screen.query_one("#next", Button).disabled


async def test_known_topics_preferences_preserve_selection(tmp_path):
    app = TutorApp(tmp_path)
    async with app.run_test(size=(100, 35)) as pilot:
        await pilot.press("f5")
        await pilot.pause()
        assert isinstance(app.screen, LessonScreen)
        await pilot.press("ctrl+b")
        await pilot.pause()
        await pilot.click("#preferences")
        await pilot.pause()
        assert isinstance(app.screen, Onboarding)
        concepts = app.screen.query_one("#onboarding-concepts", SelectionList)
        concepts.select("Identity & mutability")
        await pilot.press("f5")
        await pilot.pause()
        assert isinstance(app.screen, Dashboard)
        assert app.store.status(BY_ID["objects-not-boxes"]) == "familiar"
        await pilot.click("#preferences")
        await pilot.pause()
        assert (
            "Identity & mutability"
            in app.screen.query_one("#onboarding-concepts", SelectionList).selected
        )
        await pilot.press("escape")
        await pilot.pause()
        assert isinstance(app.screen, Dashboard)


@pytest.mark.parametrize("lesson_id", ["lantern-quest", "signal-from-noise"])
async def test_capstone_run_check_and_export(tmp_path, lesson_id):
    app = TutorApp(tmp_path)
    app.store.data["onboarded"] = True
    lesson = BY_ID[lesson_id]
    app.store.data["track"] = lesson.track
    async with app.run_test(size=(120, 40)) as pilot:
        app.screen.query_one("#chapter-picker", Select).value = lesson.chapter_id
        await pilot.pause()
        options = app.screen.query_one("#lesson-list", OptionList)
        options.focus()
        await pilot.press("end")
        await pilot.press("enter")
        await pilot.pause()
        screen = app.screen
        assert screen.lesson.id == lesson_id
        screen.query_one("#editor", TextArea).load_text(
            lesson.stage_contract(screen.stage).reference_files[lesson.entrypoint]
        )
        await pilot.press("f5")
        await wait_for_run(pilot, screen)
        assert "BUILD PASSED" in str(screen.query_one("#results", Static).content)
        choices = screen.query_one("#prediction-choices", OptionList)
        choices.scroll_visible(animate=False)
        choices.focus()
        await pilot.press("home", *(["down"] * lesson.answer), "enter")
        await pilot.pause()
        assert app.store.status(lesson) != "completed"
        await pilot.press("ctrl+n")
        await pilot.pause()
        screen.query_one("#editor", TextArea).load_text(
            lesson.stage_contract(screen.stage).reference_files[lesson.entrypoint]
        )
        await pilot.press("f5")
        await wait_for_run(pilot, screen)
        assert app.store.status(lesson) == "completed"
        screen.action_export()
        assert (
            next((tmp_path / "exports").glob("*.py")).read_text()
            == lesson.stage_contract("repair").reference_files[lesson.entrypoint]
        )


async def test_stop_recovers_and_does_not_complete(tmp_path):
    app = TutorApp(tmp_path)
    app.store.data["onboarded"] = True
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.click("#continue")
        await pilot.pause()
        screen = app.screen
        screen.query_one("#editor", TextArea).load_text("while True: pass")
        await pilot.click("#run")
        await pilot.pause(0.1)
        await pilot.click("#stop")
        await wait_for_run(pilot, screen)
        assert "Stopped" in str(screen.query_one("#results", Static).content)
        assert not app.store.entry(LESSONS[0]).get("completed")
        screen.query_one("#editor", TextArea).load_text(LESSONS[0].solution)
        await pilot.press("f5")
        await wait_for_run(pilot, screen)
        assert "BUILD PASSED" in str(screen.query_one("#results", Static).content)


async def test_palette_export_and_dashboard_from_overlay(tmp_path):
    app = TutorApp(tmp_path)
    app.store.data["onboarded"] = True
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.click("#continue")
        await pilot.pause()
        await pilot.press("ctrl+p")
        await pilot.pause()
        await pilot.press(*"Export code")
        await pilot.pause(0.2)
        await pilot.press("enter")
        await pilot.pause()
        assert list((tmp_path / "exports").glob("*.py"))
        app.push_screen(KeyboardHelp())
        await pilot.pause()
        await pilot.press("ctrl+b")
        await pilot.pause()
        assert isinstance(app.screen, Dashboard)


async def test_editor_navigation_and_failed_save(tmp_path, monkeypatch):
    app = TutorApp(tmp_path)
    app.store.data["onboarded"] = True
    async with app.run_test(size=(120, 40)) as pilot:
        await pilot.click("#continue")
        await pilot.pause()
        editor = app.screen.query_one("#editor", TextArea)
        editor.focus()
        await pilot.press("escape", "tab")
        assert app.focused is not editor

        def fail_save():
            raise OSError("disk full")

        monkeypatch.setattr(app.store, "save", fail_save)
        app.screen.save_draft()
        assert str(app.screen.query_one("#save-status", Static).content) == "Not saved"
