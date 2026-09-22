"""Application shell and navigation."""

from collections.abc import Iterable
from pathlib import Path

from textual.app import App, SystemCommand
from textual.binding import Binding
from textual.screen import Screen
from textual.theme import Theme

from pytuitor.state import Store


class TutorApp(App):
    TITLE = "pytuitor"
    SUB_TITLE = "A little practice. A lot of possibility."
    CSS_PATH = "theme.tcss"
    BINDINGS = [
        Binding("f10", "keyboard_help", "Keybinds", priority=True),
        Binding("ctrl+p", "command_palette", "Commands", priority=True),
        Binding("ctrl+b", "dashboard", "Home", priority=True),
        Binding("ctrl+q", "quit", "Quit", priority=True),
    ]

    def __init__(self, data_dir: Path | None = None):
        super().__init__()
        self.store = Store(data_dir)

    def on_mount(self) -> None:
        from pytuitor.screens import Dashboard, Onboarding

        self.register_theme(
            Theme(
                name="pytuitor",
                primary="#3776ab",
                secondary="#ffd343",
                accent="#3776ab",
                foreground="#dddcd7",
                background="#151719",
                surface="#1c1f22",
                panel="#222629",
                success="#a2c5a2",
                warning="#ffd343",
                error="#e39393",
                dark=True,
                variables={
                    "footer-background": "#151719",
                    "footer-key-foreground": "#ffd343",
                    "block-cursor-foreground": "#151719",
                    "block-cursor-background": "#ffd343",
                },
            )
        )
        self.theme = "pytuitor"
        self.push_screen(Dashboard() if self.store.data["onboarded"] else Onboarding())

    def persist(self) -> bool:
        try:
            self.store.save()
            if self.store.durability_warning:
                self.notify(self.store.durability_warning, severity="warning", timeout=10)
            return True
        except OSError as exc:
            self.notify(f"Could not save progress: {exc}", severity="error", timeout=10)
            return False

    def action_dashboard(self) -> None:
        from pytuitor.screens import Dashboard, LessonScreen

        if not self.store.data["onboarded"] or isinstance(self.screen, Dashboard):
            return
        for screen in self.screen_stack:
            if isinstance(screen, LessonScreen):
                screen.save_draft()
        while len(self.screen_stack) > 2:
            self.pop_screen()
        if not isinstance(self.screen, Dashboard):
            self.switch_screen(Dashboard())

    def action_quit(self) -> None:
        from pytuitor.screens import LessonScreen

        for screen in self.screen_stack:
            if isinstance(screen, LessonScreen):
                screen.save_draft()
        if self.persist():
            self.exit()

    def on_unmount(self) -> None:
        self.store.close()

    def action_keyboard_help(self) -> None:
        from pytuitor.dialogs import KeyboardHelp

        if isinstance(self.screen, KeyboardHelp):
            self.pop_screen()
        else:
            self.push_screen(KeyboardHelp())

    def action_restart(self) -> None:
        from pytuitor.dialogs import ConfirmRestart

        self.push_screen(ConfirmRestart(), self.restart_confirmed)

    def restart_confirmed(self, confirmed: bool) -> None:
        from pytuitor.screens import LessonScreen
        from pytuitor.setup import Onboarding

        if not confirmed:
            return
        for screen in self.screen_stack:
            if isinstance(screen, LessonScreen):
                screen.stop()
                if screen.save_timer:
                    screen.save_timer.stop()
        try:
            self.store.reset()
        except OSError as exc:
            self.notify(f"Could not reset progress: {exc}", severity="error")
            return
        for screen in self.screen_stack:
            if isinstance(screen, LessonScreen):
                screen.suspend_saves = True
        while len(self.screen_stack) > 2:
            self.pop_screen()
        self.switch_screen(Onboarding())

    def get_system_commands(self, screen: Screen) -> Iterable[SystemCommand]:
        from pytuitor.dialogs import ExecutionInfo
        from pytuitor.screens import LessonScreen
        from pytuitor.setup import Onboarding

        yield SystemCommand(
            "Execution and privacy",
            "Understand local code access and explicit network actions",
            lambda: self.push_screen(ExecutionInfo()),
        )
        yield SystemCommand(
            "Dashboard", "Continue your chapter or revisit lessons", self.action_dashboard
        )
        if self.store.data["onboarded"]:
            yield SystemCommand(
                "Known topics",
                "Choose which familiar concepts Continue skips",
                lambda: self.push_screen(Onboarding(editing=True)),
            )
        yield SystemCommand(
            "Keyboard help", "All navigation and editor shortcuts", self.action_keyboard_help
        )
        if self.store.data["onboarded"]:
            yield SystemCommand(
                "Start over", "Erase progress and return to onboarding", self.action_restart
            )
        if isinstance(screen, LessonScreen):
            if len(screen.project_files()) > 1:
                yield SystemCommand(
                    "Focus files", "Show the workspace explorer", screen.action_focus_files
                )
                yield SystemCommand(
                    "Toggle file explorer",
                    "Show or hide the compact sidebar",
                    screen.action_toggle_files,
                )
            yield SystemCommand(
                "Project environment",
                "Create a venv or explicitly install a package",
                screen.action_environment,
            )
            yield SystemCommand(
                "Add project file",
                "Create a file in this stage's workspace",
                screen.action_add_file,
            )
            yield SystemCommand(
                "Remove project file",
                "Back up the workspace and remove the selected file",
                screen.action_remove_file,
            )
            yield SystemCommand(
                "Reveal reference solution",
                "Compare one correct approach without replacing your draft",
                screen.action_solution,
            )
            yield SystemCommand(
                "Focus lesson", "Read and scroll the explanation", screen.action_focus_lesson
            )
            yield SystemCommand(
                "Exercise requirements",
                "Focus and scroll the complete stage specification",
                screen.action_focus_exercise,
            )
            yield SystemCommand("Focus editor", "Write Python code", screen.action_focus_editor)
            yield SystemCommand(
                "Focus console", "Read output or type an answer", screen.action_focus_console
            )
            yield SystemCommand(
                "Lesson question", "Answer the prediction question", screen.action_question
            )
            yield SystemCommand(
                "Run program", "Run with interactive keyboard input", screen.action_run
            )
            yield SystemCommand("Check exercise", "Run automated test cases", screen.action_check)
            yield SystemCommand(
                "Next lesson", "Continue after completing this lesson", screen.next_lesson
            )
            yield SystemCommand(
                "Export code",
                "Save this stage's complete workspace in your profile's exports folder",
                screen.action_export,
            )
            yield SystemCommand(
                "Reset exercise",
                "Back up and reset the current Build or Repair stage",
                screen.action_reset,
            )
        yield SystemCommand("Quit", "Save your work and close Pytuitor", self.action_quit)
