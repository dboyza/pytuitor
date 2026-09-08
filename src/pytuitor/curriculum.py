"""Course catalog; authored paths are separate from UI and execution."""

from pytuitor.beginner_course import CHAPTERS as BEGINNER_CHAPTERS
from pytuitor.beginner_course import LESSONS as BEGINNER_LESSONS
from pytuitor.experienced_course import CHAPTERS as EXPERIENCED_CHAPTERS
from pytuitor.experienced_course import LESSONS as EXPERIENCED_LESSONS
from pytuitor.legacy import LESSONS as LEGACY_LESSONS
from pytuitor.legacy import default_input as legacy_input
from pytuitor.models import Check as Check
from pytuitor.models import Lesson as Lesson

LESSONS = (*BEGINNER_LESSONS, *EXPERIENCED_LESSONS)
CHAPTERS = (*BEGINNER_CHAPTERS, *EXPERIENCED_CHAPTERS)

BY_ID = {lesson.id: lesson for lesson in (*LEGACY_LESSONS, *LESSONS)}
CONCEPTS = tuple(
    dict.fromkeys(c for lesson in LESSONS if not lesson.project for c in lesson.concepts)
)
TRACKS = {"beginner": "Beginner", "experienced": "Experienced", "custom": "Custom"}


def track_lessons(track: str) -> list[Lesson]:
    return [lesson for lesson in LESSONS if track == "custom" or lesson.track == track]


def track_chapters(track: str):
    return [chapter for chapter in CHAPTERS if track == "custom" or chapter.track == track]


def default_input(lesson: Lesson) -> str:
    return lesson.stdin or legacy_input(lesson)
