"""Optional mixed review with independent drafts and explicit progression."""

import asyncio
import copy
from datetime import date, timedelta

from rich.text import Text
from textual import on, work
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.events import Resize
from textual.widgets import Button, Footer, Markdown, OptionList, Static, TextArea
from textual.widgets.option_list import Option

from pytuitor import review_progress as progress
from pytuitor.check_feedback import render_feedback
from pytuitor.content.reviews import REVIEWS
from pytuitor.curriculum import CHAPTERS
from pytuitor.experience_dialogs import CheckChooser
from pytuitor.runner import execute
from pytuitor.ui import CodeEditor, TutorScreen, brand


class ReviewHub(TutorScreen):
    BINDINGS = [Binding("escape", "app.dashboard", "Dashboard")]

    def compose(self):
        yield brand("OPTIONAL REVIEW")
        with Vertical(id="review-hub"):
            yield Static("A short return to earlier ideas", classes="hero")
            yield Static(
                "Three tasks: predict, repair, write. Reviews never block Continue.\n"
                "All chapters remain available; preparation is advisory.",
                classes="muted",
            )
            yield OptionList(id="review-chapters")
            yield Static(id="review-info", markup=False)
            with Horizontal(classes="actions"):
                yield Button("Start review", id="review-open", variant="primary")
                yield Button("Suggest tomorrow", id="review-defer")
                yield Button("Pause suggestions", id="review-pause")
        yield Footer(show_command_palette=False)

    def on_mount(self):
        self.refresh_reviews()
        suggestion = progress.suggested(self.store)
        if suggestion:
            self.query_one(OptionList).highlighted = next(
                i for i, chapter in enumerate(CHAPTERS) if chapter.id == suggestion
            )
        self.query_one(OptionList).focus()

    def on_screen_resume(self):
        if self.is_mounted:
            self.refresh_reviews()

    def refresh_reviews(self):
        listing = self.query_one("#review-chapters", OptionList)
        selected = listing.highlighted or 0
        listing.clear_options()
        for chapter in CHAPTERS:
            label = (
                "Suggested"
                if progress.due(self.store, chapter.id)
                else ("Available" if progress.ready(self.store, chapter.id) else "Preview")
            )
            count = sum(
                progress.task_entry(self.store, chapter.id, task, create=False).get("passed")
                is True
                for task in REVIEWS[chapter.id]
            )
            listing.add_option(
                Option(Text(f"{chapter.title} · {label} · {count}/3"), id=chapter.id)
            )
        listing.highlighted = selected
        paused = progress.review_data(self.store).get("paused") is True
        self.query_one("#review-pause", Button).label = (
            "Resume suggestions" if paused else "Pause suggestions"
        )
        self.show_selection()

    def selected(self):
        listing = self.query_one("#review-chapters", OptionList)
        return listing.get_option_at_index(listing.highlighted or 0).id

    @on(OptionList.OptionHighlighted, "#review-chapters")
    def show_selection(self):
        item = progress.entry(self.store, self.selected(), create=False)
        self.query_one("#review-info", Static).update(
            "Completed session. Start again to practice; your latest code stays available."
            if item.get("finished")
            else "Resume your saved attempt."
            if item.get("tasks")
            else "About 6-10 minutes. You can leave and return at any point."
        )

    @on(OptionList.OptionSelected, "#review-chapters")
    @on(Button.Pressed, "#review-open")
    def open_review(self):
        chapter = self.selected()
        if progress.entry(self.store, chapter).get("finished"):
            progress.restart(self.store, chapter)
        self.app.push_screen(ReviewScreen(chapter))

    @on(Button.Pressed, "#review-defer")
    def defer(self):
        item = progress.entry(self.store, self.selected())
        old = copy.deepcopy(item)
        item["due"] = (date.today() + timedelta(days=1)).isoformat()
        if not self.tutor.persist():
            item.clear()
            item.update(old)
        self.refresh_reviews()

    @on(Button.Pressed, "#review-pause")
    def pause_suggestions(self):
        data = progress.review_data(self.store)
        old = data.get("paused", False)
        data["paused"] = not old
        if not self.tutor.persist():
            data["paused"] = old
        self.refresh_reviews()


