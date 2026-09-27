"""Real runner, persisted lineage, navigation, and learner-facing game journeys."""

import copy
import json
import subprocess
import sys

import pytest
from textual.widgets import Button, OptionList, TextArea

from pytuitor.app import TutorApp
from pytuitor.curriculum import ACTIVITIES, CHAPTERS, LESSONS, PRACTICE, chapter_activities
from pytuitor.project_catalog import BY_MILESTONE, MILESTONES
from pytuitor.project_screen import CheckpointPlayer, ProjectScreen
from pytuitor.project_workspace import ProjectError, ProjectWorkspace
from pytuitor.runner import execute
from pytuitor.state import Store
from pytuitor.workspace import WorkspaceError


async def checked_snapshot(workspace, milestone, *, files=None):
    entry = workspace.entry(milestone)
    files = dict(files or milestone.lesson.stage_contract("build").reference_files)
    entry.update(files=files, code=files[milestone.lesson.entrypoint])
    contract = workspace.contract(milestone, "build")
    result = await execute(
        milestone.lesson,
        files[milestone.lesson.entrypoint],
        contract.stdin,
        files=files,
        stage=contract,
    )
    assert result.passed, [
        (item["label"], item["actual"]) for item in result.checks if not item["passed"]
    ]
    return workspace.checkpoint(milestone, files, result.checks)


@pytest.mark.parametrize("milestone", MILESTONES, ids=lambda item: item.lesson.id)
async def test_every_game_contract_and_independent_repair(milestone):
    lesson = milestone.lesson
    for stage in ("build", "repair"):
        contract = lesson.stage_contract(stage)
        result = await execute(
            lesson,
            contract.reference_files[lesson.entrypoint],
            contract.stdin,
            files=contract.reference_files,
            stage=contract,
        )
        assert result.passed, (lesson.id, stage, result)
        if stage == "repair":
            broken = await execute(
                lesson,
                contract.starter_files[lesson.entrypoint],
                contract.stdin,
                files=contract.starter_files,
                stage=contract,
            )
            assert not broken.passed, lesson.id


def test_recommended_path_and_independent_specialties():
    assert len(LESSONS) == 87 and len(PRACTICE) == 12
    assert len(ACTIVITIES) == 96 and len(MILESTONES) == len(CHAPTERS) == 21
    assert len({item.lesson.id for item in MILESTONES}) == 21
    for chapter in CHAPTERS:
        units = chapter_activities(chapter.id)
        assert units[-1].project_id == "lantern-reach"
        assert all(not lesson.project for lesson in units[:-1])
    assert "scouts" not in BY_MILESTONE["reach-package"].requires
    assert "package" not in BY_MILESTONE["reach-formatters"].requires
    assert "actions" not in BY_MILESTONE["reach-chronicle"].requires


async def test_continuation_preserves_learner_source_and_personal_files(tmp_path):
    store = Store(tmp_path)
    workspace = ProjectWorkspace(store)
    first, second = MILESTONES[:2]
    files = dict(first.lesson.solution_files)
    # A distinct valid implementation and an extra creative file must survive.
    files["game.py"] = files["game.py"].replace("food * 3", "3 * food") + "\n# My expedition\n"
    files["journal.txt"] = "The valley smells of rain.\n"
    checkpoint = await checked_snapshot(workspace, first, files=files)
    initial = workspace.read_checkpoint(checkpoint["id"])
    next_entry = workspace.entry(second)
    assert next_entry["files"]["game.py"] == files["game.py"]
    assert next_entry["files"]["journal.txt"] == files["journal.txt"]
    assert next_entry["base_origin"] == "learner"
    assert next_entry["parent"] == checkpoint["id"]
    next_entry["files"]["game.py"] += "# Later edits\n"
    assert workspace.read_checkpoint(checkpoint["id"]) == initial
    assert not store.entry(first.lesson).get("completed")
    store.save()
    store.close()
    reopened = Store(tmp_path)
    assert reopened.entry(second.lesson)["files"]["journal.txt"] == files["journal.txt"]
    reopened.close()


async def test_supported_later_entry_and_reference_provenance(tmp_path):
    store = Store(tmp_path)
    workspace = ProjectWorkspace(store)
    milestone = BY_MILESTONE["reach-quests"]
    entry = workspace.entry(milestone)
    assert entry["base_origin"] == "supplied"
    assert entry["files"]["game.py"] == milestone.base_files["game.py"]
    checkpoint = await checked_snapshot(workspace, milestone)
    assert workspace.read_checkpoint(checkpoint["id"])["supported"]
    assert store.status(MILESTONES[0].lesson) == "new"
    first = workspace.entry(MILESTONES[0])
    first["solution_seen"] = True
    revealed = await checked_snapshot(workspace, MILESTONES[0])
    assert workspace.read_checkpoint(revealed["id"])["reference_seen"]
    store.close()


