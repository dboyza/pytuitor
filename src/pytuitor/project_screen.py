"""The learner's game, working checkpoints, and explicit recovery choices."""

from __future__ import annotations

from rich.text import Text
from textual import on, work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.events import Resize
from textual.screen import ModalScreen
from textual.widgets import Button, Footer, Input, OptionList, Static
from textual.widgets.option_list import Option

from pytuitor.curriculum import BY_ID, CHAPTERS
from pytuitor.learning_progress import progress_counts
from pytuitor.models import ProjectMilestone
from pytuitor.project_catalog import BY_MILESTONE, LANTERN_REACH, MILESTONES
from pytuitor.project_workspace import ProjectWorkspace
from pytuitor.runner import ConsoleSession, execute
from pytuitor.ui import TutorScreen, brand
from pytuitor.workspace import WorkspaceError


class BaseChoice(ModalScreen[bool]):
    BINDINGS = [Binding("escape", "cancel", "Cancel")]

    def __init__(self, milestone: ProjectMilestone, exists: bool):
        super().__init__()
        self.milestone = milestone
        self.exists = exists

    def compose(self) -> ComposeResult:
        with VerticalScroll(classes="dialog"):
            yield Static("Start from supplied earlier code?", classes="title")
            yield Static(
                "This is the working game before this milestone, not its solution. "
                "Earlier milestones stay incomplete. Your future "
                "checkpoints will record this supplied base.\n\n"
                + (
                    "Both current stage drafts will be backed up before a new attempt begins. "
                    "Existing working checkpoints remain available."
                    if self.exists
                    else "No existing draft will be replaced."
                ),
                markup=False,
            )
            with Horizontal(classes="actions"):
                yield Button("Keep working", id="base-cancel", variant="primary")
                yield Button("Use supplied base", id="base-confirm")

    @on(Button.Pressed, "#base-cancel")
    def action_cancel(self) -> None:
        self.dismiss(False)

    @on(Button.Pressed, "#base-confirm")
    def confirm(self) -> None:
        self.dismiss(True)


class CheckpointHistory(ModalScreen[str | None]):
    BINDINGS = [Binding("escape", "close", "Close")]

    def __init__(self, workspace: ProjectWorkspace, milestone: ProjectMilestone):
        super().__init__()
        self.workspace = workspace
        self.milestone = milestone
        self.selected: str | None = None
        self.restore_pending = False

    def compose(self) -> ComposeResult:
        with Vertical(classes="dialog", id="checkpoint-dialog"):
            yield Static("Working checkpoint history", classes="title")
            yield Static(
                "Immutable source versions. Playing and exporting leave drafts unchanged.",
                classes="muted",
            )
            yield OptionList(id="checkpoint-list")
            yield Static(id="checkpoint-detail", markup=False)
            with Horizontal(classes="actions"):
                yield Button("Play", id="checkpoint-play")
                yield Button("Export", id="checkpoint-export")
                yield Button("Restore copy", id="checkpoint-restore")
                yield Button("Close", id="checkpoint-close")
            yield Static(id="checkpoint-feedback", markup=False, classes="muted")

    def on_mount(self) -> None:
        listing = self.query_one("#checkpoint-list", OptionList)
        for index, item in enumerate(reversed(self.workspace.data["checkpoints"]), 1):
            title = BY_ID.get(item["milestone"])
            label = title.title if title else item["milestone"]
            provenance = "supported" if item.get("supported") else "own code"
            listing.add_option(
                Option(
                    Text(f"{index:02}  {label} · r{item['revision']} · {provenance}"), id=item["id"]
                )
            )
        if listing.option_count:
            listing.highlighted = 0
        else:
            self.query_one("#checkpoint-detail", Static).update(
                "Pass an Extend stage to save your first working checkpoint."
            )
        self.update_buttons()
        listing.focus()

    def update_buttons(self) -> None:
        for name in ("play", "export", "restore"):
            self.query_one(f"#checkpoint-{name}", Button).disabled = self.selected is None

    @on(OptionList.OptionHighlighted, "#checkpoint-list")
    def select_checkpoint(self, event: OptionList.OptionHighlighted) -> None:
        self.selected = event.option.id
        self.restore_pending = False
        self.query_one("#checkpoint-restore", Button).label = "Restore copy"
        item = next(
            item for item in self.workspace.data["checkpoints"] if item["id"] == self.selected
        )
        self.query_one("#checkpoint-detail", Static).update(
            f"Saved {item.get('created', 'earlier')}\n"
            f"{len(item['capabilities'])} "
            f"{'capability' if len(item['capabilities']) == 1 else 'capabilities'} · "
            f"{item.get('bytes', 0):,} bytes · {self.selected[:12]}"
        )
        self.update_buttons()

    @on(Button.Pressed, "#checkpoint-play")
    def play(self) -> None:
        if self.selected:
            try:
                payload = self.workspace.read_checkpoint(self.selected)
                self.app.push_screen(CheckpointPlayer(payload))
            except (OSError, WorkspaceError) as error:
                self.query_one("#checkpoint-feedback", Static).update(str(error))

    @on(Button.Pressed, "#checkpoint-export")
    def export(self) -> None:
        if self.selected:
            try:
                path = self.workspace.export_checkpoint(self.selected)
                self.query_one("#checkpoint-feedback", Static).update(f"Exported to {path}")
            except (OSError, WorkspaceError) as error:
                self.query_one("#checkpoint-feedback", Static).update(str(error))

    @on(Button.Pressed, "#checkpoint-restore")
    def restore(self) -> None:
        if not self.selected:
            return
        if not self.restore_pending:
            self.restore_pending = True
            self.query_one("#checkpoint-restore", Button).label = "Confirm restore"
            self.query_one("#checkpoint-feedback", Static).update(
                f"Restore into {self.milestone.lesson.title}? "
                "Both current stage drafts will be backed up. "
                "The restored copy must be checked again. Select Confirm restore to continue."
            )
            return
        self.dismiss(self.selected)

    @on(Button.Pressed, "#checkpoint-close")
    def action_close(self) -> None:
        self.dismiss(None)


