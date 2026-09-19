"""Chapter-based continuation and compatibility with saved path profiles."""

import json

import pytest

from pytuitor.curriculum import BY_ID, CHAPTERS, LESSONS, SECTIONS, chapter_lessons
from pytuitor.state import Store


def finish(store, lessons):
    for lesson in lessons:
        store.entry(lesson)["completed"] = True


def test_new_profile_starts_at_foundations_without_path(tmp_path):
    store = Store(tmp_path)
    assert "track" not in store.data
    assert store.next_lesson() == LESSONS[0]
    store.save()
    store.close()
    restored = Store(tmp_path)
    assert "track" not in restored.data
    assert restored.next_lesson() == LESSONS[0]
    restored.close()


@pytest.mark.parametrize("old_track", ["beginner", "experienced", "custom"])
def test_saved_path_profile_resumes_same_chapter_with_both_drafts(tmp_path, old_track):
    lesson = BY_ID["data-models"]
    store = Store(tmp_path)
    store.data.update(track=old_track, onboarded=True, last_lesson=lesson.id)
    original = {"code": "# my build\n", "stage": "repair", "repair": {"code": "# my repair\n"}}
    store.data["lessons"][lesson.id] = original
    store.save()
    store.close()
    restored = Store(tmp_path)
    assert restored.next_lesson() == lesson
    assert restored.entry(lesson) == original
    finish(restored, [lesson])
    pending = restored.next_lesson()
    assert pending.chapter_id == lesson.chapter_id
    assert pending.id != LESSONS[0].id
    restored.save()
    restored.close()
    assert (
        json.loads((tmp_path / "profile.json").read_text())["lessons"][lesson.id]["repair"]
        == original["repair"]
    )


def test_continue_completes_active_chapter_before_later_chapters(tmp_path):
    store = Store(tmp_path)
    chapter = next(chapter for chapter in CHAPTERS if len(chapter_lessons(chapter.id)) >= 3)
    units = chapter_lessons(chapter.id)
    store.data["last_lesson"] = units[-1].id
    finish(store, [units[-1]])
    assert store.next_lesson() == units[0]
    store.set_familiar(list(units[0].concepts))
    assert store.next_lesson() == next(unit for unit in units if store.status(unit) == "new")
    store.close()


def test_core_completion_does_not_automatically_enter_optional_sections(tmp_path):
    store = Store(tmp_path)
    optional = {section.id for section in SECTIONS if section.optional}
    core_chapters = [chapter for chapter in CHAPTERS if chapter.section_id not in optional]
    finish(store, [lesson for chapter in core_chapters for lesson in chapter_lessons(chapter.id)])
    store.data["last_lesson"] = chapter_lessons(core_chapters[-1].id)[-1].id
    assert store.next_lesson() is None
    chosen = next(chapter for chapter in CHAPTERS if chapter.section_id in optional)
    first = chapter_lessons(chosen.id)[0]
    store.data["last_lesson"] = first.id
    assert store.next_lesson() == first
    store.close()


def test_optional_section_completion_waits_for_explicit_choice(tmp_path):
    store = Store(tmp_path)
    section = next(section for section in SECTIONS if section.optional)
    chapters = [chapter for chapter in CHAPTERS if chapter.section_id == section.id]
    units = [lesson for chapter in chapters for lesson in chapter_lessons(chapter.id)]
    finish(store, units)
    store.data["last_lesson"] = units[-1].id
    assert store.next_lesson() is None
    assert store.status(LESSONS[0]) == "new"
    store.close()


def test_missing_or_retired_resume_target_falls_back_to_core(tmp_path):
    store = Store(tmp_path)
    store.data["last_lesson"] = "no-longer-in-catalog"
    assert store.next_lesson() == LESSONS[0]
    store.close()


async def test_failed_next_save_keeps_completed_lesson_as_resume_anchor(tmp_path, monkeypatch):
    from textual.widgets import TextArea

    from pytuitor.app import TutorApp

    app = TutorApp(tmp_path)
    app.store.data["onboarded"] = True
    async with app.run_test(size=(80, 24)) as pilot:
        await pilot.press("c")
        await pilot.pause()
        screen = app.screen
        for stage in ("build", "repair"):
            contract = screen.lesson.stage_contract(stage)
            screen.query_one("#editor", TextArea).load_text(
                contract.reference_files[screen.lesson.entrypoint]
            )
            await pilot.press("f5")
            await app.workers.wait_for_complete()
            assert screen.stage_passed(stage)
            if stage == "build":
                await pilot.press("ctrl+n")
                await pilot.pause()
        monkeypatch.setattr(app, "persist", lambda: False)
        await pilot.press("ctrl+n")
        await pilot.pause()
        assert app.screen is screen
        assert app.store.data["last_lesson"] == screen.lesson.id
