import json
from dataclasses import replace
from datetime import UTC, datetime, timedelta

import pytest

from pytuitor.curriculum import LESSONS
from pytuitor.models import Review
from pytuitor.state import ProfileError, Store


def test_version_two_migration_backs_up_original_and_preserves_stage_drafts(tmp_path):
    profile = {
        "version": 2,
        "onboarded": True,
        "track": "beginner",
        "familiar": [],
        "lessons": {
            "first-light": {
                "code": "# build",
                "repair": {"code": "# repair"},
                "stage": "repair",
                "completed": True,
            }
        },
    }
    raw = json.dumps(profile)
    (tmp_path / "profile.json").write_text(raw)
    store = Store(tmp_path)
    assert store.data["version"] == 3
    assert store.data["lessons"] == profile["lessons"]
    store.save()
    assert (tmp_path / "profile-before-v3.json").read_text() == raw
    store.close()


def test_review_is_optional_local_and_spaced(tmp_path):
    store = Store(tmp_path)
    project = replace(LESSONS[0], review=Review("Practice", "", ()))
    store.schedule_review(project)
    first = store.data["reviews"][project.id]
    assert first["level"] == 0
    assert datetime.fromisoformat(first["due"]) > datetime.now(UTC)
    next_before = store.next_lesson()
    store.schedule_review(replace(project, review_of=project.id), practiced=True)
    second = store.data["reviews"][project.id]
    assert second["level"] == 1
    assert datetime.fromisoformat(second["due"]) > datetime.fromisoformat(first["due"]) + timedelta(
        days=1
    )
    assert store.next_lesson() == next_before
    store.close()


def test_feedback_is_opt_in_and_export_omits_source_and_input(tmp_path):
    store = Store(tmp_path)
    lesson = LESSONS[0]
    store.entry(lesson).update(code="SECRET", input="PRIVATE")
    store.record_feedback(lesson, "hint", "build")
    assert store.data["feedback"] == []
    store.data["feedback_enabled"] = True
    store.record_feedback(lesson, "hint", "build")
    store.data["feedback"][0]["code"] = "INJECTED"
    exported = store.export_feedback().read_text()
    assert "hint" in exported
    assert all(
        secret not in exported for secret in ("SECRET", "PRIVATE", "INJECTED", str(tmp_path))
    )
    store.close()


@pytest.mark.parametrize(
    "schedule",
    [
        {"level": 0},
        {"level": 0, "due": "2026-01-01"},
        {"level": -1, "due": "2026-01-01T00:00:00+00:00"},
    ],
)
def test_malformed_review_profile_fails_without_modifying_data(tmp_path, schedule):
    store = Store(tmp_path)
    store.data["reviews"]["chapter"] = schedule
    store.save()
    store.close()
    before = (tmp_path / "profile.json").read_bytes()
    with pytest.raises(ProfileError):
        Store(tmp_path)
    assert (tmp_path / "profile.json").read_bytes() == before
