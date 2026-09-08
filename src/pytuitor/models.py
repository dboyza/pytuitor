"""Authored curriculum, independent of the terminal interface."""

from dataclasses import dataclass
from importlib.resources import files
from textwrap import dedent


@dataclass(frozen=True)
class Check:
    label: str
    expression: str
    expected: object
    nudge: str
    stdin: str | None = None
    expected_output: str | None = None
    description: str = ""


@dataclass(frozen=True)
class Lesson:
    id: str
    track: str
    title: str
    subtitle: str
    minutes: int
    concepts: tuple[str, ...]
    body: str
    repair: str
    checks: tuple[Check, ...]
    hints: tuple[str, ...]
    prediction: str
    choices: tuple[str, ...]
    answer: int
    explanation: str
    solution: str
    project: bool = False
    revision: int = 3

    chapter_id: str = ""
    prerequisites: tuple[str, ...] = ()
    entrypoint: str = "lesson.py"
    files: tuple[str, ...] = ("lesson.py",)
    solution_files: dict[str, str] | None = None
    repair_files: dict[str, str] | None = None
    stdin: str = ""

    @property
    def starter(self) -> str:
        return ""


def lesson_text(lesson_id: str) -> str:
    return files("pytuitor").joinpath("lessons", f"{lesson_id}.md").read_text(encoding="utf-8")


def code(source: str) -> str:
    return dedent(source).strip() + "\n"


@dataclass(frozen=True)
class Chapter:
    id: str
    track: str
    title: str
    outcome: str