class CheckpointPlayer(ModalScreen):
    BINDINGS = [
        Binding("escape", "close", "Close", priority=True),
        Binding("ctrl+d", "eof", "End input", priority=True),
    ]

    def __init__(self, payload: dict):
        super().__init__()
        self.payload = payload
        self.transcript = ""
        self.console = None
        self.execution = None
        self.closing = False

    def compose(self) -> ComposeResult:
        with Vertical(classes="dialog", id="checkpoint-player"):
            yield Static("Play a working checkpoint", classes="title")
            yield Static(
                "Temporary run. Source history and current drafts remain unchanged.",
                classes="muted",
            )
            with VerticalScroll(id="checkpoint-output-scroll"):
                yield Static("Starting expedition…", id="checkpoint-output", markup=False)
            yield Input(
                placeholder="Type a command, then Enter", id="checkpoint-input", disabled=True
            )
            yield Button("Close", id="player-close")

    def on_mount(self) -> None:
        self.console = ConsoleSession(self.output, self.waiting)
        self.execution = self.run_checkpoint()

    def output(self, text: str) -> None:
        if self.closing or not self.is_mounted:
            return
        self.transcript = (self.transcript + text)[-70000:]
        self.query_one("#checkpoint-output", Static).update(self.transcript)
        self.query_one("#checkpoint-output-scroll", VerticalScroll).scroll_end(animate=False)

    def waiting(self, waiting: bool) -> None:
        if self.closing or not self.is_mounted:
            return
        field = self.query_one("#checkpoint-input", Input)
        field.disabled = not waiting
        if waiting:
            field.focus()

    @on(Input.Submitted, "#checkpoint-input")
    def answer(self, event: Input.Submitted) -> None:
        if self.console and self.console.submit(event.value):
            self.output(event.value + "\n")
            event.input.value = ""

    def action_eof(self) -> None:
        if self.console:
            self.console.end_input()

    @work(exclusive=True)
    async def run_checkpoint(self) -> None:
        lesson = BY_ID.get(self.payload["milestone"])
        if lesson is None:
            self.output("This milestone is no longer available. Export its source to play it.")
            return
        try:
            result = await execute(
                lesson,
                self.payload["files"][lesson.entrypoint],
                "",
                check=False,
                files=self.payload["files"],
                console=self.console,
            )
            self.output(
                "\n" + (result.error or "Expedition finished. Close to return to your work.")
            )
            if not self.closing and self.is_mounted:
                self.query_one("#checkpoint-input", Input).disabled = True
        except (OSError, WorkspaceError) as error:
            self.output(f"\nCannot run this checkpoint: {error}")

    @on(Button.Pressed, "#player-close")
    def action_close(self) -> None:
        self.closing = True
        if self.execution:
            self.execution.cancel()
        self.dismiss()

    def on_unmount(self) -> None:
        self.closing = True
        if self.execution:
            self.execution.cancel()


