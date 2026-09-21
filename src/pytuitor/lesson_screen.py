"""Lesson reading, code editing, and an interactive Python console."""

from datetime import datetime

from rich.text import Text
from textual import on, work
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.events import DescendantFocus, Resize
from textual.widgets import Button, Footer, Input, Markdown, OptionList, Select, Static, TextArea
from textual.widgets.option_list import Option

from pytuitor.curriculum import BY_ID, Lesson, default_input
from pytuitor.dialogs import ConfirmReset
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

    def compose(self) -> ComposeResult:
        root = self.store.entry(self.lesson)
        self.stage = root.get("stage", "build")
        if self.stage == "repair" and not self.stage_passed("build"):
            self.stage = "build"
        entry = self.stage_entry()
        sources = self.project_files()
        yield brand(self.lesson.title.upper())
        with Horizontal(id="lesson-toolbar"):
            yield Button("← Dashboard", id="back")
            yield Static(self.lesson.title, id="lesson-name", classes="title")
            yield Static("Saved locally", id="save-status", classes="muted")
        with Horizontal(id="stage-navigation"):
            yield Button(
                "1  Build from scratch",
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
                            "Reset this stage if you want to begin with a blank Build editor.",
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
                    yield Markdown(self.lesson.body, id="lesson-markdown")
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
                    yield Select(
                        [(name, name) for name in sources],
                        value=self.active_file,
                        allow_blank=False,
                        id="project-file",
                    )
                    yield Button("+ File", id="add-file")
                    yield Button("Environment", id="environment")
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
                    yield Button("Run files", id="run-files", classes="run-files")
                    yield Button("Next  →", id="next", disabled=not self.stage_passed(self.stage))
                with Vertical(id="console-pane"):
                    yield Static(
                        "CONSOLE  ·  Ctrl+R to run  ·  F5 to check",
                        id="console-status",
                        classes="eyebrow",
                    )
                    yield Static("", id="check-summary", markup=False)
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
        self.query_one("#run-files").display = False
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
        self.save_draft()
        self.select_pane("lesson")

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
        sources = self.project_files()
        self.active_file = self.lesson.entrypoint
        select = self.query_one("#project-file", Select)
        select.set_options([(name, name) for name in sources])
        select.value = self.active_file
        self.query_one("#editor", TextArea).load_text(sources[self.active_file])

    @on(Select.Changed, "#project-file")
    def change_file(self, event: Select.Changed) -> None:
        if event.value == self.active_file or event.value not in self.project_files():
            return
        self.save_draft()
        self.active_file = str(event.value)
        editor = self.query_one("#editor", TextArea)
        editor.language = "python" if self.active_file.endswith(".py") else None
        editor.load_text(self.project_files()[self.active_file])

    @on(Button.Pressed, "#add-file")
    def action_add_file(self) -> None:
        self.app.push_screen(FileDialog(), self.add_file)

    def add_file(self, name: str | None) -> None:
        if not name:
            return
        self.save_draft()
        sources = self.project_files()
        if name in sources:
            self.notify("This file already exists. Choose it from the file menu.")
            return
        try:
            validate_files({**sources, name: ""})
        except WorkspaceError as exc:
            self.notify(str(exc), severity="error")
            return
        sources[name] = ""
        self.query_one("#project-file", Select).set_options([(key, key) for key in sources])
        self.query_one("#project-file", Select).value = name
        self.tutor.persist()

    def action_remove_file(self) -> None:
        if self.active_file in self.stage_contract().files:
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
        return self.lesson.stage_contract(self.stage)

    def stage_passed(self, stage: str) -> bool:
        root = self.store.entry(self.lesson)
        entry = root if stage == "build" else root.get("repair", {})
        return entry.get("checked_revision") == self.lesson.revision and "checked_code" in entry

    def update_stage_ui(self) -> None:
        for stage in ("build", "repair"):
            label = "1  Build from scratch" if stage == "build" else "2  Repair a program"
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
            "fix it to meet the requirements. Your Build draft is saved separately."
        )
        self.query_one("#stage-heading", Static).update(
            "1 OF 2 · BUILD · WRITE AND CHECK"
            if self.stage == "build"
            else "2 OF 2 · REPAIR · INVESTIGATE AND FIX"
        )
        self.query_one("#stage-instructions", Markdown).update(
            self.stage_contract().instructions or default_instructions
        )
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
        self.stage = stage
        self.check_results = {}
        self.run_files = {}
        self.query_one("#run-files").display = False
        self.store.entry(self.lesson)["stage"] = stage
        self.load_project()
        self.transcript = ""
        if self.stage_passed(stage):
            self.append_output(f"{stage.title()} draft restored. This stage has passed its checks.")
        else:
            self.append_output(
                "Build draft restored."
                if stage == "build"
                else "Repair program loaded. Run to investigate the mistake, then Check your fix."
            )
        self.query_one("#check-summary", Static).update("")
        self.query_one("#console-status", Static).update(f"{stage.upper()} · READY")
        self.update_stage_ui()
        transition = self.query_one("#stage-transition", Static)
        transition.update(
            (
                "Saved Repair draft restored. Build saved."
                if repair_saved
                else "New Repair program loaded. Build saved."
            )
            if stage == "repair"
            else "Saved Build draft restored."
        )
        transition.display = True
        self.query_one("#exercise-scroll", VerticalScroll).scroll_home(animate=False)
        self.show_hints()
        self.save_draft()
        self.select_pane("editor")

    def on_resize(self, event: Resize) -> None:
        self.apply_layout()

    def apply_layout(self) -> None:
        self.set_class(self.size.width < 100, "narrow")
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
        if not self.is_mounted or self.suspend_saves:
            return
        entry = self.stage_entry()
        if "code" not in entry:
            entry["revision"] = self.lesson.revision
        self.capture_editor()
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
        if not self.is_mounted or self.suspend_saves or not self.query("#editor"):
            return
        entry = self.stage_entry()
        if "code" not in entry:
            entry["revision"] = self.lesson.revision
        self.capture_editor()
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
        passed = sum(case.get("passed", False) for case in self.check_results.values())
        lines = [
            f"{self.stage.upper()} · {passed}/{len(self.stage_contract().checks)} checks passed",
            "",
        ]
        for case in self.check_results.values():
            status = (
                "RUNNING" if case["status"] == "running" else "PASS" if case["passed"] else "FAIL"
            )
            lines.extend(
                [
                    f"{case['number']}. {status} · {case['label']}",
                    "   Keyboard input: " + case["input"].replace("\n", " ↵ ").rstrip()
                    if case["input"]
                    else "   Keyboard input: none",
                    f"   Test: {case['operation']}",
                    f"   Expected result: {case['expected']}",
                    "   Expected printed output: "
                    + (
                        "final lines " + repr(case["expected_output"])
                        if case.get("expected_output") is not None
                        else "not required; this test checks behavior or a return value"
                    ),
                ]
            )
            if case["status"] == "finished":
                lines.extend(
                    [
                        f"   Actual result: {case['actual']}",
                        f"   Printed output: {case['output']!r}",
                    ]
                )
                if not case["passed"]:
                    lines.append(f"   Hint: {case['nudge']}")
                    guidance = error_guidance(case["actual"])
                    if guidance:
                        lines.append("   Why: " + guidance)
            lines.append("")
        self.transcript = ""
        self.append_output("\n".join(lines))

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
                                "Build passed. Next: choose Repair to investigate a new program."
                            )
                            lines.append("✓ BUILD PASSED · Ctrl+N or Repair → opens stage 2.")
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
                    self.query_one("#console-input", Input).disabled = True

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
        self.query_one("#console-input", Input).disabled = True

    def action_stop(self) -> None:
        self.stop()

    @on(Button.Pressed, "#back")
    def back(self) -> None:
        self.save_draft()
        self.app.pop_screen()

    @on(Button.Pressed, "#next")
    def next_lesson(self) -> None:
        if self.running:
            return
        if self.stage == "build":
            if self.stage_passed("build"):
                self.switch_stage("repair")
            else:
                self.notify("Pass the Build checks to unlock Repair.")
            return
        if not self.stage_passed("repair"):
            self.notify("Pass the Repair checks to complete the lesson.")
            return
        self.save_draft()
        self.store.data["last_lesson"] = self.lesson.id
        following = self.store.next_lesson()
        if following is not None and following.id != self.lesson.id:
            self.store.data["last_lesson"] = following.id
            if self.tutor.persist():
                self.app.switch_screen(LessonScreen(following))
            else:
                self.store.data["last_lesson"] = self.lesson.id
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
        self.app.push_screen(ConfirmReset(), self.reset_confirmed)

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
            ):
                root.pop(key, None)
            root["revision"] = self.lesson.revision
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
