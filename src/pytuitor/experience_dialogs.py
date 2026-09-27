"""Occasional workspace actions and explicit check selection."""

from rich.text import Text
from textual import on
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, OptionList, Static, TextArea
from textual.widgets.option_list import Option

from pytuitor.check_feedback import status


class WorkspaceTools(ModalScreen[str | None]):
    BINDINGS = [("escape", "cancel", "Close")]

    def compose(self):
        with VerticalScroll(classes="dialog", id="workspace-tools-dialog"):
            yield Static("Workspace tools", classes="title")
            yield Static("Your draft stays open while you choose an action.", classes="muted")
            for action, label in (
                ("add-file", "Add file"),
                ("environment", "Project environment"),
                ("note", "Note for next time"),
                ("export", "Export this stage"),
                ("reset", "Back up and reset stage"),
                ("close", "Close"),
            ):
                yield Button(label, id=f"tool-{action}")

    def on_mount(self):
        self.query_one("#tool-add-file", Button).focus()

    @on(Button.Pressed)
    def choose(self, event):
        value = event.button.id.removeprefix("tool-")
        self.dismiss(None if value == "close" else value)

    def action_cancel(self):
        self.dismiss(None)


class ResumeNote(ModalScreen[str | None]):
    BINDINGS = [("escape", "cancel", "Cancel")]

    def __init__(self, note=""):
        super().__init__()
        self.note = note

    def compose(self):
        with Vertical(classes="dialog", id="resume-note-dialog"):
            yield Static("Note for next time", classes="title")
            yield Static(
                "Keep a short reminder for this activity (up to 1,000 characters).", classes="muted"
            )
            yield TextArea(self.note, id="resume-note-editor")
            yield Static("", id="note-feedback", markup=False)
            with Horizontal(classes="actions"):
                yield Button("Save note", id="save-note", variant="primary")
                yield Button("Cancel", id="cancel-note")

    def on_mount(self):
        self.query_one("#resume-note-editor").focus()

    @on(Button.Pressed, "#save-note")
    def save(self):
        value = self.query_one("#resume-note-editor", TextArea).text
        if len(value) > 1000:
            self.query_one("#note-feedback", Static).update(
                "Please shorten the note to 1,000 characters."
            )
        else:
            self.dismiss(value)

    @on(Button.Pressed, "#cancel-note")
    def action_cancel(self):
        self.dismiss(None)


class CheckChooser(ModalScreen[int | None]):
    BINDINGS = [("escape", "cancel", "Close")]

    def __init__(self, checks, selected):
        super().__init__()
        self.checks = list(checks)
        self.selected = selected

    def compose(self):
        with Vertical(classes="dialog", id="check-chooser-dialog"):
            yield Static("Choose a check", classes="title")
            yield Static("Passing checks stay available for inspection.", classes="muted")
            yield OptionList(
                *[
                    Option(
                        Text(f"{case['number']}. {status(case)} · {case['label']}"),
                        id=str(case["number"]),
                    )
                    for case in self.checks
                ],
                id="check-chooser",
            )
            yield Button("Close", id="check-chooser-close")

    def on_mount(self):
        listing = self.query_one(OptionList)
        listing.highlighted = next(
            (i for i, case in enumerate(self.checks) if case["number"] == self.selected), 0
        )
        listing.focus()

    @on(OptionList.OptionSelected)
    def choose(self, event):
        self.dismiss(int(event.option.id))

    @on(Button.Pressed, "#check-chooser-close")
    def action_cancel(self):
        self.dismiss(None)
