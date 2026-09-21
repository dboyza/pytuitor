"""Opt-in learning aids and project environment controls."""

from difflib import unified_diff
from pathlib import Path

from textual import on, work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Select, Static, TextArea

from pytuitor.models import Lesson, StageContract
from pytuitor.workspace import (
    WorkspaceError,
    create_environment,
    environment_python,
    install_package,
)


class SolutionDialog(ModalScreen):
    BINDINGS = [Binding("escape", "close", "Close")]

    def __init__(
        self, lesson: Lesson, contract: StageContract, drafts: dict[str, str] | None = None
    ):
        super().__init__()
        self.lesson = lesson
        self.drafts = dict(drafts or {})
        self.comparing = False
        self.files = contract.reference_files or {lesson.entrypoint: lesson.solution}

    def on_mount(self) -> None:
        self.set_class(self.size.height < 32, "compact")

    def on_resize(self) -> None:
        self.set_class(self.size.height < 32, "compact")

    def compose(self) -> ComposeResult:
        with Vertical(classes="dialog", id="solution-dialog"):
            yield Static("Reference solution", classes="title")
            yield Static(
                "One correct approach. Compare the reasoning with yours; your draft stays saved.",
                id="solution-intro",
            )
            yield Select(
                [(name, name) for name in self.files],
                value=self.lesson.entrypoint,
                allow_blank=False,
                id="solution-file",
            )
            yield TextArea.code_editor(
                self.files[self.lesson.entrypoint],
                language="python",
                theme="vscode_dark",
                read_only=True,
                id="solution-code",
            )
            yield Static(
                "Explain one difference: what input exposes it, and why does the result change?",
                id="compare-prompt",
            )
            with Horizontal(id="solution-actions"):
                yield Button("Compare with my draft", id="compare-solution")
                yield Button("Back to my work", id="close-solution")

    @on(Select.Changed, "#solution-file")
    def change_file(self, event: Select.Changed) -> None:
        if event.value in self.files:
            self.show_file(event.value)

    def show_file(self, name: str) -> None:
        reference = self.files[name]
        if self.comparing:
            reference = (
                "".join(
                    unified_diff(
                        self.drafts.get(name, "").splitlines(keepends=True),
                        reference.splitlines(keepends=True),
                        fromfile="Your draft: " + name,
                        tofile="One reference: " + name,
                    )
                )
                or "No textual differences. Explain why your approach meets the contract."
            )
        editor = self.query_one("#solution-code", TextArea)
        editor.language = None if self.comparing else "python"
        editor.load_text(reference)

    @on(Button.Pressed, "#compare-solution")
    def compare(self) -> None:
        self.comparing = not self.comparing
        self.query_one("#compare-solution", Button).label = (
            "Show reference" if self.comparing else "Compare with my draft"
        )
        self.show_file(self.query_one("#solution-file", Select).value)

    @on(Button.Pressed, "#close-solution")
    def action_close(self) -> None:
        self.dismiss()


class FileDialog(ModalScreen[str | None]):
    BINDINGS = [Binding("escape", "cancel", "Cancel")]

    def compose(self) -> ComposeResult:
        with VerticalScroll(classes="dialog"):
            yield Static("Add a project file", classes="title")
            yield Static("Use a relative path, for example helpers.py or tests/test_tools.py.")
            yield Input(placeholder="File path", id="new-file", max_length=180)
            yield Static("", id="file-error")
            with Horizontal(classes="actions"):
                yield Button("Add file", id="add-file-confirm", variant="primary")
                yield Button("Cancel", id="cancel-file")

    @on(Button.Pressed, "#add-file-confirm")
    @on(Input.Submitted, "#new-file")
    def add(self) -> None:
        from pytuitor.workspace import validate_files

        name = self.query_one("#new-file", Input).value.strip()
        try:
            validate_files({name: ""})
        except WorkspaceError as exc:
            self.query_one("#file-error", Static).update(str(exc))
        else:
            self.dismiss(name)

    @on(Button.Pressed, "#cancel-file")
    def action_cancel(self) -> None:
        self.dismiss(None)


