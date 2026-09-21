"""Exercise save and recovery through the same UI persistence entry point."""

import json
import os
import stat

import pytest
from textual.widgets import TextArea

from pytuitor.app import TutorApp
from pytuitor.curriculum import LESSONS


async def test_learner_save_syncs_file_then_directory(tmp_path, monkeypatch):
    app = TutorApp(tmp_path)
    app.store.data.update(onboarded=True, last_lesson=LESSONS[0].id)
    calls = []
    original = os.fsync

    def observe(descriptor):
        calls.append("directory" if stat.S_ISDIR(os.fstat(descriptor).st_mode) else "file")
        original(descriptor)

    async with app.run_test(size=(80, 24)) as pilot:
        await pilot.press("c")
        monkeypatch.setattr(os, "fsync", observe)
        app.screen.query_one("#editor", TextArea).load_text("# retained draft\n")
        app.screen.save_draft()
        if os.name == "nt":
            assert calls and set(calls) == {"file"}
        else:
            assert calls[-2:] == ["file", "directory"]
        assert json.loads(app.store.path.read_text())["lessons"][LESSONS[0].id]["code"] == (
            "# retained draft\n"
        )


@pytest.mark.skipif(os.name == "nt", reason="Windows uses write-through replacement")
def test_directory_sync_failure_does_not_undo_a_committed_reset(tmp_path, monkeypatch):
    from pytuitor.state import Store

    store = Store(tmp_path)
    store.entry(LESSONS[0])["code"] = "old draft"
    store.save()
    original = os.fsync

    def fail_directory(descriptor):
        if stat.S_ISDIR(os.fstat(descriptor).st_mode):
            raise OSError("directory sync unavailable")
        original(descriptor)

    monkeypatch.setattr(os, "fsync", fail_directory)
    store.reset()
    assert store.data["lessons"] == {}
    assert json.loads(store.path.read_text())["lessons"] == {}
    assert "could not be synced" in store.durability_warning
    store.close()