async def test_snapshot_integrity_and_explicit_recovery(tmp_path):
    store = Store(tmp_path)
    workspace = ProjectWorkspace(store)
    first = await checked_snapshot(workspace, MILESTONES[0])
    path = workspace.directory / (first["id"] + ".json")
    path.write_text('{"files": {}}')
    with pytest.raises(ProjectError, match="missing or damaged"):
        workspace.entry(MILESTONES[1])
    entry = workspace.start(MILESTONES[1], supplied=True)
    assert entry["base_origin"] == "supplied"
    assert store.entry(MILESTONES[0].lesson)["files"] == MILESTONES[0].lesson.solution_files
    with pytest.raises(ProjectError, match="identity"):
        workspace.read_checkpoint("../../profile")
    store.close()


async def test_checkpoint_pointer_rolls_back_when_profile_write_fails(tmp_path, monkeypatch):
    store = Store(tmp_path)
    workspace = ProjectWorkspace(store)
    milestone = MILESTONES[0]
    entry = workspace.entry(milestone)
    files = milestone.lesson.solution_files
    entry.update(files=dict(files), code=files["game.py"])
    before = copy.deepcopy(workspace.data)
    checks = [{"label": check.label, "passed": True} for check in milestone.lesson.checks]
    with monkeypatch.context() as patch:
        patch.setattr(store, "save", lambda: (_ for _ in ()).throw(OSError("disk full")))
        with pytest.raises(OSError, match="disk full"):
            workspace.checkpoint(milestone, files, checks)
    assert workspace.data == before
    result = workspace.checkpoint(milestone, files, checks)
    assert workspace.read_checkpoint(result["id"])["files"] == files
    # A repeated check on unchanged content does not inflate history.
    workspace.checkpoint(milestone, files, checks)
    assert len(workspace.data["checkpoints"]) == 1
    store.close()


async def test_replace_base_backs_up_both_stages_and_retains_checkpoints(tmp_path):
    store = Store(tmp_path)
    workspace = ProjectWorkspace(store)
    milestone = MILESTONES[1]
    checkpoint = await checked_snapshot(workspace, milestone)
    entry = workspace.entry(milestone)
    entry["repair"] = {"files": {"game.py": "# My unfinished repair\n"}}
    entry["stage"] = "repair"
    backup = workspace.replace_base(milestone)
    assert (backup / "extend/game.py").read_text() == milestone.lesson.solution
    assert (backup / "repair/game.py").read_text() == "# My unfinished repair\n"
    assert workspace.read_checkpoint(checkpoint["id"])["files"] == milestone.lesson.solution_files
    assert not workspace.entry(milestone).get("checked_revision")
    store.close()


def test_v3_migration_preserves_every_old_lesson_record(tmp_path):
    original = {
        "version": 3,
        "onboarded": True,
        "familiar": ["strings"],
        "last_lesson": "ticket-desk",
        "lessons": {
            "ticket-desk": {
                "files": {"lesson.py": "# unfinished\n"},
                "completed": True,
                "repair": {"files": {"lesson.py": "# old repair\n"}},
            }
        },
    }
    raw = json.dumps(original)
    (tmp_path / "profile.json").write_text(raw)
    store = Store(tmp_path)
    assert store.data["version"] == 4
    assert store.data["lessons"] == original["lessons"]
    assert store.data["projects"] == {}
    store.save()
    assert (tmp_path / "profile-before-v4.json").read_text() == raw
    store.close()


def test_current_revision_required_for_automatic_continuation(tmp_path):
    store = Store(tmp_path)
    workspace = ProjectWorkspace(store)
    first, second = MILESTONES[:2]
    workspace.data["checkpoints"] = [
        {
            "id": "a" * 64,
            "milestone": first.lesson.id,
            "revision": 0,
            "capabilities": list(first.provides),
        }
    ]
    assert workspace.compatible(second) == []
    assert workspace.entry(second)["base_origin"] == "supplied"
    store.close()


async def test_optional_capabilities_cannot_be_silently_dropped(tmp_path):
    store = Store(tmp_path)
    workspace = ProjectWorkspace(store)
    await checked_snapshot(workspace, BY_MILESTONE["reach-actions"])
    streaming = BY_MILESTONE["reach-chronicle"]
    entry = workspace.entry(streaming)
    assert "actions" in entry["base_capabilities"]
    contract = workspace.contract(streaming, "build")
    assert any("Recording preserves" in check.label for check in contract.checks)
    # Replacing the learner's richer source with a narrower reference loses real features.
    files = streaming.lesson.solution_files
    result = await execute(
        streaming.lesson, files["game.py"], "quit\n", files=files, stage=contract
    )
    assert not result.passed
    store.close()


