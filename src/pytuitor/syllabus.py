"""A browsable curriculum outline, independent of the learner's chosen path."""

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.events import Resize
from textual.widgets import Button, Collapsible, Footer, Select, Static

from pytuitor.curriculum import TRACKS, track_chapters, track_lessons
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
                yield Select(
                    [
                        ("Beginner path", "beginner"),
                        ("Experienced path", "experienced"),
                        ("All chapters", "custom"),
                    ],
                    value=self.store.data["track"],
                    allow_blank=False,
                    id="syllabus-path",
                )
                with VerticalScroll(id="syllabus-scroll"):
                    yield Static(id="syllabus-summary", classes="muted")
                    yield Static("Expand a chapter to see its lessons.", classes="muted")
                    yield Vertical(id="syllabus-content")
        yield Footer(show_command_palette=False)

    async def on_mount(self) -> None:
        await self.show_outline(self.store.data["track"])
        self.query_one("#syllabus-scroll").focus()

    def on_resize(self, event: Resize) -> None:
        self.set_class(event.size.width < 100, "narrow")

    @on(Select.Changed, "#syllabus-path")
    async def change_path(self, event: Select.Changed) -> None:
        if event.value != Select.BLANK:
            await self.show_outline(str(event.value))

    async def show_outline(self, track: str) -> None:
        lessons = track_lessons(track)
        chapters = track_chapters(track)
        projects = sum(lesson.project for lesson in lessons)
        self.query_one("#syllabus-summary", Static).update(
            f"{len(chapters)} chapters · {len(lessons) - projects} lessons · {projects} projects\n"
            "Each unit includes Build and Repair."
        )
        content = self.query_one("#syllabus-content", Vertical)
        await content.remove_children()
        rows = [
            Static(
                f"    {'Chapter':38} {'Lessons':>7} {'Projects':>9}",
                classes="syllabus-columns",
                markup=False,
            )
        ]
        for index, chapter in enumerate(chapters, 1):
            units = [lesson for lesson in lessons if lesson.chapter_id == chapter.id]
            project_count = sum(lesson.project for lesson in units)
            details = [Static(chapter.outcome, classes="syllabus-outcome", markup=False)]
            if track == "custom":
                details.append(Static(f"{TRACKS[chapter.track]} path", classes="muted"))
            for lesson in units:
                details.append(
                    Static(
                        f"{lesson.title} · {lesson.minutes} min\n"
                        f"{lesson.subtitle}\n"
                        f"Topics: {', '.join(lesson.concepts)}",
                        classes="syllabus-lesson",
                        markup=False,
                    )
                )
            label = f"{index:02}  {chapter.title}"
            rows.append(
                Collapsible(
                    *details,
                    title=f"{label:38} {len(units) - project_count:>7} {project_count:>9}",
                    id=f"syllabus-{chapter.id}",
                    collapsed=True,
                    classes="syllabus-chapter",
                )
            )
        await content.mount(*rows)
        self.query_one("#syllabus-scroll").scroll_home(animate=False)

    @on(Button.Pressed, "#syllabus-back")
    def action_back(self) -> None:
        self.app.pop_screen()
