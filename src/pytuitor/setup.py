"""A direct start and an optional prior-knowledge checklist."""

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Button, Footer, SelectionList, Static

from pytuitor.curriculum import CONCEPTS
from pytuitor.ui import TutorScreen, brand


class Onboarding(TutorScreen):
    BINDINGS = [
        Binding("f5,ctrl+enter", "begin", "Save / start", priority=True),
        Binding("escape", "cancel_preferences", "Cancel", show=False),
    ]

    def __init__(self, editing: bool = False):
        super().__init__()
        self.editing = editing
        self.set_class(editing, "editing")

    def compose(self) -> ComposeResult:
        yield brand("KNOWN TOPICS" if self.editing else "WELCOME")
        with VerticalScroll(id="onboarding-scroll"):
            with Vertical(id="onboarding-card"):
                yield Static(
                    "Skip what you already know"
                    if self.editing
                    else "Learn Python at your own pace.",
                    classes="hero",
                )
                if self.editing:
                    yield Static(
                        "Continue skips a lesson when all its concepts are checked. "
                        "You can still open any lesson from the syllabus or dashboard.",
                        classes="muted",
                    )
                    yield SelectionList(
                        *[(c, c, c in self.store.data["familiar"]) for c in CONCEPTS],
                        id="onboarding-concepts",
                    )
                else:
                    yield Static(
                        "Progress is saved locally. No account or internet needed.",
                        classes="muted intro",
                    )
                    yield Static(
                        "Start with Foundations, then learn everyday Python "
                        "and build useful programs.\n\n"
                        "Already programming? Browse the syllabus and open any chapter. "
                        "Python depth and specialized topics are optional.",
                        classes="topic-preview",
                    )
                with Horizontal(classes="actions"):
                    yield Button(
                        "Save topics" if self.editing else "Start learning →",
                        id="begin",
                        variant="primary",
                    )
                    if self.editing:
                        yield Button("Cancel", id="cancel-preferences")
                    else:
                        yield Button("Browse syllabus", id="browse-syllabus")
        yield Footer(show_command_palette=False)

    def on_mount(self) -> None:
        self.query_one("#onboarding-concepts" if self.editing else "#begin").focus()

    @on(Button.Pressed, "#begin")
    async def action_begin(self) -> None:
        if self.editing:
            previous = list(self.store.data["familiar"])
            self.store.set_familiar(self.query_one("#onboarding-concepts", SelectionList).selected)
            if not self.tutor.persist():
                self.store.data["familiar"] = previous
                return
            self.app.pop_screen()
        else:
            await self.start(browse=False)

    @on(Button.Pressed, "#browse-syllabus")
    async def browse_syllabus(self) -> None:
        await self.start(browse=True)

    async def start(self, *, browse: bool) -> None:
        from pytuitor.screens import Dashboard
        from pytuitor.syllabus import Syllabus

        self.store.data["onboarded"] = True
        if not self.tutor.persist():
            self.store.data["onboarded"] = False
            return
        dashboard = Dashboard()
        self.app.switch_screen(dashboard)
        if browse:
            dashboard.call_after_refresh(self.app.push_screen, Syllabus())
        else:
            dashboard.call_after_refresh(dashboard.action_continue)

    @on(Button.Pressed, "#cancel-preferences")
    def action_cancel_preferences(self) -> None:
        if self.editing:
            self.app.pop_screen()
