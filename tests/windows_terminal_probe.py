"""Observation-only application used by the real PowerShell/ConPTY journey."""

import json
import sys
from pathlib import Path

from textual.widgets import TextArea

import pytuitor.app
from pytuitor.app import TutorApp
from pytuitor.lesson_screen import LessonScreen


class ObservedApp(TutorApp):
    CSS_PATH = Path(pytuitor.app.__file__).with_name("theme.tcss")

    def on_ready(self):
        self.set_interval(0.05, self.record_state)

    def record_state(self):
        screen = self.screen
        lesson = isinstance(screen, LessonScreen)
        observation = {
            "screen": type(screen).__name__,
            "pane": getattr(screen, "active_pane", "dashboard"),
            "focus": self.focused.id if self.focused else None,
            "stage": getattr(screen, "stage", None),
            "code": screen.query_one("#editor", TextArea).text if lesson else "",
            "transcript": screen.transcript if lesson else "",
            "passed": screen.stage_passed(screen.stage) if lesson else False,
        }
        target = Path(sys.argv[2])
        temporary = target.with_suffix(".tmp")
        temporary.write_text(json.dumps(observation), encoding="utf-8")
        try:
            temporary.replace(target)
        except PermissionError:
            pass  # The test may briefly be reading the previous observation on Windows.


if __name__ == "__main__":
    ObservedApp(Path(sys.argv[1])).run()