class EnvironmentDialog(ModalScreen):
    BINDINGS = [Binding("escape", "close", "Close")]

    def __init__(self, path: Path):
        super().__init__()
        self.path = path
        self.busy = False

    def compose(self) -> ComposeResult:
        with Vertical(classes="dialog", id="environment-dialog"):
            yield Static("Project environment", classes="title")
            yield Static(
                "Create an offline virtual environment to keep project packages separate. "
                "Course exercises need no extra packages.\n\n"
                "Install package downloads third-party wheels and dependencies from PyPI. "
                "Only install packages you trust."
            )
            with Horizontal(classes="environment-actions"):
                yield Button(
                    "Create environment", id="create-environment", disabled=self.path.exists()
                )
                yield Button("Close", id="close-environment")
            with Horizontal(classes="environment-actions"):
                yield Input(placeholder="Package or package==version", id="package-name")
                yield Button(
                    "Install package", id="install-package", disabled=not self.path.exists()
                )
            with VerticalScroll(id="environment-output"):
                yield Static(
                    "Using this project's environment."
                    if self.path.exists()
                    else "Using the tutor's Python until you create an environment.",
                    id="environment-result",
                    markup=False,
                )

    def show_result(self, text: str) -> None:
        if self.is_mounted and self.query("#environment-result"):
            self.query_one("#environment-result", Static).update(text)

    def set_busy(self, busy: bool) -> None:
        self.busy = busy
        if not self.is_mounted or not self.query("#create-environment"):
            return
        self.query_one("#close-environment", Button).label = "Cancel / close" if busy else "Close"
        self.query_one("#create-environment", Button).disabled = busy or self.path.exists()
        self.query_one("#install-package", Button).disabled = busy or not self.path.exists()

    @on(Button.Pressed, "#create-environment")
    @work(exclusive=True)
    async def create(self) -> None:
        self.set_busy(True)
        self.show_result("Creating an isolated environment…")
        try:
            await create_environment(self.path)
            self.show_result("Ready. Run and Check now use this environment.")
        except (OSError, WorkspaceError) as exc:
            self.show_result(str(exc))
        finally:
            self.set_busy(False)

    @on(Button.Pressed, "#install-package")
    @work(exclusive=True)
    async def install(self) -> None:
        requirement = self.query_one("#package-name", Input).value.strip()
        self.set_busy(True)
        self.show_result("Installing the requested package from PyPI…")
        try:
            output = await install_package(environment_python(self.path), requirement)
            self.show_result(output)
        except (OSError, WorkspaceError) as exc:
            self.show_result(str(exc))
        finally:
            self.set_busy(False)

    @on(Button.Pressed, "#close-environment")
    def action_close(self) -> None:
        if self.busy:
            self.workers.cancel_node(self)
        self.dismiss()


def error_guidance(error: str) -> str:
    """Explain the next debugging action without rewriting the learner's program."""
    for kind, guidance in (
        (
            "IndentationError",
            "Indentation groups statements. Use four spaces inside each if, loop, function or "
            "class, and align statements in the same block.",
        ),
        (
            "SyntaxError",
            "Python could not read this statement. Check the reported line and the one above "
            "it for missing colons, closing quotes or brackets.",
        ),
        (
            "NameError",
            "This name has no value yet. Check its spelling and whether the assignment or "
            "import runs before this line.",
        ),
        (
            "TypeError",
            "An operation received a value it cannot use. Check the types and the function's "
            "expected arguments; input() always returns text.",
        ),
        (
            "ValueError",
            "The type was acceptable but the value was not. Inspect the input and the "
            "conversion or validation on the reported line.",
        ),
        (
            "IndexError",
            "That position is outside the sequence. Positions begin at zero and end at "
            "len(sequence) - 1; also consider an empty sequence.",
        ),
        (
            "KeyError",
            "That key is missing from the dictionary. Check spelling and decide how absent "
            "data should be handled.",
        ),
        (
            "ModuleNotFoundError",
            "Python could not find an imported module. Check the project file name and import "
            "spelling. Third-party packages belong in the project environment.",
        ),
        (
            "FileNotFoundError",
            "This run starts with your saved project files in a fresh working directory. "
            "Check the relative path and create any required data file.",
        ),
        (
            "AssertionError",
            "An assertion found a result that did not meet its condition. Compare the actual "
            "value with the requirement before changing the test.",
        ),
    ):
        if kind in error:
            return guidance
    return ""


class DeleteFileDialog(ModalScreen[bool]):
    BINDINGS = [Binding("escape", "cancel", "Cancel")]

    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def compose(self) -> ComposeResult:
        with VerticalScroll(classes="dialog"):
            yield Static("Remove this file?", classes="title")
            yield Static(self.name, markup=False)
            yield Static("The complete workspace will be backed up in exports first.")
            with Horizontal(classes="actions"):
                yield Button("Keep file", id="keep-file", variant="primary")
                yield Button("Remove file", id="remove-file-confirm")

    def on_mount(self) -> None:
        self.query_one("#keep-file").focus()

    @on(Button.Pressed, "#keep-file")
    def action_cancel(self) -> None:
        self.dismiss(False)

    @on(Button.Pressed, "#remove-file-confirm")
    def confirm(self) -> None:
        self.dismiss(True)


class RunFilesDialog(ModalScreen[dict[str, str] | None]):
    BINDINGS = [Binding("escape", "close", "Close")]

    def __init__(self, files: dict[str, str]):
        super().__init__()
        self.files = dict(files)

    def compose(self) -> ComposeResult:
        first = next(iter(self.files))
        with Vertical(classes="dialog", id="run-files-dialog"):
            yield Static("Files from your last Run", classes="title")
            yield Static(
                "Inspect these new or changed text files before keeping them. "
                "Save to workspace backs up your current workspace first, then adds or replaces "
                "the files listed here. It does not delete other files."
            )
            yield Select(
                [(name, name) for name in self.files],
                value=first,
                allow_blank=False,
                id="run-file-choice",
            )
            yield TextArea(
                self.files[first], read_only=True, theme="vscode_dark", id="run-file-code"
            )
            with Horizontal(classes="actions"):
                yield Button("Save to workspace", id="keep-run-files", variant="primary")
                yield Button("Close", id="close-run-files")

    @on(Select.Changed, "#run-file-choice")
    def change_file(self, event: Select.Changed) -> None:
        if event.value in self.files:
            self.query_one("#run-file-code", TextArea).load_text(self.files[event.value])

    @on(Button.Pressed, "#keep-run-files")
    def keep(self) -> None:
        self.dismiss(self.files)

    @on(Button.Pressed, "#close-run-files")
    def action_close(self) -> None:
        self.dismiss(None)
