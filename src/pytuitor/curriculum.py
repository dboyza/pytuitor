"""Unified course catalog; authoring provenance does not determine navigation."""

from dataclasses import replace

from pytuitor.beginner_course import CHAPTERS as BEGINNER_CHAPTERS
from pytuitor.beginner_course import LESSONS as BEGINNER_LESSONS
from pytuitor.course_map import CHAPTER_UNITS, PROJECT_PREPARATION
from pytuitor.course_map import CHAPTERS as CHAPTERS
from pytuitor.course_map import SECTIONS as SECTIONS
from pytuitor.experienced_course import CHAPTERS as EXPERIENCED_CHAPTERS
from pytuitor.experienced_course import LESSONS as EXPERIENCED_LESSONS
from pytuitor.legacy import LESSONS as LEGACY_LESSONS
from pytuitor.legacy import default_input as legacy_input
from pytuitor.models import Check as Check
from pytuitor.models import Lesson as Lesson

_AUTHORED_LESSONS = (*BEGINNER_LESSONS, *EXPERIENCED_LESSONS)
_AUTHORED_BY_ID = {lesson.id: lesson for lesson in _AUTHORED_LESSONS}


def _assemble_lessons() -> tuple[Lesson, ...]:
    units = []
    for chapter in CHAPTERS:
        previous = tuple(CHAPTER_UNITS[item][-1] for item in chapter.prerequisites)
        for identifier in CHAPTER_UNITS[chapter.id]:
            authored = _AUTHORED_BY_ID[identifier]
            preparation = PROJECT_PREPARATION.get(identifier)
            concepts = (
                tuple(
                    dict.fromkeys(
                        concept
                        for item in preparation
                        for concept in _AUTHORED_BY_ID[item].concepts
                    )
                )
                if preparation
                else authored.concepts
            )
            units.append(
                replace(
                    authored,
                    chapter_id=chapter.id,
                    prerequisites=preparation or previous,
                    concepts=concepts,
                )
            )
            previous = (identifier,)
    return tuple(units)


LESSONS = _assemble_lessons()

BY_ID = {lesson.id: lesson for lesson in (*LEGACY_LESSONS, *LESSONS)}
CONCEPTS = tuple(
    dict.fromkeys(c for lesson in LESSONS if not lesson.project for c in lesson.concepts)
)
TRACKS = {"beginner": "Beginner", "experienced": "Experienced", "custom": "Custom"}


def track_lessons(track: str) -> list[Lesson]:
    """Legacy authoring provenance, retained for imports and old profile tools."""
    return [lesson for lesson in _AUTHORED_LESSONS if track == "custom" or lesson.track == track]


def track_chapters(track: str):
    """Legacy authoring chapters; use CHAPTERS for learner navigation."""
    return [
        chapter
        for chapter in (*BEGINNER_CHAPTERS, *EXPERIENCED_CHAPTERS)
        if track == "custom" or chapter.track == track
    ]


def chapter_lessons(chapter_id: str) -> list[Lesson]:
    return [lesson for lesson in LESSONS if lesson.chapter_id == chapter_id]


def default_input(lesson: Lesson) -> str:
    return lesson.stdin or legacy_input(lesson)
