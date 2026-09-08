"""The learning experience: onboarding, dashboard, and lesson workspace."""

from rich.text import Text
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.events import Click, Resize
from textual.screen import ModalScreen
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
    TRACKS,
    Lesson,
    track_chapters,
    track_lessons,
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


class ReviewDialog(ModalScreen[Lesson | None]):
    BINDINGS = [Binding("escape", "close", "Close")]
    DEFAULT_CSS = """
    #review-dialog { height: 80%; }
    #review-list { height: 1fr; min-height: 4; margin: 1 0; }
    """

    def compose(self) -> ComposeResult:
        reviews = self.app.store.due_reviews(include_future=True)
        due = {lesson.id for lesson in self.app.store.due_reviews()}
        with VerticalScroll(classes="dialog", id="review-dialog"):
            yield Static("Optional practice", classes="title")
            yield Static(
                "Fresh exercises revisit completed chapters. Practice whenever you like; "
                "unfinished drafts are saved. Completed practice starts fresh next time."
            )
            yield LessonList(
                *[
                    Option(
                        Text(
                            f"{lesson.title}\n"
                            + ("Due now" if lesson.id in due else "Scheduled - practice anytime")
                        ),
                        id=lesson.id,
                    )
                    for lesson in reviews
                ],
                id="review-list",
            )
            if not reviews:
                yield Static("Complete a chapter project to add its practice here.")
            yield Button("Close", id="close-review")

    def on_mount(self) -> None:
        self.query_one("#review-list", OptionList).focus()

    @on(OptionList.OptionSelected, "#review-list")
    def choose(self, event: OptionList.OptionSelected) -> None:
        self.dismiss(BY_ID[event.option.id])

    @on(Button.Pressed, "#close-review")
    def action_close(self) -> None:
        self.dismiss(None)


class Dashboard(TutorScreen):
    BINDINGS = [
        Binding("c", "continue", "Continue"),
        Binding("p", "preferences", "Edit path"),
        Binding("s", "syllabus", "Syllabus", show=False),
    ]

    def __init__(self):
        super().__init__()
        self.track = "beginner"
        self.current: Lesson | None = None
        self.chapter_id: str | None = None

    def compose(self) -> ComposeResult:
        self.track = self.store.data["track"]
        yield brand("YOUR LEARNING PATH")
        with Horizontal(id="dashboard-body"):
            with Vertical(id="dashboard-main"):
                with Horizontal(id="path-header"):
                    yield Static(id="path-title", classes="hero")
                    yield Button("Syllabus", id="syllabus")
                    yield Button("Edit path", id="preferences")
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
                    yield Button("Practice", id="review")
                    yield Button("Study notes", id="study-notes")
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
        track = self.store.data["track"]
        if track != self.track:
            self.chapter_id = None
            self.current = None
        self.track = track
        lessons = track_lessons(self.track)
        completed = sum(self.store.status(lesson) == "completed" for lesson in lessons)
        familiar = sum(self.store.status(lesson) == "familiar" for lesson in lessons)
        self.query_one("#path-title", Static).update(f"Your {TRACKS[self.track].lower()} path")
        self.query_one("#dashboard-summary", Static).update(
            f"{completed} of {len(lessons)} completed"
            + (f" · {familiar} already known" if familiar else "")
        )
        next_lesson = self.store.next_lesson()
        self.query_one("#continue-summary", Static).update(
            Text(f"UP NEXT\n{next_lesson.title} · {next_lesson.minutes} min")
            if next_lesson
            else Text(
                "PATH COMPLETE\nRevisit a lesson, or use Edit path to choose what comes next."
            )
        )
        self.query_one("#continue", Button).disabled = next_lesson is None
        chapters = track_chapters(self.track)
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
        due_count = len(self.store.due_reviews())
        self.query_one("#review", Button).label = (
            f"Practice ({due_count})" if due_count else "Practice"
        )
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
        lessons = [
            lesson
            for lesson in track_lessons(self.track)
            if not self.chapter_id or lesson.chapter_id == self.chapter_id
        ]
        chapter = next((c for c in track_chapters(self.track) if c.id == self.chapter_id), None)
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
        if not lesson.review_of:
            self.store.data["last_lesson"] = lesson.id
            self.chapter_id = lesson.chapter_id
        if not self.tutor.persist():
            return
        self.app.push_screen(LessonScreen(lesson))

    @on(Button.Pressed, "#continue")
    def action_continue(self) -> None:
        lesson = self.store.next_lesson()
        if lesson:
            self.open_lesson(lesson)
        else:
            self.notify("Your path is complete. Revisit a lesson or choose Edit path.")

    @on(Button.Pressed, "#preferences")
    def action_preferences(self) -> None:
        self.app.push_screen(Onboarding(editing=True))

    @on(Button.Pressed, "#syllabus")
    def action_syllabus(self) -> None:
        from pytuitor.syllabus import Syllabus

        self.app.push_screen(Syllabus())

    @on(Button.Pressed, "#review")
    def review(self) -> None:
        self.app.push_screen(ReviewDialog(), self.open_review)

    def open_review(self, lesson: Lesson | None) -> None:
        if lesson is None:
            return
        entry = self.store.entry(lesson)
        if entry.get("completed"):
            previous = entry.copy()
            entry.clear()
            if not self.tutor.persist():
                entry.update(previous)
                return
        self.open_lesson(lesson)

    @on(Button.Pressed, "#study-notes")
    def study_notes(self) -> None:
        from pytuitor.learning_tools import FeedbackDialog

        self.app.push_screen(FeedbackDialog())

    @on(Button.Pressed, "#restart")
    def restart(self) -> None:
        self.tutor.action_restart()
