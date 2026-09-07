"""Shared widgets and keyboard conventions."""

from typing import TYPE_CHECKING, cast

from textual.binding import ActiveBinding, Binding
from textual.containers import Horizontal
from textual.screen import Screen
from textual.widgets import Static, TextArea

if TYPE_CHECKING:
    from pytuitor.app import TutorApp


class TutorScreen(Screen):
    @property
    def active_bindings(self) -> dict[str, ActiveBinding]:
        bindings = super().active_bindings

        def display_order(key: str) -> tuple[int, int]:
            if key.startswith("f") and key[1:].isdigit():
                return (0, int(key[1:]))
            return (1 if key.startswith("ctrl+") else 2, 0)

        return {key: bindings[key] for key in sorted(bindings, key=display_order)}

    @property
    def tutor(self) -> "TutorApp":
        return cast("TutorApp", self.app)

    @property
    def store(self):
        return self.tutor.store


class CodeEditor(TextArea):
    BINDINGS = [Binding("ctrl+a", "select_all", "Select all", show=False, priority=True)]


def brand(detail: str = "LEARN PYTHON, ONE CONCEPT AT A TIME") -> Horizontal:
    return Horizontal(
        Static("[b #86bde8]py[/][#ffd343]tuitor[/]", classes="brand"),
        Static(detail, classes="eyebrow brand-detail"),
        classes="topbar",
    )
