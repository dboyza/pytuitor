from collections import Counter
from dataclasses import fields

from pytuitor.beginner_course import LESSONS as BEGINNER_LESSONS
from pytuitor.curriculum import CHAPTERS, CONCEPTS, LESSONS, SECTIONS, chapter_lessons
from pytuitor.experienced_course import LESSONS as EXPERIENCED_LESSONS
from pytuitor.models import Lesson


def test_catalog_has_complete_chapters_and_ordered_prerequisites():
    assert len(LESSONS) == len({lesson.id for lesson in LESSONS}) == 87
    assert sum(lesson.project for lesson in LESSONS) == 12
    assert Counter(lesson.track for lesson in LESSONS) == {"beginner": 46, "experienced": 41}
    assert len(CHAPTERS) == 21
    assert len(SECTIONS) == 5
    assert [section.optional for section in SECTIONS] == [False, False, False, True, True]
    seen = set()
    taught_concepts = set()
    for lesson in LESSONS:
        assert set(lesson.prerequisites) <= seen, lesson.id
        assert lesson.body.strip() and lesson.checks and lesson.hints
        assert lesson.entrypoint in lesson.files
        assert set(lesson.concepts) <= set(CONCEPTS)
        if lesson.project:
            assert set(lesson.concepts) <= taught_concepts
        else:
            taught_concepts.update(lesson.concepts)
        seen.add(lesson.id)
    seen_chapters = set()
    for chapter in CHAPTERS:
        units = chapter_lessons(chapter.id)
        assert 2 <= len(units) <= 6
        assert chapter.section_id in {section.id for section in SECTIONS}
        assert set(chapter.prerequisites) <= seen_chapters
        projects = [unit for unit in units if unit.project]
        assert len(projects) <= 1
        if projects:
            assert units[-1].project
        seen_chapters.add(chapter.id)
    assert tuple(unit for chapter in CHAPTERS for unit in chapter_lessons(chapter.id)) == LESSONS
    section_order = [section.id for section in SECTIONS]
    positions = [section_order.index(chapter.section_id) for chapter in CHAPTERS]
    assert positions == sorted(positions)


def test_reorganization_preserves_every_authored_exercise_contract():
    authored = {lesson.id: lesson for lesson in (*BEGINNER_LESSONS, *EXPERIENCED_LESSONS)}
    assert {lesson.id for lesson in LESSONS} == authored.keys()
    unchanged_fields = {field.name for field in fields(Lesson)} - {
        "chapter_id",
        "prerequisites",
        "concepts",
    }
    for lesson in LESSONS:
        for name in unchanged_fields:
            assert getattr(lesson, name) == getattr(authored[lesson.id], name), (lesson.id, name)


def test_specialties_have_relevant_independent_preparation():
    chapters = {chapter.id: chapter for chapter in CHAPTERS}
    assert "async-work" not in chapters["distributable-tools"].prerequisites
    assert "distributable-tools" not in chapters["python-machinery"].prerequisites
    assert "iterators-and-streaming" in chapters["exceptions-and-contexts"].prerequisites
    assert "decorators" in chapters["exceptions-and-contexts"].prerequisites
    assert "classes-and-tested-tools" in chapters["exceptions-and-contexts"].prerequisites
    optional = {section.id for section in SECTIONS if section.optional}
    for chapter in CHAPTERS:
        if chapter.section_id not in optional:
            assert all(chapters[item].section_id not in optional for item in chapter.prerequisites)
    assert not chapter_lessons("missing")
