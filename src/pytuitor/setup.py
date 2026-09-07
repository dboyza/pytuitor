"""Direct path selection and prior-knowledge checklists."""

from rich.text import Text
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Button, Footer, Label, Select, SelectionList, Static

from pytuitor.curriculum import CONCEPTS, track_chapters, track_lessons
from pytuitor.ui import TutorScreen, brand


class Onboarding(TutorScreen):
    BINDINGS = [
        Binding("f5,ctrl+enter", "begin", "Save / start", priority=True),
        Binding("escape", "cancel_preferences", "Cancel", show=False),
    ]

    def __init__(self, editing: bool = False):
        super().__init__()
        self.editing = editing

    def compose(self) -> ComposeResult:
        yield brand("EDIT YOUR PATH" if self.editing else "CHOOSE WHERE TO START")
        with VerticalScroll(id="onboarding-scroll"):
            with Vertical(id="onboarding-card"):
                yield Static(
                    "Your path and known topics"
                    if self.editing
                    else "Learn Python at your own pace.",
                    classes="hero",
                )
                yield Static(
                    "Progress is always saved.\nEverything stays on your machine.",
                    classes="muted intro",
                )
                yield Label("CHOOSE A PATH", classes="eyebrow")
                yield Select(
                    [
                        ("Beginner - learn programming from the beginning", "beginner"),
                        ("Experienced - learn how Python works", "experienced"),
                        ("Custom - skip Python topics I already know", "custom"),
                    ],
                    value=self.store.data["track"],
                    allow_blank=False,
                    id="path",
                )
                yield Static(id="path-description", classes="muted")
                yield Static(id="path-topics", classes="topic-preview")
                yield Label("ALREADY KNOW SOME OF THIS?", classes="eyebrow")
                yield Static(
                    "Check the concepts you already know. Continue skips a lesson when all its "
                    "concepts are checked. You can still open it from the dashboard.",
                    classes="muted",
                )
                yield SelectionList(
                    *[(c, c, c in self.store.data["familiar"]) for c in CONCEPTS],
                    id="onboarding-concepts",
                )
                with Horizontal(classes="actions"):
                    yield Button(
                        "Save path" if self.editing else "Start learning  →",
                        id="begin",
                        variant="primary",
                    )
                    if self.editing:
                        yield Button("Cancel", id="cancel-preferences")
                yield Static(
                    "You can change paths or update this checklist anytime.", classes="muted"
                )
        yield Footer(show_command_palette=False)

    def on_mount(self) -> None:
        self.update_preview()
        self.query_one("#path", Select).focus()

    @on(Select.Changed, "#path")
    def path_changed(self) -> None:
        self.update_preview()

    def update_preview(self) -> None:
        track = self.query_one("#path", Select).value
        descriptions = {
            "beginner": "No programming experience needed. "
            "Build useful command-line tools and automation, from first values to tested projects.",
            "experienced": "For people who already program. "
            "Explore Python's behavior, features, and tools.",
            "custom": "Both paths in order, skipping what you know. "
            "Start with the checklist below.",
        }
        self.query_one("#path-description", Static).update(descriptions[track])
        chapters = track_chapters(track)
        preview = (
            "\n".join(
                f"{index:02}  {chapter.title}\n      {chapter.outcome}"
                for index, chapter in enumerate(chapters, 1)
            )
            if chapters
            else "\n".join(
                f"{index:02}  {lesson.title}"
                for index, lesson in enumerate(track_lessons(track), 1)
            )
        )
        self.query_one("#path-topics", Static).update(Text(preview))

    @on(Button.Pressed, "#begin")
    def action_begin(self) -> None:
        from pytuitor.screens import Dashboard

        self.store.data.update({"track": self.query_one("#path", Select).value, "onboarded": True})
        self.store.set_familiar(self.query_one("#onboarding-concepts", SelectionList).selected)
        if not self.tutor.persist():
            return
        if self.editing:
            self.app.pop_screen()
        else:
            self.app.switch_screen(Dashboard())

    @on(Button.Pressed, "#cancel-preferences")
    def action_cancel_preferences(self) -> None:
        if self.editing:
            self.app.pop_screen()
