"""Lesson reading, code editing, and an interactive Python console."""

from datetime import datetime

from rich.text import Text
from textual import on, work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.events import DescendantFocus, Resize
from textual.widgets import Button, Footer, Input, Markdown, OptionList, Static, TextArea, Tree
from textual.widgets.option_list import Option

from pytuitor.check_feedback import render_feedback
from pytuitor.curriculum import BY_ID, Lesson, default_input
from pytuitor.dialogs import ConfirmReset
from pytuitor.experience_dialogs import CheckChooser, ResumeNote, WorkspaceTools
from pytuitor.file_tree import FileTree
from pytuitor.learning_progress import load_report, report_is_current, safe_view, saved_report
from pytuitor.learning_tools import (
    DeleteFileDialog,
    EnvironmentDialog,
    FileDialog,
    RunFilesDialog,
    SolutionDialog,
    error_guidance,
)
from pytuitor.models import StageContract
from pytuitor.progress_types import CheckEvent, DraftState, StageName
from pytuitor.runner import ConsoleSession, execute
from pytuitor.ui import CodeEditor, TutorScreen, brand
from pytuitor.workspace import WorkspaceError, environment_python, export_workspace, validate_files


class ConsoleInput(Input):
    BINDINGS = [Binding("ctrl+d", "end_input", "End input", priority=True)]

    def action_end_input(self) -> None:
        self.screen.end_input()


