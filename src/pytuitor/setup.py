"""A direct start and an optional prior-knowledge checklist."""

from rich.text import Text
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Button, Footer, SelectionList, Static

from pytuitor.curriculum import CHAPTERS, LESSONS, SECTIONS
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
        self.category_topics = {}
        for section in SECTIONS:
            chapters = {c.id for c in CHAPTERS if c.section_id == section.id}
            self.category_topics[f"category:{section.id}"] = tuple(
                dict.fromkeys(
                    concept
                    for lesson in LESSONS
                    if lesson.chapter_id in chapters and not lesson.project
                    for concept in lesson.concepts
                )
            )

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
                        "Toggle a category to check or clear all its topics. "
                        "All lessons stay available.",
                        classes="muted",
                    )
                    options = []
                    for section in SECTIONS:
                        category = f"category:{section.id}"
                        options.append((section.title, category, False))
                        options.extend(
                            (f"  {concept}", concept, concept in self.store.data["familiar"])
                            for concept in self.category_topics[category]
                        )
                    yield SelectionList(*options, id="onboarding-concepts")
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
        if self.editing:
            self.update_categories()
        self.query_one("#onboarding-concepts" if self.editing else "#begin").focus()

    @on(SelectionList.SelectionToggled, "#onboarding-concepts")
    def toggle_category(self, event: SelectionList.SelectionToggled) -> None:
        topics = self.category_topics.get(event.selection.value)
        if topics is None:
            return
        listing = event.selection_list
        clear = all(topic in listing.selected for topic in topics)
        with listing.prevent(SelectionList.SelectedChanged):
            for topic in topics:
                listing.deselect(topic) if clear else listing.select(topic)
        self.update_categories()

    @on(SelectionList.SelectedChanged, "#onboarding-concepts")
    def update_categories(self) -> None:
        listing = self.query_one("#onboarding-concepts", SelectionList)
        selected = set(listing.selected)
        index = 0
        with listing.prevent(SelectionList.SelectedChanged):
            for section in SECTIONS:
                category = f"category:{section.id}"
                topics = self.category_topics[category]
                count = sum(topic in selected for topic in topics)
                listing.select(category) if count == len(topics) else listing.deselect(category)
                listing.replace_option_prompt_at_index(
                    index, Text(f"{section.title} · {count}/{len(topics)} known", style="bold")
                )
                index += len(topics) + 1

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
        # Keep Home behind the destination without painting it during onboarding.
        with self.app.batch_update():
            self.app.switch_screen(dashboard)
            if browse:
                self.app.push_screen(Syllabus())
            else:
                dashboard.action_continue()

    @on(Button.Pressed, "#cancel-preferences")
    def action_cancel_preferences(self) -> None:
        if self.editing:
            self.app.pop_screen()