class ProjectScreen(TutorScreen):
    BINDINGS = [Binding("escape", "back", "Back")]

    def __init__(self):
        super().__init__()
        self.selected = MILESTONES[0]

    @property
    def workspace(self) -> ProjectWorkspace:
        return ProjectWorkspace(self.store)

    def compose(self) -> ComposeResult:
        yield brand("YOUR GROWING GAME")
        with Vertical(id="game-body"):
            with Horizontal(id="game-header"):
                yield Static(LANTERN_REACH.title, classes="hero")
                yield Button("Back", id="game-back")
            yield Static(LANTERN_REACH.description, id="game-description", classes="muted")
            yield Static(id="game-summary", classes="topic-preview")
            with Horizontal(id="game-content"):
                yield OptionList(id="milestone-list")
                with VerticalScroll(id="milestone-details"):
                    yield Static(id="milestone-title", classes="title", markup=False)
                    yield Static(id="milestone-description", markup=False)
                    yield Static(id="milestone-origin", classes="topic-preview", markup=False)
                    yield Static(id="milestone-preparation", classes="muted", markup=False)
            with Horizontal(id="game-actions"):
                yield Button("Open milestone", id="game-open", variant="primary")
                yield Button("Supplied base", id="game-base")
                yield Button("History", id="game-history")
                yield Button("Export latest", id="game-export")
            yield Static(id="game-feedback", markup=False, classes="muted")
        yield Footer(show_command_palette=False)

    def on_mount(self) -> None:
        last = self.workspace.data.get("last_milestone")
        self.selected = BY_MILESTONE.get(
            last,
            next(
                (item for item in MILESTONES if self.store.status(item.lesson) != "completed"),
                MILESTONES[0],
            ),
        )
        self.refresh_game()
        self.apply_layout()
        self.query_one("#milestone-list").focus()

    def on_screen_resume(self) -> None:
        if self.is_mounted:
            self.refresh_game()

    def on_resize(self, event: Resize) -> None:
        self.apply_layout()

    def apply_layout(self) -> None:
        self.set_class(self.size.width < 100, "narrow")

    def refresh_game(self) -> None:
        listing = self.query_one("#milestone-list", OptionList)
        listing.clear_options()
        sections = {chapter.id: chapter.section_id for chapter in CHAPTERS}
        for index, item in enumerate(MILESTONES, 1):
            status = self.store.status(item.lesson)
            symbol = {"new": "○", "in progress": "◐", "completed": "✓"}[status]
            optional = sections[item.lesson.chapter_id] in ("python-depth", "specialized-topics")
            listing.add_option(
                Option(
                    Text(
                        f"{symbol} {index:02} {item.lesson.title}"
                        + (" · optional" if optional else "")
                    ),
                    id=item.lesson.id,
                )
            )
        listing.highlighted = MILESTONES.index(self.selected)
        core, optional = progress_counts(self.store, [item.lesson for item in MILESTONES])
        snapshots = self.workspace.data["checkpoints"]
        total_bytes = sum(item.get("bytes", 0) for item in snapshots)
        storage = f"{total_bytes} B" if total_bytes < 1024 else f"{total_bytes / 1024:.1f} KiB"
        versions = "working version" if len(snapshots) == 1 else "working versions"
        self.query_one("#game-summary", Static).update(
            f"Core {core[0]}/{core[2]} · Optional {optional[0]}/{optional[2]} · "
            f"{len(snapshots)} {versions} · {storage}"
        )
        self.query_one("#game-export", Button).disabled = not snapshots
        self.show_selected()

    @on(OptionList.OptionHighlighted, "#milestone-list")
    def highlight(self, event: OptionList.OptionHighlighted) -> None:
        self.selected = BY_MILESTONE[event.option.id]
        self.show_selected()

    @on(OptionList.OptionSelected, "#milestone-list")
    def selected_option(self, event: OptionList.OptionSelected) -> None:
        self.selected = BY_MILESTONE[event.option.id]
        self.open_milestone()

    def show_selected(self) -> None:
        lesson = self.selected.lesson
        self.query_one("#milestone-title", Static).update(lesson.title)
        from pytuitor.content.lantern.briefs import BRIEFS

        self.query_one("#milestone-description", Static).update(
            BRIEFS[lesson.id.removeprefix("reach-")].outcome
        )
        entry = self.workspace.data["milestones"].get(lesson.id)
        compatible = self.workspace.compatible(self.selected)
        origin = (
            "Resume your saved Extend and Repair drafts."
            if entry
            else "Starts from your compatible working checkpoint."
            if compatible
            else "Starts from labeled supplied earlier code; skipped work stays incomplete."
            if self.selected.requires
            else "Start with a blank file and build your first scene."
        )
        self.query_one("#milestone-origin", Static).update(origin)
        self.query_one("#milestone-preparation", Static).update(
            "Extend + independent Repair · " + str(lesson.minutes) + " min\n"
            "Preparation is advisory. Source versions are retained until you explicitly start over."
        )
        self.query_one("#game-base", Button).disabled = not self.selected.requires

    @on(Button.Pressed, "#game-open")
    def open_milestone(self) -> None:
        # If the overview was opened from an active editor, close it before reopening
        # to prevent two mounted autosave timers from owning the same draft.
        from pytuitor.lesson_screen import LessonScreen

        if any(isinstance(screen, LessonScreen) for screen in self.app.screen_stack):
            self.tutor.action_dashboard()
        self.tutor.open_activity(self.selected.lesson)

    @on(Button.Pressed, "#game-base")
    def choose_base(self) -> None:
        exists = self.selected.lesson.id in self.workspace.data["milestones"]
        self.app.push_screen(BaseChoice(self.selected, exists), self.use_base)

    def use_base(self, confirmed: bool) -> None:
        if not confirmed:
            return
        try:
            self.stop_old_editor()
            if self.selected.lesson.id in self.workspace.data["milestones"]:
                path = self.workspace.replace_base(self.selected)
                self.query_one("#game-feedback", Static).update(
                    f"Previous drafts backed up to {path}"
                )
            else:
                self.workspace.start(self.selected, supplied=True)
                self.store.save()
            self.refresh_game()
        except (OSError, WorkspaceError) as error:
            self.query_one("#game-feedback", Static).update(str(error))

    def stop_old_editor(self) -> None:
        from pytuitor.lesson_screen import LessonScreen

        for screen in self.app.screen_stack:
            if isinstance(screen, LessonScreen) and screen.lesson.id == self.selected.lesson.id:
                screen.save_draft()
                screen.stop()
                if screen.save_timer:
                    screen.save_timer.stop()
                screen.suspend_saves = True

    @on(Button.Pressed, "#game-history")
    def history(self) -> None:
        self.app.push_screen(CheckpointHistory(self.workspace, self.selected), self.restore)

    def restore(self, identifier: str | None) -> None:
        if identifier is None:
            return
        try:
            self.stop_old_editor()
            if self.selected.lesson.id in self.workspace.data["milestones"]:
                backup = self.workspace.replace_base(self.selected, identifier)
                message = f"Restored into a new draft. Previous work backed up to {backup}"
            else:
                entry = self.workspace.start(self.selected, parent=identifier)
                entry["base_origin"] = "restored"
                self.store.save()
                message = (
                    "Checkpoint copied into a new draft. Check it against this milestone's "
                    "requirements."
                )
            self.query_one("#game-feedback", Static).update(message)
            self.refresh_game()
        except (OSError, WorkspaceError) as error:
            self.query_one("#game-feedback", Static).update(str(error))

    @on(Button.Pressed, "#game-export")
    def export_latest(self) -> None:
        checkpoints = self.workspace.data["checkpoints"]
        if not checkpoints:
            return
        try:
            path = self.workspace.export_checkpoint(checkpoints[-1]["id"])
            self.query_one("#game-feedback", Static).update(f"Exported working game to {path}")
        except (OSError, WorkspaceError) as error:
            self.query_one("#game-feedback", Static).update(str(error))

    @on(Button.Pressed, "#game-back")
    def action_back(self) -> None:
        from pytuitor.lesson_screen import LessonScreen

        if any(
            isinstance(screen, LessonScreen) and screen.suspend_saves
            for screen in self.app.screen_stack
        ):
            self.tutor.action_dashboard()
        else:
            self.app.pop_screen()
