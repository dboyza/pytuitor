from collections import Counter

from pytuitor.curriculum import CHAPTERS, CONCEPTS, LESSONS


def test_catalog_has_complete_chapters_and_ordered_prerequisites():
    assert len(LESSONS) == len({lesson.id for lesson in LESSONS}) == 60
    assert sum(lesson.project for lesson in LESSONS) == 12
    assert Counter(lesson.track for lesson in LESSONS) == {"beginner": 30, "experienced": 30}
    assert len(CHAPTERS) == 12
    seen = set()
    for lesson in LESSONS:
        assert set(lesson.prerequisites) <= seen, lesson.id
        assert lesson.body.strip() and lesson.checks and lesson.hints
        assert lesson.entrypoint in lesson.files
        assert set(lesson.concepts) <= set(CONCEPTS)
        seen.add(lesson.id)
    for chapter in CHAPTERS:
        units = [lesson for lesson in LESSONS if lesson.chapter_id == chapter.id]
        assert len(units) == 5
        assert sum(lesson.project for lesson in units) == 1
        assert units[-1].project