@pytest.mark.parametrize("size", [(80, 24), (140, 44)], ids=["small", "wide"])
async def test_game_ui_checkpoint_repair_history_and_resume(tmp_path, size):
    app = TutorApp(tmp_path)
    app.store.data["onboarded"] = True
    first = MILESTONES[0]
    async with app.run_test(size=size) as pilot:
        await pilot.press("g")
        await pilot.pause()
        assert isinstance(app.screen, ProjectScreen)
        assert app.store.data["last_lesson"] is None
        await pilot.press("enter")
        await pilot.pause()
        screen = app.screen
        assert screen.lesson.id == first.lesson.id
        assert "Extend" in str(screen.query_one("#stage-build", Button).label)
        screen.query_one("#editor", TextArea).load_text(first.lesson.solution)
        await pilot.press("f5")
        await app.workers.wait_for_complete()
        assert screen.stage_passed("build")
        checkpoint = ProjectWorkspace(app.store).data["checkpoints"][0]
        await pilot.press("ctrl+n")
        await pilot.pause()
        assert screen.stage == "repair"
        assert screen.project_files() != first.lesson.solution_files
        screen.query_one("#editor", TextArea).load_text(
            first.lesson.repair_stage.reference_files["game.py"]
        )
        await pilot.press("f5")
        await app.workers.wait_for_complete()
        assert app.store.status(first.lesson) == "completed"
        await pilot.press("ctrl+b", "g")
        await pilot.pause()
        app.screen.history()
        await pilot.pause()
        history = app.screen
        assert history.query_one("#checkpoint-list", OptionList).option_count == 1
        history.play()
        await pilot.pause()
        assert isinstance(app.screen, CheckpointPlayer)
        app.screen.action_close()
        await pilot.pause()
        history.action_close()
        await pilot.pause()
        overview = app.screen
        overview.selected = MILESTONES[1]
        overview.open_milestone()
        await pilot.pause()
        second = app.screen
        assert second.project_files()["game.py"] == first.lesson.solution
        assert app.store.entry(second.lesson)["parent"] == checkpoint["id"]
        second.select_pane("editor")
        await pilot.pause()
        assert second.query_one("#editor").region.height >= 5
        assert second.query_one("#editor").region.right <= size[0]
    reopened = Store(tmp_path)
    assert reopened.next_lesson().id == MILESTONES[1].lesson.id
    reopened.close()


async def test_exported_core_game_runs_without_tutor(tmp_path):
    store = Store(tmp_path / "profile")
    workspace = ProjectWorkspace(store)
    milestone = BY_MILESTONE["reach-beacon"]
    checkpoint = await checked_snapshot(workspace, milestone)
    destination = workspace.export_checkpoint(checkpoint["id"], tmp_path / "export café")
    result = subprocess.run(
        [
            sys.executable,
            "-I",
            "-c",
            "import runpy,sys;sys.path.insert(0,'.');runpy.run_path('game.py',run_name='__main__')",
        ],
        input="forest\ngather\ngather\noutpost\ndeliver\nbeacon\nsave\nquit\n",
        text=True,
        capture_output=True,
        cwd=destination,
        timeout=15,
    )
    assert result.returncode == 0, result.stderr
    assert "The beacon shines. Lantern Reach is home again." in result.stdout
    assert json.loads((destination / "save.json").read_text())["beacon"] is True
    manifest = json.loads((destination / "pytuitor-checkpoint.json").read_text())
    assert manifest["snapshot"] == checkpoint["id"]
    with pytest.raises(WorkspaceError):
        workspace.export_checkpoint(checkpoint["id"], destination)
    store.close()


async def test_complete_cumulative_game_keeps_all_optional_features_and_exports(tmp_path):
    from lantern_reference_journey import reference_history

    store = Store(tmp_path / "profile")
    workspace = ProjectWorkspace(store)
    previous = None
    for milestone, files in reference_history():
        entry = workspace.entry(milestone)
        if previous:
            assert entry["parent"] == previous["id"]
            assert entry["files"]["my-trail.txt"].startswith("A personal detail")
        previous = await checked_snapshot(workspace, milestone, files=files)
        assert workspace.read_checkpoint(previous["id"])["files"] == files
    payload = workspace.read_checkpoint(previous["id"])
    assert len(payload["capabilities"]) == 21
    destination = workspace.export_checkpoint(previous["id"], tmp_path / "complete-game")
    commands = (
        "help\nhelp oren\nforest\ngather\ngather\ngather\ngather\ngather\n"
        "outpost\ndeliver\nhelp tess\nbeacon\nstatus\n"
        "branch\ncaves\nactions\nchronicle\nstation\nrecords\nstores\nscouts\nformatters\nquit\n"
    )
    result = subprocess.run(
        [sys.executable, "-m", "lantern_reach", "--name", "Zoë"],
        input=commands,
        text=True,
        capture_output=True,
        cwd=destination,
        timeout=15,
    )
    assert result.returncode == 0, result.stderr
    for expected in (
        "Lantern Reach | Zoë",
        "Tess builds the outpost storehouse.",
        "Buildings: storehouse",
        "Beacon: lit",
        "entrance, pool, crystal chamber",
        "ridge: survey",
        "Mira waits by the beacon.",
        "return route preserved",
        "forest clear, ridge clear",
        "Trail: The beacon shines.",
    ):
        assert expected in result.stdout, (expected, result.stdout)
    store.close()