class ReviewScreen(TutorScreen):
    BINDINGS = [
        Binding("f5", "check", "Check"),
        Binding("ctrl+n", "next", "Next"),
        Binding("escape", "back", "Reviews", priority=True),
    ]

    def __init__(self, chapter):
        super().__init__()
        self.chapter = chapter
        self.index = 0
        self.restoring_task = True
        self.running = False
        self.suspend_saves = False
        self.execution = None
        self.checks = {}
        self.selected_check = None
        self.details = False

    @property
    def task(self):
        return REVIEWS[self.chapter][self.index]

    @property
    def attempt(self):
        return progress.task_entry(self.store, self.chapter, self.task)

    def compose(self):
        yield brand("OPTIONAL REVIEW")
        with Vertical(id="review-workbench"):
            yield Static(id="review-title", classes="title", markup=False)
            with VerticalScroll(id="review-prompt"):
                yield Markdown(id="review-instructions")
            yield OptionList(id="review-choices")
            yield CodeEditor(
                language="python", show_line_numbers=True, tab_behavior="indent", id="review-editor"
            )
            with Horizontal(classes="actions"):
                yield Button("Check", id="review-check", variant="primary")
                yield Button("Hint", id="review-hint")
                yield Button("Reference", id="review-reference")
                yield Button("Next", id="review-next")
                yield Button("Back", id="review-back")
            with Horizontal(id="review-check-actions"):
                yield Button("Checks", id="review-cases")
                yield Button("Details", id="review-details")
            with VerticalScroll(id="review-feedback-scroll"):
                yield Static(id="review-feedback", markup=False)
        yield Footer(show_command_palette=False)

    def on_mount(self):
        self.apply_layout()
        index = progress.entry(self.store, self.chapter).get("index", 0)
        self.index = index if type(index) is int and 0 <= index < 3 else 0
        self.load_task()

    def on_resize(self, event: Resize):
        self.apply_layout()

    def apply_layout(self):
        self.set_class(self.size.height < 32, "compact")

    def feedback(self):
        return render_feedback(
            self.checks, self.selected_check, details=self.details, stage="Review", compact=True
        )

    @on(Button.Pressed, "#review-cases")
    def choose_case(self):
        self.app.push_screen(
            CheckChooser(list(self.checks.values()), self.selected_check), self.case_chosen
        )

    def case_chosen(self, number):
        if number is not None and not self.suspend_saves and self.is_mounted:
            self.selected_check = number
            self.query_one("#review-feedback", Static).update(self.feedback())

    @on(Button.Pressed, "#review-details")
    def toggle_details(self):
        self.details = not self.details
        self.query_one("#review-details", Button).label = (
            "Hide details" if self.details else "Details"
        )
        self.query_one("#review-feedback", Static).update(self.feedback())

    def load_task(self):
        self.restoring_task = True
        self.checks = {}
        self.selected_check = None
        self.details = False
        self.query_one("#review-check-actions").display = False
        self.query_one("#review-details", Button).label = "Details"
        task = self.task
        self.query_one("#review-title", Static).update(
            f"{self.index + 1}/3 · {task.kind.title()} · {task.title}"
        )
        self.query_one("#review-instructions", Markdown).update(task.prompt)
        editor = self.query_one("#review-editor", TextArea)
        text = self.attempt.get("code", task.starter)
        editor.load_text(text if isinstance(text, str) and len(text) <= 100000 else task.starter)
        editor.display = task.kind != "predict"
        choices = self.query_one("#review-choices", OptionList)
        choices.clear_options()
        choices.add_options(
            [Option(Text(value), id=str(i)) for i, value in enumerate(task.choices)]
        )
        choices.display = task.kind == "predict"
        selected = self.attempt.get("choice", 0)
        if task.choices:
            choices.highlighted = (
                selected if type(selected) is int and 0 <= selected < len(task.choices) else 0
            )
        self.query_one("#review-reference", Button).display = task.kind != "predict"
        self.query_one("#review-feedback", Static).update(
            "Passed previously. Continue when ready."
            if self.attempt.get("passed")
            else "Try the task, then Check. Hints and references are optional."
        )
        self.query_one("#review-next", Button).disabled = not self.attempt.get("passed", False)
        self.query_one("#review-next", Button).label = "Finish" if self.index == 2 else "Next"
        self.query_one("#review-prompt").scroll_home(animate=False)
        self.call_after_refresh(self.ready)

    def ready(self):
        if self.suspend_saves or not self.is_mounted or not self.query("#review-editor"):
            return
        self.restoring_task = False
        self.query_one(
            "#review-choices" if self.task.kind == "predict" else "#review-editor"
        ).focus()

    @on(TextArea.Changed, "#review-editor")
    def edited(self):
        if self.restoring_task or self.suspend_saves:
            return
        self.attempt["code"] = self.query_one("#review-editor", TextArea).text
        self.attempt.pop("passed", None)
        self.query_one("#review-next", Button).disabled = True
        self.tutor.persist()

    @on(OptionList.OptionHighlighted, "#review-choices")
    def choice_changed(self):
        if not self.restoring_task and not self.suspend_saves:
            self.attempt["choice"] = self.query_one("#review-choices", OptionList).highlighted
            self.attempt.pop("passed", None)
            self.query_one("#review-next", Button).disabled = True
            self.tutor.persist()

    @on(Button.Pressed, "#review-check")
    def action_check(self):
        if not self.running:
            self.check_answer()

    @work(exclusive=True)
    async def check_answer(self):
        if self.suspend_saves or not self.is_mounted or not self.query("#review-check"):
            return
        self.running = True
        self.query_one("#review-check", Button).disabled = True
        self.query_one("#review-feedback", Static).update("Checking…")
        source = self.query_one("#review-editor", TextArea).text
        try:
            if self.task.kind == "predict":
                choice = self.query_one("#review-choices", OptionList).highlighted
                passed = choice == self.task.answer
                feedback = ("Correct. " if passed else "Try again. ") + self.task.explanation
            else:
                lesson = self.task.lesson()
                self.execution = asyncio.create_task(execute(lesson, source))
                result = await self.execution
                if self.suspend_saves or not self.is_mounted or not self.query("#review-check"):
                    return
                passed = result.passed and source == self.query_one("#review-editor", TextArea).text
                self.checks = {case["number"]: case for case in result.checks}
                self.selected_check = None
                self.query_one("#review-check-actions").display = bool(self.checks)
                feedback = (
                    self.feedback() if self.checks else result.error or "No checks completed."
                )
                if source != self.query_one("#review-editor", TextArea).text:
                    feedback += "\nDraft changed during the check. Check again."
            old = copy.deepcopy(self.attempt)
            self.attempt["passed"] = bool(passed)
            if not passed:
                self.attempt["assisted"] = True
            if not self.tutor.persist():
                self.attempt.clear()
                self.attempt.update(old)
                passed = False
                feedback += (
                    "\nCould not save this result. Check again after resolving the save error."
                )
            self.query_one("#review-feedback", Static).update(feedback)
            self.query_one("#review-next", Button).disabled = not passed
        finally:
            self.running = False
            self.execution = None
            if not self.suspend_saves and self.is_mounted and self.query("#review-check"):
                self.query_one("#review-check", Button).disabled = False

    @on(Button.Pressed, "#review-hint")
    def hint(self):
        self.attempt["assisted"] = True
        self.tutor.persist()
        self.query_one("#review-feedback", Static).update(
            self.task.hint
            or "Trace each statement in order and keep a note of the changing values."
        )

    @on(Button.Pressed, "#review-reference")
    def reference(self):
        self.attempt["assisted"] = True
        self.tutor.persist()
        self.query_one("#review-feedback", Static).update(
            "Reference, read only. Your draft is unchanged.\n\n" + self.task.reference
        )

    @on(Button.Pressed, "#review-next")
    def action_next(self):
        if self.running or not self.attempt.get("passed"):
            return
        item = progress.entry(self.store, self.chapter)
        old = copy.deepcopy(item)
        if self.index == 2:
            progress.complete(self.store, self.chapter)
        else:
            item["index"] = self.index + 1
        if not self.tutor.persist():
            item.clear()
            item.update(old)
            return
        if self.index == 2:
            self.notify("Review complete. Your course progress is unchanged.")
            self.action_back()
        else:
            self.index += 1
            self.load_task()

    @on(Button.Pressed, "#review-back")
    def action_back(self):
        self.stop_review()
        self.app.pop_screen()

    def stop_review(self):
        self.suspend_saves = True
        if self.execution:
            self.execution.cancel()

    def on_unmount(self):
        self.stop_review()
