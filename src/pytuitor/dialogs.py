"""Global keyboard help and explicit profile reset."""

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, Static


class KeyboardHelp(ModalScreen):
    BINDINGS = [Binding("escape,f10", "close", "Close", priority=True)]

    def compose(self) -> ComposeResult:
        with VerticalScroll(classes="dialog", id="help-dialog"):
            yield Static("Everything works from the keyboard", classes="title")
            yield Static(
                "EVERYWHERE\n"
                "Tab / Shift+Tab     Next / previous control\n"
                "↑ ↓                 Move through a list\n"
                "Enter               Open or activate\n"
                "Space               Toggle a checkbox\n"
                "Ctrl+P              Search commands\n"
                "Ctrl+B              Dashboard\n"
                "Ctrl+Q              Save and quit\n\n"
                "ON THE DASHBOARD\n"
                "C                   Continue learning\n"
                "P                   Known topics\n"
                "S                   Browse syllabus\n\n"
                "IN THE SYLLABUS\n"
                "↑ ↓ / PageUp / PageDown   Scroll the outline\n"
                "Home / End          Start / end of the outline\n"
                "Escape              Back\n\n"
                "IN A LESSON\n"
                "Ctrl+T              Cycle lesson / editor / console\n"
                "F6 / Shift+F6       Next / previous pane\n"
                "Ctrl+R              Run interactively\n"
                "F4                  Focus exercise requirements\n"
                "F5 or Ctrl+Enter    Check with test inputs\n"
                "F1                  Reveal a hint\n"
                "F7                  Focus the lesson question\n"
                "Ctrl+N              Next lesson after completion\n"
                "F8                  Stop the running program\n\n"
                "IN THE FILE EXPLORER\n"
                "Ctrl+E              Show and focus files\n"
                "↑ ↓                 Move through files and folders\n"
                "← / →               Collapse / expand a folder\n"
                "Enter               Open file or toggle folder\n"
                "Files button        Show / hide the explorer\n\n"
                "IN THE EDITOR\n"
                "Tab                 Indent\n"
                "Escape, then Tab    Leave editor and move focus\n"
                "Ctrl+A              Select all\n"
                "Ctrl+Z / Ctrl+Y     Undo / redo\n\n"
                "IN THE CONSOLE\n"
                "Enter               Send the answer you typed\n"
                "Ctrl+D              End input (EOF)\n\n"
                "On some keyboards, hold Fn to use the F-keys.\n"
                "The command palette also lists project file, environment, "
                "solution, export and reset actions.",
                markup=False,
            )
            yield Button("Close", id="close-help")

    @on(Button.Pressed, "#close-help")
    def action_close(self) -> None:
        self.dismiss()


class ConfirmRestart(ModalScreen[bool]):
    BINDINGS = [Binding("escape", "cancel", "Cancel")]

    def compose(self) -> ComposeResult:
        with Vertical(classes="dialog", id="restart-dialog"):
            yield Static("Erase progress and start over?", classes="title")
            yield Static(
                "This erases all saved lesson drafts, completions, hints, and checked topics "
                "in this profile, then returns to the welcome screen.\n\n"
                "This cannot be undone. Python files you already exported are separate and remain.",
                classes="muted",
            )
            with Horizontal(classes="actions"):
                yield Button("Keep my progress", id="cancel-restart", variant="primary")
                yield Button("Erase and start over", id="confirm-restart", variant="error")

    def on_mount(self) -> None:
        self.query_one("#cancel-restart").focus()

    @on(Button.Pressed, "#cancel-restart")
    def action_cancel(self) -> None:
        self.dismiss(False)

    @on(Button.Pressed, "#confirm-restart")
    def confirm(self) -> None:
        self.dismiss(True)


class ConfirmReset(ModalScreen[bool]):
    BINDINGS = [Binding("escape", "cancel", "Cancel")]

    def compose(self) -> ComposeResult:
        with Vertical(classes="dialog", id="reset-dialog"):
            yield Static("Start this exercise again?", classes="title")
            yield Static(
                "Your current code will be backed up in your profile's exports folder.\n"
                "This stage's draft, hints, and pass status will be reset.\n"
                "Build becomes blank; Repair restores the broken program. The other draft is kept.",
                classes="muted",
            )
            with Horizontal(classes="actions"):
                yield Button("Reset exercise", id="confirm-reset", variant="primary")
                yield Button("Keep working", id="cancel")

    @on(Button.Pressed, "#confirm-reset")
    def confirm(self) -> None:
        self.dismiss(True)

    @on(Button.Pressed, "#cancel")
    def action_cancel(self) -> None:
        self.dismiss(False)


class ExecutionInfo(ModalScreen):
    BINDINGS = [Binding("escape", "close", "Close")]

    def compose(self) -> ComposeResult:
        with VerticalScroll(classes="dialog"):
            yield Static("Execution and privacy", classes="title")
            yield Static(
                "Your lessons and progress stay local. Run and Check execute Python as your "
                "user, with access to your files and network. Only run code you trust.\n\n"
                "Temporary workspaces, time limits, output limits, and virtual environments "
                "help contain mistakes. They are not an operating-system security sandbox.\n\n"
                "The tutor does not require accounts, send learning telemetry, or download "
                "packages during lessons. Installing a named package and checking for upgrades "
                "are explicit network actions."
            )
            yield Button("Back to learning", id="close-execution-info")

    @on(Button.Pressed, "#close-execution-info")
    def action_close(self) -> None:
        self.dismiss()
