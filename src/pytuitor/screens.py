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
    ACTIVITIES,
    BY_ID,
    CHAPTERS,
    SECTIONS,
    Lesson,
    chapter_activities,
)
from pytuitor.learning_progress import progress_counts, resume_summary
from pytuitor.lesson_screen import LessonScreen as LessonScreen
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
        Binding("g", "game", "Your game", show=False),
        Binding("r", "app.review", "Review", show=False),
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
                    yield Button("Your game", id="your-game")
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
                    yield Button("Review", id="review")
                    yield Button("Start over", id="restart")
        yield Footer(show_command_palette=False)

    @on(Button.Pressed, "#review")
    def open_review(self):
        self.tutor.action_review()

    def on_mount(self) -> None:
        self.apply_layout()
        self.refresh_dashboard()
        self.query_one("#lesson-list", OptionList).focus()

    def on_screen_resume(self) -> None:
        if self.is_mounted:
            self.refresh_dashboard()

    def on_resize(self, event: Resize) -> None:
        self.apply_layout()
        if self.is_mounted and self.query("#lesson-list"):
            self.show_course()

    def apply_layout(self) -> None:
        self.set_class(self.size.width < 100 or self.size.height < 36, "compact")

    def refresh_dashboard(self) -> None:
        last_lesson = self.store.data.get("last_lesson")
        if last_lesson != self.seen_last_lesson and last_lesson in BY_ID:
            self.chapter_id = BY_ID[last_lesson].chapter_id
            self.current = BY_ID[last_lesson]
        self.seen_last_lesson = last_lesson
        lessons = ACTIVITIES
        core, optional = progress_counts(self.store, lessons)
        self.query_one("#path-title", Static).update("Learning")
        self.query_one("#dashboard-summary", Static).update(
            f"Core {core[0]}/{core[2]} completed"
            + (f" · {core[1]} known" if core[1] else "")
            + f" · Optional {optional[0]}/{optional[2]}"
            + (f" · {optional[1]} known" if optional[1] else "")
        )
        next_lesson = self.store.next_lesson()
        self.query_one("#continue-summary", Static).update(
            Text(
                f"UP NEXT · {next_lesson.minutes} min\n{next_lesson.title}\n"
                f"{resume_summary(self.store, next_lesson)}"
            )
            if next_lesson
            else Text("CHOOSE YOUR NEXT CHAPTER\nOpen the syllabus to explore more topics.")
        )
        self.query_one("#continue", Button).disabled = next_lesson is None
        root = (
            self.store.entry(next_lesson)
            if next_lesson and self.store.status(next_lesson) == "in progress"
            else {}
        )
        note = root.get("resume_note", "")
        self.query_one("#continue-summary").tooltip = (
            ("Your note: " + note) if isinstance(note, str) and note else None
        )
        from pytuitor.review_progress import suggested

        suggestion = suggested(self.store)
        self.query_one("#review", Button).label = "Review suggested" if suggestion else "Review"
        if isinstance(note, str) and note:
            self.query_one("#continue-summary", Static).update(
                Text(
                    f"UP NEXT · {next_lesson.title}\n"
                    f"{resume_summary(self.store, next_lesson)}\nNote: {note[:90]}"
                )
            )
        chapters = CHAPTERS
        if self.chapter_id not in {chapter.id for chapter in chapters}:
            self.chapter_id = next_lesson.chapter_id if next_lesson else None
            if not self.chapter_id and chapters:
                self.chapter_id = chapters[0].id
        picker = self.query_one("#chapter-picker", Select)
        section_titles = {section.id: section.title for section in SECTIONS}
        section_width = max(map(len, section_titles.values()))
        number_width = len(str(len(chapters)))
        picker.set_options(
            [
                (
                    f"{section_titles[chapter.section_id]:<{section_width}} · "
                    f"Chapter {index:>{number_width}}: {chapter.title}",
                    chapter.id,
                )
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
        lessons = chapter_activities(self.chapter_id) if self.chapter_id else ACTIVITIES
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
            kind = "game milestone · " if lesson.project_id else ""
            if self.size.width < 100:
                detail = (
                    "known"
                    if status == "familiar"
                    else "game"
                    if lesson.project_id
                    else "project"
                    if lesson.project and not lesson.title.lower().startswith("project:")
                    else ""
                )
                if detail:
                    text.append(f" · {detail}", style="#8f999c")
            else:
                separator = " · " if self.has_class("compact") else "\n       "
                text.append(f"{separator}{kind}{lesson.minutes} min · {label}", style="#8f999c")
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
        if self.tutor.open_activity(lesson):
            self.chapter_id = lesson.chapter_id

    @on(Button.Pressed, "#your-game")
    def action_game(self) -> None:
        self.tutor.action_game()

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
