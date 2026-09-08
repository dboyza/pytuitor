"""The learning experience: onboarding, dashboard, and lesson workspace."""

from rich.text import Text
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.events import Click, Resize
from textual.widgets import (
    Button,
    Footer,
    OptionList,
    Select,
    Static,
)
from textual.widgets.option_list import Option

from pytuitor.curriculum import (
    BY_ID,
    CHAPTERS,
    LESSONS,
    Lesson,
    chapter_lessons,
)
from pytuitor.lesson_screen import LessonScreen
from pytuitor.setup import Onboarding
from pytuitor.ui import TutorScreen, brand


class LessonList(OptionList):
    async def _on_click(self, event: Click) -> None:
        event.prevent_default()
        index = event.style.meta.get("option")
        if index is not None and not self.get_option_at_index(index).disabled:
            self.highlighted = index
            if event.chain == 2:
                self.action_select()
        event.stop()


class Dashboard(TutorScreen):
    BINDINGS = [
        Binding("c", "continue", "Continue"),
        Binding("p", "preferences", "Known topics"),
        Binding("s", "syllabus", "Syllabus", show=False),
    ]

    def __init__(self):
        super().__init__()
        self.current: Lesson | None = None
        self.chapter_id: str | None = None
        self.seen_last_lesson: str | None = None

    def compose(self) -> ComposeResult:
        yield brand("LEARNING")
        with Horizontal(id="dashboard-body"):
            with Vertical(id="dashboard-main"):
                with Horizontal(id="path-header"):
                    yield Static(id="path-title", classes="hero")
                    yield Button("Syllabus", id="syllabus")
                    yield Button("Known topics", id="preferences")
                yield Static(id="dashboard-summary", classes="muted")
                with Horizontal(id="resume-card"):
                    yield Static(id="continue-summary")
                    yield Button("Continue →", id="continue", variant="primary")
                yield Select(
                    [("Your lessons", "")], value="", allow_blank=False, id="chapter-picker"
                )
                yield Static(id="chapter-outcome", classes="muted")
                yield Static("Lessons in this chapter", id="course-heading", classes="title")
                yield LessonList(id="lesson-list")
                yield Static(
                    "↑ ↓ select · Enter or double-click opens · Known lessons stay available",
                    id="lesson-list-help",
                    classes="muted",
                )
                with Horizontal(id="dashboard-bottom"):
                    yield Static("Saved locally", classes="muted")
                    yield Button("Start over", id="restart")
        yield Footer(show_command_palette=False)

    def on_mount(self) -> None:
        self.refresh_dashboard()
        self.query_one("#lesson-list", OptionList).focus()

    def on_screen_resume(self) -> None:
        if self.is_mounted:
            self.refresh_dashboard()

    def on_resize(self, event: Resize) -> None:
        self.set_class(event.size.width < 100, "narrow")
        if self.is_mounted and self.query("#lesson-list"):
            self.show_course()

    def refresh_dashboard(self) -> None:
        last_lesson = self.store.data.get("last_lesson")
        if last_lesson != self.seen_last_lesson and last_lesson in BY_ID:
            self.chapter_id = BY_ID[last_lesson].chapter_id
            self.current = BY_ID[last_lesson]
        self.seen_last_lesson = last_lesson
        lessons = LESSONS
        completed = sum(self.store.status(lesson) == "completed" for lesson in lessons)
        familiar = sum(self.store.status(lesson) == "familiar" for lesson in lessons)
        self.query_one("#path-title", Static).update("Learning")
        self.query_one("#dashboard-summary", Static).update(
            f"{completed} of {len(lessons)} completed"
            + (f" · {familiar} already known" if familiar else "")
        )
        next_lesson = self.store.next_lesson()
        self.query_one("#continue-summary", Static).update(
            Text(f"UP NEXT\n{next_lesson.title} · {next_lesson.minutes} min")
            if next_lesson
            else Text("CHOOSE YOUR NEXT CHAPTER\nOpen the syllabus to explore more topics.")
        )
        self.query_one("#continue", Button).disabled = next_lesson is None
        chapters = CHAPTERS
        if self.chapter_id not in {chapter.id for chapter in chapters}:
            self.chapter_id = next_lesson.chapter_id if next_lesson else None
            if not self.chapter_id and chapters:
                self.chapter_id = chapters[0].id
        picker = self.query_one("#chapter-picker", Select)
        picker.set_options(
            [
                (f"Chapter {index}: {chapter.title}", chapter.id)
                for index, chapter in enumerate(chapters, 1)
            ]
            or [("Your lessons", "")]
        )
        picker.value = self.chapter_id or ""
        self.show_course()

    @on(Select.Changed, "#chapter-picker")
    def chapter_changed(self, event: Select.Changed) -> None:
        if (
            event.value == Select.BLANK
            or event.value != self.query_one("#chapter-picker", Select).value
        ):
            return
        self.chapter_id = str(event.value)
        self.show_course()

    def show_course(self) -> None:
        lessons = chapter_lessons(self.chapter_id) if self.chapter_id else LESSONS
        chapter = next((c for c in CHAPTERS if c.id == self.chapter_id), None)
        self.query_one("#chapter-outcome", Static).update(chapter.outcome if chapter else "")
        listing = self.query_one("#lesson-list", OptionList)
        selected_id = self.current.id if self.current else None
        listing.clear_options()
        symbols = {"new": "○", "in progress": "◐", "familiar": "✓", "completed": "✓"}
        for index, lesson in enumerate(lessons):
            status = self.store.status(lesson)
            text = Text()
            text.append(f"{symbols[status]}  {index + 1:02}  {lesson.title}", style="bold")
            label = "known · skipped" if status == "familiar" else status
            kind = "project · " if lesson.project else ""
            if self.size.width < 100:
                detail = (
                    "known"
                    if status == "familiar"
                    else "project"
                    if lesson.project and not lesson.title.lower().startswith("project:")
                    else ""
                )
                if detail:
                    text.append(f" · {detail}", style="#8f999c")
            else:
                text.append(f"\n       {kind}{lesson.minutes} min · {label}", style="#8f999c")
            listing.add_option(Option(text, id=lesson.id))
        selected = next((i for i, lesson in enumerate(lessons) if lesson.id == selected_id), 0)
        listing.highlighted = selected
        self.current = lessons[selected] if lessons else None

    @on(OptionList.OptionHighlighted, "#lesson-list")
    def highlight_lesson(self, event: OptionList.OptionHighlighted) -> None:
        if event.option.id in BY_ID:
            self.current = BY_ID[event.option.id]

    @on(OptionList.OptionSelected, "#lesson-list")
    def select_lesson(self, event: OptionList.OptionSelected) -> None:
        self.open_lesson(BY_ID[event.option.id])

    def open_lesson(self, lesson: Lesson) -> None:
        previous = self.store.data.get("last_lesson")
        self.store.data["last_lesson"] = lesson.id
        if not self.tutor.persist():
            self.store.data["last_lesson"] = previous
            return
        self.chapter_id = lesson.chapter_id
        self.app.push_screen(LessonScreen(lesson))

    @on(Button.Pressed, "#continue")
    def action_continue(self) -> None:
        lesson = self.store.next_lesson()
        if lesson:
            self.open_lesson(lesson)
        else:
            self.notify("Choose your next chapter in the syllabus.")

    @on(Button.Pressed, "#preferences")
    def action_preferences(self) -> None:
        self.app.push_screen(Onboarding(editing=True))

    @on(Button.Pressed, "#syllabus")
    def action_syllabus(self) -> None:
        from pytuitor.syllabus import Syllabus

        self.app.push_screen(Syllabus())

    @on(Button.Pressed, "#restart")
    def restart(self) -> None:
        self.tutor.action_restart()
