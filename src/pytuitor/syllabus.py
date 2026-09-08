"""A browsable syllabus with a recommended sequence and optional depth."""

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.events import Resize
from textual.widgets import Button, Collapsible, Footer, Static

from pytuitor.curriculum import BY_ID, CHAPTERS, LESSONS, SECTIONS, chapter_lessons
from pytuitor.lesson_screen import LessonScreen
from pytuitor.ui import TutorScreen, brand


class Syllabus(TutorScreen):
    BINDINGS = [Binding("escape", "back", "Back")]

    def compose(self) -> ComposeResult:
        yield brand("SYLLABUS")
        with Horizontal(id="syllabus-container"):
            with Vertical(id="syllabus-body"):
                with Horizontal(id="syllabus-header"):
                    yield Static("Curriculum", classes="hero")
                    yield Button("Back", id="syllabus-back")
                with VerticalScroll(id="syllabus-scroll"):
                    projects = sum(lesson.project for lesson in LESSONS)
                    yield Static(
                        f"{len(CHAPTERS)} chapters · {len(LESSONS) - projects} lessons · "
                        f"{projects} projects\nEach unit includes Build and Repair.",
                        id="syllabus-summary",
                        classes="muted",
                    )
                    yield Static(
                        "Expand a chapter to see lessons and start learning.", classes="muted"
                    )
                    with Vertical(id="syllabus-content"):
                        for section in SECTIONS:
                            yield Static(
                                section.title + (" · Optional" if section.optional else ""),
                                classes="syllabus-section title",
                                markup=False,
                            )
                            yield Static(
                                section.description,
                                classes="syllabus-section-description muted",
                                markup=False,
                            )
                            for chapter in CHAPTERS:
                                if chapter.section_id != section.id:
                                    continue
                                units = chapter_lessons(chapter.id)
                                projects = sum(lesson.project for lesson in units)
                                count = f"{len(units) - projects} lessons"
                                if projects:
                                    count += f" · {projects} project" + (
                                        "s" if projects != 1 else ""
                                    )
                                with Collapsible(
                                    title=f"{chapter.title} · {count}",
                                    id=f"syllabus-{chapter.id}",
                                    collapsed=True,
                                    classes="syllabus-chapter",
                                ):
                                    yield Static(
                                        chapter.outcome, classes="syllabus-outcome", markup=False
                                    )
                                    prerequisites = [
                                        c.title for c in CHAPTERS if c.id in chapter.prerequisites
                                    ]
                                    yield Static(
                                        "Recommended first: "
                                        + (
                                            ", ".join(prerequisites)
                                            if prerequisites
                                            else "No prerequisites"
                                        ),
                                        classes="syllabus-prerequisites muted",
                                        markup=False,
                                    )
                                    yield Button(
                                        self.chapter_action(chapter.id),
                                        name=chapter.id,
                                        classes="start-chapter",
                                        variant="primary",
                                    )
                                    for lesson in units:
                                        yield Static(
                                            f"{lesson.title} · {lesson.minutes} min\n"
                                            f"{lesson.subtitle}\n"
                                            f"Topics: {', '.join(lesson.concepts)}",
                                            classes="syllabus-lesson",
                                            markup=False,
                                        )
        yield Footer(show_command_palette=False)

    def chapter_action(self, chapter_id: str) -> str:
        pending = self.store.chapter_next_lesson(chapter_id)
        if pending is None:
            return "Revisit chapter"
        units = chapter_lessons(chapter_id)
        if any(self.store.status(lesson) != "new" for lesson in units):
            return "Continue chapter"
        return "Start chapter"

    def on_screen_resume(self) -> None:
        for button in self.query(".start-chapter"):
            button.label = self.chapter_action(button.name)

    def on_mount(self) -> None:
        self.query_one("#syllabus-scroll").focus()

    def on_resize(self, event: Resize) -> None:
        self.set_class(event.size.width < 100, "narrow")

    @on(Button.Pressed, ".start-chapter")
    def start_chapter(self, event: Button.Pressed) -> None:
        chapter_id = event.button.name
        units = chapter_lessons(chapter_id)
        active = BY_ID.get(self.store.data.get("last_lesson"))
        lesson = (
            active
            if active
            and active.chapter_id == chapter_id
            and self.store.status(active) in ("new", "in progress")
            else self.store.chapter_next_lesson(chapter_id) or units[0]
        )
        previous = self.store.data.get("last_lesson")
        self.store.data["last_lesson"] = lesson.id
        if not self.tutor.persist():
            self.store.data["last_lesson"] = previous
            return
        self.app.push_screen(LessonScreen(lesson))

    @on(Button.Pressed, "#syllabus-back")
    def action_back(self) -> None:
        self.app.pop_screen()
