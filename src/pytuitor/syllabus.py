"""A browsable curriculum outline, independent of the learner's chosen path."""

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.events import Resize
from textual.widgets import Button, Footer, Markdown, Select, Static

from pytuitor.curriculum import TRACKS, track_chapters, track_lessons
from pytuitor.ui import TutorScreen, brand


class Syllabus(TutorScreen):
    BINDINGS = [Binding("escape", "back", "Back")]

    def compose(self) -> ComposeResult:
        yield brand("SYLLABUS")
        with Horizontal(id="syllabus-container"):
            with Vertical(id="syllabus-body"):
                with Horizontal(id="syllabus-header"):
                    yield Static("Explore the curriculum", classes="hero")
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
                    yield Markdown(id="syllabus-content")
        yield Footer(show_command_palette=False)

    def on_mount(self) -> None:
        self.show_outline(self.store.data["track"])
        self.query_one("#syllabus-scroll").focus()

    def on_resize(self, event: Resize) -> None:
        self.set_class(event.size.width < 100, "narrow")

    @on(Select.Changed, "#syllabus-path")
    def change_path(self, event: Select.Changed) -> None:
        if event.value != Select.BLANK:
            self.show_outline(str(event.value))

    def show_outline(self, track: str) -> None:
        lessons = track_lessons(track)
        chapters = track_chapters(track)
        projects = sum(lesson.project for lesson in lessons)
        minutes = sum(lesson.minutes for lesson in lessons)
        title = "All chapters" if track == "custom" else f"{TRACKS[track]} path"
        lines = [
            f"# {title}",
            f"{len(chapters)} chapters · {len(lessons) - projects} lessons · "
            f"{projects} projects · about {minutes // 60} hr {minutes % 60} min",
            "Build from scratch, then Repair a broken program to complete each unit. "
            "Learn entirely offline.",
        ]
        for index, chapter in enumerate(chapters, 1):
            lines.extend([f"## Chapter {index}: {chapter.title}", chapter.outcome])
            if track == "custom":
                lines.append(f"{TRACKS[chapter.track]} path")
            for lesson in (item for item in lessons if item.chapter_id == chapter.id):
                lines.extend(
                    [
                        f"### {lesson.title}",
                        f"{'Project' if lesson.project else 'Lesson'} · {lesson.minutes} min · "
                        f"{lesson.subtitle}",
                        f"Topics: {', '.join(lesson.concepts)}.",
                    ]
                )
        self.query_one("#syllabus-content", Markdown).update("\n\n".join(lines))
        self.query_one("#syllabus-scroll").scroll_home(animate=False)

    @on(Button.Pressed, "#syllabus-back")
    def action_back(self) -> None:
        self.app.pop_screen()