def test_every_teaching_lesson_has_a_specific_game_connection():
    from pytuitor.content.lantern.connections import GAME_CONNECTIONS

    assert set(GAME_CONNECTIONS) == {lesson.id for lesson in LESSONS if not lesson.project}
    practice_ids = {lesson.id for lesson in PRACTICE}
    assert all(not practice_ids.intersection(item.lesson.prerequisites) for item in MILESTONES)


async def test_game_history_exports_full_workspace_at_file_limit(tmp_path):
    app = TutorApp(tmp_path)
    app.store.data["onboarded"] = True
    workspace = ProjectWorkspace(app.store)
    milestone = MILESTONES[0]
    files = dict(milestone.lesson.solution_files)
    files.update({f"notes/{index}.txt": "Personal story detail" for index in range(31)})
    await checked_snapshot(workspace, milestone, files=files)
    async with app.run_test(size=(80, 24)) as pilot:
        await pilot.press("g")
        app.screen.history()
        await pilot.pause()
        app.screen.export()
        from textual.widgets import Static

        feedback = str(app.screen.query_one("#checkpoint-feedback", Static).content)
        assert feedback.startswith("Exported to "), feedback
        assert len(list((tmp_path / "exports").rglob("*.txt"))) == 31


def test_base_backup_handles_two_full_workspaces(tmp_path):
    store = Store(tmp_path)
    workspace = ProjectWorkspace(store)
    milestone = MILESTONES[1]
    entry = workspace.entry(milestone)
    entry["files"].update({f"{index}.txt": "extend" for index in range(31)})
    entry["repair"] = {"files": {f"{index}.txt": "repair" for index in range(32)}}
    destination = workspace.replace_base(milestone)
    assert len(list((destination / "extend").rglob("*.*"))) == 32
    assert len(list((destination / "repair").rglob("*.*"))) == 32
    store.close()


async def test_restore_from_active_editor_preserves_attempt_and_stops_old_autosave(tmp_path):
    app = TutorApp(tmp_path)
    app.store.data["onboarded"] = True
    workspace = ProjectWorkspace(app.store)
    first, second = MILESTONES[:2]
    checkpoint = await checked_snapshot(workspace, first)
    async with app.run_test(size=(80, 24)) as pilot:
        app.open_activity(second.lesson)
        await pilot.pause()
        editor = app.screen
        editor.query_one("#editor", TextArea).load_text("# An unfinished attempt\n")
        await pilot.pause()
        app.action_game()
        await pilot.pause()
        app.screen.history()
        await pilot.pause()
        app.screen.restore()
        app.screen.restore()
        await pilot.pause()
        assert editor.suspend_saves
        restored = workspace.entry(second)
        assert restored["parent"] == checkpoint["id"]
        assert restored["base_origin"] == "restored"
        assert restored["files"]["game.py"] == first.lesson.solution
        assert not restored.get("checked_revision")
        backup = next((tmp_path / "exports").glob("*/extend/game.py"))
        assert backup.read_text() == "# An unfinished attempt\n"
        app.screen.open_milestone()
        await pilot.pause()
        app.screen.save_draft()
        assert workspace.entry(second)["files"]["game.py"] == first.lesson.solution
        assert len(workspace.data["checkpoints"]) == 1


async def test_checkpoint_player_accepts_commands_and_cancels_cleanly(tmp_path):
    from textual.widgets import Input

    app = TutorApp(tmp_path)
    app.store.data["onboarded"] = True
    workspace = ProjectWorkspace(app.store)
    await checked_snapshot(workspace, MILESTONES[3])
    before = copy.deepcopy(workspace.data)
    async with app.run_test(size=(80, 24)) as pilot:
        await pilot.press("g")
        app.screen.history()
        await pilot.pause()
        history = app.screen
        history.play()
        await pilot.pause()
        player = app.screen
        for _ in range(50):
            if player.console.waiting:
                break
            await pilot.pause(0.02)
        assert player.console.waiting
        player.query_one("#checkpoint-input", Input).value = "forest"
        await pilot.press("enter")
        for _ in range(50):
            if "Location: forest" in player.transcript:
                break
            await pilot.pause(0.02)
        assert "Location: forest" in player.transcript
        await pilot.press("escape")
        await app.workers.wait_for_complete()
        assert app.screen is history
        assert workspace.data == before