class LessonScreen(TutorScreen):
    BINDINGS = [
        Binding("ctrl+r", "run", "Run", priority=True),
        Binding("f5,ctrl+enter", "check", "Check", priority=True),
        Binding("ctrl+s", "save", "Save", priority=True, show=False),
        Binding("f1", "hint", "Hint", priority=True),
        Binding("ctrl+t", "cycle_pane(1)", "Pane", priority=True, key_display="^t"),
        Binding("f6", "cycle_pane(1)", "Next pane", priority=True, show=False),
        Binding("shift+f6", "cycle_pane(-1)", "Previous pane", priority=True, show=False),
        Binding("f4", "focus_exercise", "Exercise", priority=True, show=False),
        Binding("f7", "question", "Question", priority=True, show=False),
        Binding("ctrl+n", "next", "Next lesson", priority=True, show=False),
        Binding("f8", "stop", "Stop", priority=True, show=False),
        Binding("ctrl+e", "focus_files", "Files", priority=True, show=False),
    ]
    PANES = ("lesson", "editor", "console")

    def __init__(self, lesson: Lesson):
        super().__init__()
        self.lesson = lesson
        self.running = False
        self.active_pane = "lesson"
        self.save_timer = None
        self.execution = None
        self.console: ConsoleSession | None = None
        self.transcript = ""
        self.suspend_saves = False
        self.run_serial = 0
        self.stage: StageName = "build"
        self.check_results: dict[int, CheckEvent] = {}
        self.active_file = lesson.entrypoint
        self.run_files = {}
        self.last_run_sources = {}
        self.check_selected = None
        self.check_details = False
        self.check_selection_explicit = False
        self.file_positions = {}
        self.restoring_view = True
        self.initial_view = {}

    @property
    def build_label(self) -> str:
        return self.lesson.build_label

    def stage_label(self, stage: str | None = None) -> str:
        return self.build_label if (stage or self.stage) == "build" else "Repair"

    def compose(self) -> ComposeResult:
        root = self.store.entry(self.lesson)
        self.stage = root.get("stage", "build")
        if self.stage == "repair" and not self.stage_passed("build"):
            self.stage = "build"
        entry = self.stage_entry()
        sources = self.project_files()
        self.initial_view = safe_view(entry, sources)
        self.active_file = self.initial_view.get("active_file", self.lesson.entrypoint)
        self.file_positions = self.initial_view.get("positions", {})
        yield brand(self.lesson.title.upper())
        with Horizontal(id="lesson-toolbar"):
            yield Button("← Dashboard", id="back")
            if self.lesson.project_id:
                yield Button("Your game", id="game-overview")
            yield Static(self.lesson.title, id="lesson-name", classes="title")
            yield Static("Saved locally", id="save-status", classes="muted")
        with Horizontal(id="stage-navigation"):
            yield Button(
                f"1  {self.build_label}"
                + (" your game" if self.lesson.project_id else " from scratch"),
                id="stage-build",
                variant="primary" if self.stage == "build" else "default",
            )
            yield Button(
                "2  Repair a program",
                id="stage-repair",
                disabled=not self.stage_passed("build"),
                variant="primary" if self.stage == "repair" else "default",
            )
        with Horizontal(id="lesson-body"):
            with VerticalScroll(id="reading-panel"):
                with Vertical(id="lesson-content"):
                    yield Static(
                        f"{self.lesson.minutes} MIN  /  "
                        f"{'PROJECT' if self.lesson.project else 'LESSON'}",
                        classes="eyebrow",
                    )
                    if "code" in entry and entry.get("revision", 1) != self.lesson.revision:
                        yield Static(
                            "This exercise has been updated. Your previous draft is kept below. "
                            f"Reset this stage to restore its original {self.build_label} "
                            "starting code.",
                            id="updated-notice",
                            classes="muted",
                        )
                        yield Button("Reset this stage", id="update-starter")
                    missing = [
                        BY_ID[key].title
                        for key in self.lesson.prerequisites
                        if key in BY_ID
                        and self.store.status(BY_ID[key]) not in ("completed", "familiar")
                    ]
                    if missing:
                        yield Static(
                            "Useful preparation: "
                            + ", ".join(missing)
                            + ". You can continue now or revisit these from the dashboard.",
                            classes="topic-preview",
                        )
                    if self.lesson.project_id:
                        origin = root.get("base_origin", "blank")
                        origins = {
                            "blank": "Your first version starts blank.",
                            ("supplied"): (
                                "Starting from supplied earlier code. Skipped milestones stay "
                                "incomplete."
                            ),
                            ("learner"): (
                                "Continuing your own working "
                                "checkpoint. Earlier source is preserved."
                            ),
                            ("restored"): (
                                "A historical checkpoint was restored "
                                "into this draft. Check it again."
                            ),
                        }
                        yield Static(origins[origin], id="project-origin", classes="topic-preview")
                        yield Static(
                            (
                                "Your game opens checkpoint history, exports, and an explicit "
                                "supplied-base restart."
                            ),
                            classes="muted",
                        )
                    if self.lesson.project_id:
                        from pytuitor.content.lantern.briefs import BRIEFS

                        yield Markdown(
                            BRIEFS[self.lesson.id.removeprefix("reach-")].markdown(),
                            id="milestone-brief",
                        )
                    yield Markdown(self.lesson.body, id="lesson-markdown")
                    if not self.lesson.project_id:
                        from pytuitor.content.lantern.connections import GAME_CONNECTIONS

                        connection = GAME_CONNECTIONS.get(self.lesson.id)
                        if connection:
                            yield Static(
                                "In Lantern Reach: " + connection,
                                classes="topic-preview",
                            )
                    yield Static(
                        "OPTIONAL: CHECK YOUR UNDERSTANDING",
                        classes="eyebrow",
                        id="prediction-heading",
                    )
                    yield Static(Text(self.lesson.prediction), id="prediction")
                    yield OptionList(
                        *[Option(Text(c), id=str(i)) for i, c in enumerate(self.lesson.choices)],
                        id="prediction-choices",
                    )
                    yield Static(id="prediction-feedback", classes="muted")
                    yield Static("HINTS", classes="eyebrow")
                    yield Static(id="hint-copy", classes="muted")
                    yield Button("Next hint  ·  F1", id="hint")
                    yield Button("Reveal reference solution", id="solution")
            with Vertical(id="workbench"):
                with Vertical(id="exercise-card"):
                    yield Static(id="stage-heading", classes="exercise-heading")
                    yield Static(id="stage-transition", classes="exercise-transition")
                    with VerticalScroll(id="exercise-scroll"):
                        yield Markdown(id="stage-instructions", classes="stage-instructions")
                with Horizontal(id="file-toolbar", classes="file-label"):
                    yield Button("Files", id="toggle-files")
                    yield Static(self.active_file, id="active-file", markup=False)
                    yield Button("Tools", id="workspace-tools")
                yield Static(id="file-context", markup=False)
                with Horizontal(id="editor-workspace"):
                    with Vertical(id="file-sidebar"):
                        yield Static("EXPLORER", id="files-heading")
                        yield FileTree()
                        yield Static("▶ Run  * Required", id="file-legend", markup=False)
                    yield CodeEditor.code_editor(
                        sources[self.active_file],
                        language="python",
                        theme="vscode_dark",
                        id="editor",
                    )
                with Horizontal(id="execution-actions"):
                    yield Button("Run", id="run")
                    yield Button("Check  →", id="check", variant="primary")
                    yield Button("Stop", id="stop", disabled=True)
                    yield Button("Play version", id="play-checkpoint")
                    yield Button("Run files", id="run-files", classes="run-files")
                    yield Button("Next  →", id="next", disabled=not self.stage_passed(self.stage))
                with Vertical(id="console-pane"):
                    yield Static(
                        "CONSOLE  ·  Ctrl+R to run  ·  F5 to check",
                        id="console-status",
                        classes="eyebrow",
                    )
                    yield Static("", id="milestone-reward", markup=False, classes="topic-preview")
                    yield Static("", id="check-summary", markup=False)
                    with Horizontal(id="check-actions"):
                        yield Button("Checks", id="choose-check")
                        yield Button("Details", id="check-details")
                        yield Button("Hint", id="check-hint")
                    with VerticalScroll(id="results-scroll"):
                        yield Static(
                            "Run your program to see its output here.\n"
                            "When it asks a question, type your answer and press Enter.",
                            id="results",
                            markup=False,
                        )
                    yield ConsoleInput(
                        placeholder="Type your answer · Enter sends · Ctrl+D ends input",
                        id="console-input",
                        disabled=True,
                        max_length=4096,
                    )
        yield Footer(show_command_palette=False)

    def on_mount(self) -> None:
        self.refresh_file_tree()
        self.query_one("#run-files").display = False
        self.query_one("#check-actions").display = False
        self.query_one("#stop").display = False
        if not self.lesson.choices:
            for selector in (
                "#prediction-heading",
                "#prediction",
                "#prediction-choices",
                "#prediction-feedback",
            ):
                self.query_one(selector).display = False
        self.apply_layout()
        self.show_hints()
        self.update_stage_ui()
        self.query_one("#stage-transition").display = False
        entry = self.store.entry(self.lesson)
        if entry.get("prediction") is True:
            self.query_one("#prediction-feedback", Static).update(
                Text("✓ " + self.lesson.explanation)
            )
        self.call_after_refresh(self.restore_view)

    def remember_file_position(self):
        editor = self.query_one("#editor", TextArea)
        self.file_positions[self.active_file] = {
            "cursor": list(editor.cursor_location),
            "scroll": [int(editor.scroll_x), int(editor.scroll_y)],
        }

    def capture_view(self):
        self.remember_file_position()
        self.stage_entry()["view"] = {
            "active_file": self.active_file,
            "positions": dict(self.file_positions),
            "pane": self.active_pane,
            "focus": self.focused.id if self.focused else None,
            "reading": int(self.query_one("#reading-panel").scroll_y),
            "exercise": int(self.query_one("#exercise-scroll").scroll_y),
            "results": int(self.query_one("#results-scroll").scroll_y),
            "selected": self.check_selected,
            "details": self.check_details,
        }

    def restore_file_position(self):
        editor = self.query_one("#editor", TextArea)
        position = self.file_positions.get(self.active_file, {})
        row, column = position.get("cursor", [0, 0])
        lines = editor.text.split("\n")
        row = min(row, len(lines) - 1)
        column = min(column, len(lines[row]))
        editor.move_cursor((row, column), center=False)
        x, y = position.get("scroll", [0, 0])
        editor.scroll_to(x=x, y=y, animate=False, immediate=True)

    def restore_view(self):
        if not self.is_mounted or self.suspend_saves:
            return
        view = self.initial_view
        self.check_results = {
            case["number"]: case for case in load_report(self.stage_entry(), self.lesson.revision)
        }
        self.check_selected = view.get("selected")
        self.check_selection_explicit = self.check_selected in self.check_results
        self.check_details = view.get("details", False)
        if self.check_results:
            self.render_checks()
            if not report_is_current(self.stage_entry(), self.lesson.revision):
                self.query_one("#check-summary", Static).update(
                    "Earlier results. Draft changed; check again."
                )
        else:
            self.query_one("#check-actions").display = False
        self.select_pane(view.get("pane", "lesson"))
        focus = view.get("focus")
        if focus and self.query(f"#{focus}") and self.query_one(f"#{focus}").display:
            self.query_one(f"#{focus}").focus()
        self.restore_file_position()
        for key, selector in (
            ("reading", "#reading-panel"),
            ("exercise", "#exercise-scroll"),
            ("results", "#results-scroll"),
        ):
            self.query_one(selector).scroll_to(y=view.get(key, 0), animate=False, immediate=True)
        self.restoring_view = False
        self.update_reward()
        self.save_draft()

    @on(Button.Pressed, "#workspace-tools")
    def workspace_tools(self):
        self.app.push_screen(WorkspaceTools(), self.workspace_tool_chosen)

    def workspace_tool_chosen(self, action):
        actions = {
            "add-file": self.action_add_file,
            "environment": self.action_environment,
            "note": self.action_note,
            "export": self.action_export,
            "reset": self.action_reset,
        }
        if action in actions:
            actions[action]()

    def action_note(self):
        note = self.store.entry(self.lesson).get("resume_note", "")
        self.app.push_screen(ResumeNote(note if isinstance(note, str) else ""), self.note_saved)

    def note_saved(self, note):
        if note is not None and self.is_mounted and not self.suspend_saves:
            entry = self.store.entry(self.lesson)
            previous = entry.get("resume_note", "")
            entry["resume_note"] = note
            if not self.tutor.persist():
                entry["resume_note"] = previous
            else:
                self.notify("Note saved for next time." if note else "Note cleared.")

    def update_reward(self):
        if not self.query("#play-checkpoint"):
            return
        root = self.store.entry(self.lesson)
        available = bool(
            self.lesson.project_id
            and root.get("checkpoint")
            and self.stage_passed("build")
            and (self.stage == "build" or self.stage_passed("repair"))
        )
        self.query_one("#play-checkpoint").display = available
        reward = self.query_one("#milestone-reward", Static)
        reward.display = available
        if available:
            from pytuitor.content.lantern.briefs import BRIEFS

            reward.update(BRIEFS[self.lesson.id.removeprefix("reach-")].outcome)

    @on(Button.Pressed, "#play-checkpoint")
    def play_checkpoint(self):
        from pytuitor.project_screen import CheckpointPlayer
        from pytuitor.project_workspace import ProjectWorkspace

        identifier = self.store.entry(self.lesson).get("checkpoint")
        if not identifier or self.running:
            return
        try:
            payload = ProjectWorkspace(self.store).read_checkpoint(identifier)
            self.app.push_screen(CheckpointPlayer(payload))
        except (OSError, WorkspaceError) as error:
            self.notify(str(error), severity="error")

    def project_files(self) -> dict[str, str]:
        entry = self.stage_entry()
        contract = self.stage_contract()
        if "files" not in entry:
            defaults = dict(contract.starter_files or {name: "" for name in contract.files})
            defaults[self.lesson.entrypoint] = entry.get(
                "code", defaults.get(self.lesson.entrypoint, "")
            )
            entry["files"] = defaults
        # A curriculum update may add or rename required files. Keep every old draft.
        entry["files"].setdefault(self.lesson.entrypoint, entry.get("code", ""))
        for name in contract.files:
            entry["files"].setdefault(name, (contract.starter_files or {}).get(name, ""))
        return entry["files"]

    def capture_editor(self) -> dict[str, str]:
        sources = self.project_files()
        sources[self.active_file] = self.query_one("#editor", TextArea).text
        self.stage_entry()["code"] = sources[self.lesson.entrypoint]
        return dict(sources)

    def load_project(self) -> None:
        view = safe_view(self.stage_entry(), self.project_files())
        self.active_file = view.get("active_file", self.lesson.entrypoint)
        self.file_positions = view.get("positions", {})
        self.refresh_file_tree()
        self.load_active_file()
        self.apply_layout()

    def refresh_file_tree(self) -> None:
        self.query_one(FileTree).set_files(
            self.project_files(),
            self.active_file,
            required_files=self.stage_contract().files,
            entrypoint=self.lesson.entrypoint,
        )
        self.update_file_context()

    def update_file_context(self) -> None:
        required = (
            self.active_file == self.lesson.entrypoint
            or self.active_file in self.stage_contract().files
        )
        context = Text("Required file" if required else "Extra file")
        context.append(" · Run starts in ")
        context.append(self.lesson.entrypoint, style="#86bde8")
        label = self.query_one("#file-context", Static)
        label.update(context)
        label.tooltip = context.plain

    def load_active_file(self) -> None:
        label = self.query_one("#active-file", Static)
        label.update(Text(self.active_file))
        label.tooltip = self.active_file
        editor = self.query_one("#editor", TextArea)
        editor.language = "python" if self.active_file.endswith(".py") else None
        editor.load_text(self.project_files()[self.active_file])
        self.restore_file_position()
        self.update_file_context()

    @on(Tree.NodeSelected, "#file-tree")
    def change_file(self, event: Tree.NodeSelected[str]) -> None:
        if event.node.allow_expand or event.node.data not in self.project_files():
            return
        self.open_file(event.node.data)
        self.select_pane("editor")

    def open_file(self, name: str) -> None:
        self.remember_file_position()
        if name == self.active_file:
            return
        self.save_draft()
        self.active_file = name
        self.load_active_file()
        self.query_one(FileTree).mark_active(name)

    @on(Button.Pressed, "#toggle-files")
    def action_toggle_files(self) -> None:
        if len(self.project_files()) < 2:
            return
        sidebar = self.query_one("#file-sidebar")
        if not sidebar.display:
            self.action_focus_files()
            return
        focused = sidebar.has_focus_within
        self.add_class("files-hidden")
        if focused:
            self.select_pane("editor")

    def action_focus_files(self) -> None:
        if len(self.project_files()) < 2:
            self.select_pane("editor")
            return
        self.remove_class("files-hidden")
        self.active_pane = "editor"
        self.apply_layout()
        self.query_one(FileTree).focus()

    @on(Button.Pressed, "#add-file")
    def action_add_file(self) -> None:
        self.app.push_screen(FileDialog(), self.add_file)

    def add_file(self, name: str | None) -> None:
        if not name:
            return
        self.save_draft()
        sources = self.project_files()
        if name in sources:
            self.open_file(name)
            self.select_pane("editor")
            return
        try:
            validate_files({**sources, name: ""})
        except WorkspaceError as exc:
            self.notify(str(exc), severity="error")
            return
        sources[name] = ""
        self.refresh_file_tree()
        self.open_file(name)
        self.select_pane("editor")
        self.tutor.persist()

    def action_remove_file(self) -> None:
        if (
            self.active_file == self.lesson.entrypoint
            or self.active_file in self.stage_contract().files
        ):
            self.notify(
                "This file is required by the exercise. You can clear its contents in the editor."
            )
            return
        self.app.push_screen(DeleteFileDialog(self.active_file), self.remove_file)

    def remove_file(self, confirmed: bool) -> None:
        if not confirmed or not self.export_code():
            return
        self.stop()
        self.project_files().pop(self.active_file)
        self.load_project()
        self.save_draft()

    @on(Button.Pressed, "#solution")
    def action_solution(self) -> None:
        self.stage_entry()["solution_seen"] = True
        self.tutor.persist()
        self.app.push_screen(
            SolutionDialog(self.lesson, self.stage_contract(), self.capture_editor())
        )

    @property
    def environment_path(self):
        return self.store.directory / "environments" / self.lesson.id

    @on(Button.Pressed, "#environment")
    def action_environment(self) -> None:
        self.app.push_screen(EnvironmentDialog(self.environment_path))

    def stage_entry(self) -> DraftState:
        root = self.store.entry(self.lesson)
        return root if self.stage == "build" else root.setdefault("repair", {})

    def stage_contract(self) -> StageContract:
        if self.lesson.project_id:
            from pytuitor.project_catalog import BY_MILESTONE
            from pytuitor.project_workspace import ProjectWorkspace

            return ProjectWorkspace(self.store, self.lesson.project_id).contract(
                BY_MILESTONE[self.lesson.id], self.stage
            )
        return self.lesson.stage_contract(self.stage)

    def stage_passed(self, stage: str) -> bool:
        root = self.store.entry(self.lesson)
        entry = root if stage == "build" else root.get("repair", {})
        passed = entry.get("checked_revision") == self.lesson.revision and "checked_code" in entry
        if self.lesson.project_id:
            passed = passed and entry.get("checked_files") == entry.get("files")
        return passed

    def update_stage_ui(self) -> None:
        self.update_reward()
        for stage in ("build", "repair"):
            label = (
                f"1  {self.build_label}"
                + (" your game" if self.lesson.project_id else " from scratch")
                if stage == "build"
                else "2  Repair a program"
            )
            self.query_one(f"#stage-{stage}", Button).label = (
                label + " ✓" if self.stage_passed(stage) else label
            )
        self.query_one("#stage-build", Button).variant = (
            "primary" if self.stage == "build" else "default"
        )
        self.query_one("#stage-repair", Button).variant = (
            "primary" if self.stage == "repair" else "default"
        )
        self.query_one("#stage-repair", Button).disabled = not self.stage_passed("build")
        default_instructions = (
            "Write the whole program in the blank editor using the Exercise requirements above. "
            "Run it, then Check. Passing unlocks Repair."
            if self.stage == "build"
            else "This separate program contains a mistake. Run and Check to investigate, then "
            f"fix it to meet the requirements. Your {self.build_label} draft is saved separately."
        )
        self.query_one("#stage-heading", Static).update(
            f"1 OF 2 · {self.build_label.upper()} · WRITE AND CHECK"
            if self.stage == "build"
            else "2 OF 2 · REPAIR · INVESTIGATE AND FIX"
        )
        instructions = self.stage_contract().instructions or default_instructions
        if self.stage == "repair":
            from pytuitor.repair_pacing import repair_guidance

            instructions = repair_guidance(self.lesson) + "\n\n" + instructions
        self.query_one("#stage-instructions", Markdown).update(instructions)
        self.query_one("#next", Button).label = "Repair →" if self.stage == "build" else "Next →"
        self.query_one("#next", Button).disabled = not self.stage_passed(self.stage)

    @on(Button.Pressed, "#stage-build, #stage-repair")
    def choose_stage(self, event: Button.Pressed) -> None:
        self.switch_stage(event.button.id.removeprefix("stage-"))

    def switch_stage(self, stage: StageName) -> None:
        if stage == self.stage or self.running:
            return
        if stage == "repair" and not self.stage_passed("build"):
            return
        repair_saved = "code" in self.store.entry(self.lesson).get("repair", {})
        self.save_draft()
        if self.save_timer:
            self.save_timer.stop()
        self.restoring_view = True
        self.stage = stage
        self.check_results = {}
        self.run_files = {}
        self.query_one("#run-files").display = False
        self.store.entry(self.lesson)["stage"] = stage
        self.load_project()
        self.transcript = ""
        if self.stage_passed(stage):
            self.append_output(
                f"{self.stage_label(stage)} draft restored. This stage has passed its checks."
            )
        else:
            self.append_output(
                f"{self.build_label} draft restored."
                if stage == "build"
                else "Repair program loaded. Run to investigate the mistake, then Check your fix."
            )
        self.query_one("#check-summary", Static).update("")
        self.query_one("#console-status", Static).update(
            f"{self.stage_label(stage).upper()} · READY"
        )
        self.update_stage_ui()
        transition = self.query_one("#stage-transition", Static)
        transition.update(
            (
                f"Saved Repair draft restored. {self.build_label} saved."
                if repair_saved
                else f"New Repair program loaded. {self.build_label} saved."
            )
            if stage == "repair"
            else f"Saved {self.build_label} draft restored."
        )
        transition.display = True
        self.query_one("#exercise-scroll", VerticalScroll).scroll_home(animate=False)
        self.show_hints()
        self.initial_view = {
            "pane": "editor",
            **safe_view(self.stage_entry(), self.project_files()),
        }
        self.select_pane(self.initial_view["pane"])
        self.call_after_refresh(self.restore_view)

    def on_resize(self, event: Resize) -> None:
        self.apply_layout()

    def apply_layout(self) -> None:
        multi_file = len(self.project_files()) > 1
        self.set_class(multi_file, "multi-file")
        self.set_class(self.size.width < (120 if multi_file else 100), "narrow")
        for pane in self.PANES:
            self.set_class(self.active_pane == pane, f"show-{pane}")

    def select_pane(self, pane: str) -> None:
        self.active_pane = pane
        self.apply_layout()
        target = {"lesson": "#reading-panel", "editor": "#editor", "console": "#results-scroll"}[
            pane
        ]
        if pane == "console" and self.console and self.console.waiting:
            target = "#console-input"
        # Keep the active pane and focus in sync before accepting another key.
        self.set_focus(self.query_one(target))

    def action_focus_lesson(self) -> None:
        self.select_pane("lesson")

    def on_descendant_focus(self, event: DescendantFocus) -> None:
        # Focus notifications bubble asynchronously and may already be stale.
        if event.widget is not self.focused:
            return
        ids = {event.widget.id, *(parent.id for parent in event.widget.ancestors)}
        for widget_id, pane in (
            ("reading-panel", "lesson"),
            ("editor", "editor"),
            ("file-sidebar", "editor"),
            ("console-pane", "console"),
        ):
            if widget_id in ids:
                self.active_pane = pane
                self.apply_layout()
                break

    def action_focus_exercise(self) -> None:
        self.select_pane("editor")
        self.query_one("#exercise-scroll", VerticalScroll).focus()

    def action_focus_editor(self) -> None:
        self.select_pane("editor")

    def action_focus_console(self) -> None:
        self.select_pane("console")

    def action_cycle_pane(self, direction: int) -> None:
        index = self.PANES.index(self.active_pane)
        self.select_pane(self.PANES[(index + direction) % len(self.PANES)])

    def action_question(self) -> None:
        if not self.lesson.choices:
            self.notify("This lesson uses coding practice without an extra question.")
            return
        self.select_pane("lesson")
        choices = self.query_one("#prediction-choices", OptionList)
        choices.scroll_visible(animate=False)
        choices.focus()

    @on(TextArea.Changed, "#editor")
    def draft_changed(self) -> None:
        if not self.is_mounted or self.suspend_saves or self.restoring_view:
            return
        entry = self.stage_entry()
        if "code" not in entry:
            entry["revision"] = self.lesson.revision
        self.capture_editor()
        if self.lesson.project_id and entry.get("checked_files") != entry.get("files"):
            root = self.store.entry(self.lesson)
            root.pop("completed", None)
            root.pop("completed_revision", None)
        self.update_stage_ui()
        if (
            not self.running
            and self.check_results
            and entry.get("checked_files") != self.project_files()
        ):
            self.query_one("#check-summary", Static).update(
                "Draft changed. Check again to verify your current work."
            )
        self.query_one("#save-status", Static).update("Saving…")
        if self.save_timer:
            self.save_timer.stop()
        self.save_timer = self.set_timer(0.4, self.save_draft)

    def save_draft(self) -> None:
        if (
            self.restoring_view
            or not self.is_mounted
            or self.suspend_saves
            or not self.query("#editor")
        ):
            return
        entry = self.stage_entry()
        if "code" not in entry:
            entry["revision"] = self.lesson.revision
        self.capture_editor()
        self.capture_view()
        saved = self.tutor.persist()
        self.query_one("#save-status", Static).update("Saved locally" if saved else "Not saved")

    def action_save(self) -> None:
        self.save_draft()

    @on(OptionList.OptionSelected, "#prediction-choices")
    def predict(self, event: OptionList.OptionSelected) -> None:
        correct = event.option_index == self.lesson.answer
        self.store.entry(self.lesson)["prediction"] = correct
        self.query_one("#prediction-feedback", Static).update(
            Text(
                ("✓ " + self.lesson.explanation)
                if correct
                else "Not quite. Review the worked example above, then choose again."
            )
        )
        if self.mark_complete():
            self.append_output("\n✓ Lesson complete. Press Ctrl+N to continue.\n")
        self.tutor.persist()

    def mark_complete(self) -> bool:
        complete = self.stage_passed("build") and self.stage_passed("repair")
        if complete:
            entry = self.store.entry(self.lesson)
            entry["completed"] = True
            entry["completed_revision"] = self.lesson.revision
        self.update_stage_ui()
        return complete

    def show_hints(self) -> None:
        hints = self.stage_contract().hints
        count = min(self.stage_entry().get("hints", 0), len(hints))
        text = "\n\n".join(f"{i + 1}. {hint}" for i, hint in enumerate(hints[:count]))
        self.query_one("#hint-copy", Static).update(
            Text(text or "Press F1 for a hint if you get stuck.")
        )
        self.query_one("#hint", Button).disabled = count == len(hints)

    @on(Button.Pressed, "#hint")
    def action_hint(self) -> None:
        entry = self.stage_entry()
        entry["hints"] = min(entry.get("hints", 0) + 1, len(self.stage_contract().hints))
        self.show_hints()
        self.tutor.persist()
        self.select_pane("lesson")
        self.query_one("#hint-copy").scroll_visible(animate=False)

    @on(Button.Pressed, "#run")
    def action_run(self) -> None:
        self.start_execution(False)

    @on(Button.Pressed, "#check")
    def action_check(self) -> None:
        self.start_execution(True)

    def start_execution(self, check: bool) -> None:
        if self.running:
            return
        self.save_draft()
        self.running = True
        self.query_one("#run-files").display = False
        self.run_files = {}
        self.run_serial += 1
        self.transcript = ""
        self.check_results = {}
        self.query_one("#results", Static).update(
            "Checking test cases…" if check else "Starting Python…"
        )
        self.query_one("#run", Button).disabled = True
        self.query_one("#check", Button).disabled = True
        self.query_one("#stop", Button).disabled = False
        self.query_one("#stop").display = True
        self.query_one("#console-status", Static).update(
            "CHECKING TEST CASES" if check else "RUNNING"
        )
        serial = self.run_serial
        self.console = (
            None
            if check
            else ConsoleSession(
                lambda text: self.append_output(text) if serial == self.run_serial else None,
                lambda waiting: (
                    self.input_requested(waiting) if serial == self.run_serial else None
                ),
            )
        )
        self.check_selected = None
        self.check_selection_explicit = False
        self.query_one("#check-actions").display = False
        self.query_one("#check-summary", Static).update("")
        self.select_pane("console")
        self.execution = self.run_code(check, self.run_serial, self.capture_editor())

    def append_output(self, text: str) -> None:
        if not self.is_mounted or self.suspend_saves or not self.query("#results"):
            return
        self.transcript = (self.transcript + text)[-70000:]
        self.query_one("#results", Static).update(self.transcript)
        self.query_one("#results-scroll", VerticalScroll).scroll_end(animate=False)

    def input_requested(self, waiting: bool) -> None:
        if not self.is_mounted or self.suspend_saves or not self.query("#console-input"):
            return
        field = self.query_one("#console-input", Input)
        field.disabled = not waiting
        if waiting:
            self.query_one("#console-status", Static).update(
                "YOUR TURN  ·  Enter sends  ·  Ctrl+D ends input"
            )
            self.select_pane("console")
        elif self.running:
            self.query_one("#console-status", Static).update("RUNNING")

    @on(Input.Submitted, "#console-input")
    def submit_input(self, event: Input.Submitted) -> None:
        if self.console and self.console.submit(event.value):
            self.append_output(event.value + "\n")
            event.input.value = ""

    def end_input(self) -> None:
        if self.console:
            self.console.end_input()
            self.append_output("\n[end of input]\n")
            self.query_one("#console-input", Input).disabled = True

    def show_check(self, case: CheckEvent) -> None:
        if not self.is_mounted or self.suspend_saves or not self.query("#results"):
            return
        self.check_results[case["number"]] = case
        self.render_checks()

    def render_checks(self) -> None:
        if not self.check_selection_explicit:
            first_failure = next(
                (case for case in self.check_results.values() if case.get("passed") is False), None
            )
            if first_failure:
                self.check_selected = first_failure["number"]
        text = render_feedback(
            self.check_results,
            self.check_selected,
            details=self.check_details,
            stage=self.stage_label(),
        )
        self.transcript = text
        self.query_one("#results", Static).update(text)
        self.query_one("#check-actions").display = bool(self.check_results)
        self.query_one("#check-details", Button).label = (
            "Hide details" if self.check_details else "Details"
        )

    @on(Button.Pressed, "#check-details")
    def toggle_check_details(self):
        self.check_details = not self.check_details
        self.render_checks()
        self.save_draft()

    @on(Button.Pressed, "#choose-check")
    def choose_check(self):
        self.app.push_screen(
            CheckChooser(self.check_results.values(), self.check_selected), self.check_chosen
        )

    def check_chosen(self, number):
        if number is not None and number in self.check_results:
            self.check_selected = number
            self.check_selection_explicit = True
            self.render_checks()
            self.query_one("#results-scroll", VerticalScroll).scroll_home(animate=False)
            self.save_draft()

    @on(Button.Pressed, "#check-hint")
    def selected_hint(self):
        from pytuitor.check_feedback import selected_case

        case = selected_case(self.check_results, self.check_selected)
        if case:
            self.notify(case["nudge"], timeout=15)

    @work(exclusive=True, group="execution")
    async def run_code(self, check: bool, serial: int, source: dict[str, str]) -> None:
        try:
            contract = self.stage_contract()
            result = await execute(
                self.lesson,
                source[self.lesson.entrypoint],
                default_input(self.lesson, self.stage),
                check=check,
                files=source,
                stage=contract,
                python=environment_python(self.environment_path)
                if self.environment_path.exists()
                else None,
                console=self.console,
                on_check=lambda case: self.show_check(case) if serial == self.run_serial else None,
            )
            if serial != self.run_serial or self.suspend_saves:
                return
            lines = []
            if check:
                for case in result.checks:
                    self.check_results[case["number"]] = case
                self.render_checks()
                self.stage_entry()["last_check"] = saved_report(
                    result.checks, source, self.lesson.revision
                )
                summary = self.query_one("#check-summary", Static)
                if result.error:
                    lines.extend(["Execution stopped:", result.error])
                if result.passed:
                    if source != self.capture_editor():
                        summary.update("Draft changed. Check your latest edits again.")
                        lines.append(
                            "Checks passed for an earlier draft. Check your latest changes again."
                        )
                    else:
                        if self.lesson.project_id and self.stage == "build":
                            from pytuitor.project_catalog import BY_MILESTONE
                            from pytuitor.project_workspace import ProjectWorkspace

                            try:
                                ProjectWorkspace(self.store, self.lesson.project_id).checkpoint(
                                    BY_MILESTONE[self.lesson.id], source, result.checks
                                )
                            except (OSError, WorkspaceError) as error:
                                summary.update(
                                    "Checks passed, but the "
                                    "checkpoint could not be "
                                    "saved. Check again to "
                                    "retry."
                                )
                                self.append_output(f"\nCheckpoint not saved: {error}")
                                return
                        entry = self.stage_entry()
                        entry["checked_code"] = source[self.lesson.entrypoint]
                        entry["checked_files"] = source
                        entry["checked_revision"] = self.lesson.revision
                        if self.mark_complete():
                            summary.update("Both stages passed. Next: choose Next to continue.")
                            lines.append(
                                "✓ LESSON COMPLETE · Both stages passed. "
                                "Ctrl+N for the next lesson."
                            )
                        else:
                            summary.update(
                                f"{self.build_label} passed. "
                                "Next: choose Repair to investigate a new program."
                            )
                            lines.append(
                                f"✓ {self.build_label.upper()} PASSED · "
                                "Ctrl+N or Repair → opens stage 2."
                            )
                        self.tutor.persist()
                else:
                    failed = next((case for case in result.checks if not case.get("passed")), None)
                    summary.update(
                        "Next: "
                        + (failed["nudge"] if failed else "Read the error, edit, and Check again.")
                    )
                    lines.append(
                        "Some checks did not pass. Review the results above, edit, and Check again."
                    )
            elif result.error:
                lines.extend(
                    ["Python reported an error:", result.error, error_guidance(result.error)]
                )
            else:
                lines.append("Program finished. Use Ctrl+T to switch panes or F5 to check.")
            if not check:
                self.last_run_sources = source
                self.run_files = {
                    name: text for name, text in result.files.items() if source.get(name) != text
                }
                self.query_one("#run-files").display = bool(self.run_files)
                if self.run_files:
                    lines.append(
                        f"{len(self.run_files)} new or changed text files. "
                        "Choose Run files to inspect and keep them."
                    )
                if result.files_notice:
                    lines.append(result.files_notice)
            self.append_output(("\n" if self.transcript else "") + "\n".join(lines))
            if check:
                self.query_one("#results-scroll", VerticalScroll).scroll_home(animate=False)
            self.query_one("#console-status", Static).update(
                "CHECK RESULTS" if check else "FINISHED"
            )
        except (OSError, WorkspaceError) as exc:
            self.append_output(f"\nCould not start Python: {exc}")
        finally:
            if serial == self.run_serial:
                self.running = False
                if self.is_mounted and self.query("#run"):
                    self.query_one("#run", Button).disabled = False
                    self.query_one("#check", Button).disabled = False
                    self.query_one("#stop", Button).disabled = True
                    self.query_one("#stop").display = False
                    self.query_one("#console-input", Input).disabled = True
                    self.update_reward()
                    self.save_draft()

    @on(Button.Pressed, "#run-files")
    def action_run_files(self) -> None:
        if self.run_files:
            self.app.push_screen(RunFilesDialog(self.run_files), self.keep_run_files)

    def keep_run_files(self, files: dict[str, str] | None) -> None:
        if not files or not self.is_mounted or self.running:
            return
        current = self.capture_editor()
        if any(current.get(name) != self.last_run_sources.get(name) for name in files):
            self.notify(
                "A file changed since Run. Run the current draft again before keeping its files."
            )
            return
        try:
            updated = validate_files({**current, **files})
        except WorkspaceError as exc:
            self.notify(str(exc), severity="error")
            return
        if not self.export_code():
            return
        self.stage_entry()["files"] = updated
        self.load_project()
        self.save_draft()
        self.run_files = {}
        self.query_one("#run-files").display = False
        self.notify(
            "Run files saved to this stage. Your previous workspace is backed up in exports."
        )

    @on(Button.Pressed, "#stop")
    def stop(self) -> None:
        if not self.running:
            return
        self.run_serial += 1
        if self.execution:
            self.execution.cancel()
        self.running = False
        self.append_output("\nStopped. You can edit and run again.\n")
        self.query_one("#console-status", Static).update("STOPPED")
        self.query_one("#run", Button).disabled = False
        self.query_one("#check", Button).disabled = False
        self.query_one("#stop", Button).disabled = True
        self.query_one("#stop").display = False
        self.query_one("#console-input", Input).disabled = True

    def action_stop(self) -> None:
        self.stop()

    @on(Button.Pressed, "#back")
    def back(self) -> None:
        self.save_draft()
        self.app.pop_screen()

    @on(Button.Pressed, "#game-overview")
    def game_overview(self) -> None:
        self.save_draft()
        self.tutor.action_game()

    @on(Button.Pressed, "#next")
    def next_lesson(self) -> None:
        if self.running:
            return
        if self.stage == "build":
            if self.stage_passed("build"):
                self.switch_stage("repair")
            else:
                self.notify(f"Pass the {self.build_label} checks to unlock Repair.")
            return
        if not self.stage_passed("repair"):
            self.notify("Pass the Repair checks to complete the lesson.")
            return
        self.save_draft()
        self.store.data["last_lesson"] = self.lesson.id
        following = self.store.next_lesson()
        if following is not None and following.id != self.lesson.id:
            self.tutor.open_activity(following, replace=True)
        else:
            self.app.pop_screen()
            self.notify("Section complete. Open the syllabus to choose another chapter.")

    def action_next(self) -> None:
        self.next_lesson()

    def action_export(self) -> None:
        self.save_draft()
        path = self.export_code()
        if path:
            self.notify(f"Exported to {path}", timeout=12)

    def export_code(self):
        directory = self.store.directory / "exports"
        try:
            directory.mkdir(exist_ok=True)
            stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
            sources = self.capture_editor()
            if len(sources) == 1 and self.lesson.files == ("lesson.py",):
                path = directory / f"{self.lesson.id}-{self.stage}-{stamp}.py"
                with path.open("x", encoding="utf-8") as stream:
                    stream.write(sources[self.lesson.entrypoint])
                return path
            return export_workspace(directory / f"{self.lesson.id}-{self.stage}-{stamp}", sources)
        except (OSError, WorkspaceError) as exc:
            self.notify(f"Could not export: {exc}", severity="error")
            return None

    @on(Button.Pressed, "#update-starter")
    def action_reset(self) -> None:
        self.app.push_screen(
            ConfirmReset(project=bool(self.lesson.project_id)), self.reset_confirmed
        )

    def reset_confirmed(self, confirmed: bool) -> None:
        if not confirmed or not self.export_code():
            return
        self.stop()
        root = self.store.entry(self.lesson)
        root.pop("completed", None)
        root.pop("completed_revision", None)
        if self.stage == "build":
            for key in (
                "code",
                "files",
                "checked_files",
                "checked_code",
                "checked_revision",
                "hints",
                "prediction",
                "view",
                "last_check",
            ):
                root.pop(key, None)
            root["revision"] = self.lesson.revision
            if self.lesson.project_id:
                root["files"] = dict(root["base_files"])
                root["code"] = root["files"][self.lesson.entrypoint]
        else:
            root["repair"] = {"revision": self.lesson.revision}
        self.load_project()
        self.query_one("#prediction-feedback", Static).update("")
        self.query_one("#next", Button).disabled = True
        self.transcript = ""
        self.append_output("Stage reset. Your previous code is backed up in exports.")
        for widget in self.query("#updated-notice, #update-starter"):
            widget.display = False
        self.show_hints()
        self.update_stage_ui()
        self.save_draft()

    def on_unmount(self) -> None:
        if self.save_timer:
            self.save_timer.stop()
