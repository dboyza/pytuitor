"""Versioned local profiles with atomic writes and a single-writer lock."""

import fcntl
import json
import os
import tempfile
from datetime import UTC, datetime, timedelta
from pathlib import Path

from platformdirs import user_data_path

from pytuitor.curriculum import CONCEPTS, Lesson, track_lessons


class ProfileError(Exception):
    pass


def fresh_profile() -> dict:
    return {
        "version": 3,
        "onboarded": False,
        "track": "beginner",
        "familiar": [],
        "lessons": {},
        "last_lesson": None,
        "reviews": {},
        "feedback_enabled": False,
        "feedback": [],
    }


class Store:
    def __init__(self, directory: Path | None = None):
        self.directory = (
            (directory or user_data_path("pytuitor", appauthor=False)).expanduser().resolve()
        )
        self.directory.mkdir(parents=True, exist_ok=True)
        self.path = self.directory / "profile.json"
        self._lock = (self.directory / "profile.lock").open("a+")
        try:
            fcntl.flock(self._lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            self._lock.close()
            raise ProfileError("This profile is already open in another Pytuitor window.") from exc
        self._migration_original = None
        self.data = fresh_profile()
        if self.path.exists():
            try:
                data = json.loads(self.path.read_text())
                self._validate(data)
                if data["version"] < 3:
                    self._migration_original = self.path.read_bytes()
                self.data.update(data)
                self.data["version"] = 3
                for legacy_key in ("background", "goal", "diagnostic"):
                    self.data.pop(legacy_key, None)
            except (OSError, ValueError, TypeError, KeyError) as exc:
                self.close()
                raise ProfileError(
                    f"Cannot read profile at {self.path}. Your file was left untouched. "
                    "Use --data-dir with another directory to start a separate profile."
                ) from exc

    @staticmethod
    def _validate(data: object) -> None:
        if not isinstance(data, dict) or data.get("version") not in (1, 2, 3):
            raise ValueError("Unsupported profile version")
        if data.get("track") not in ("beginner", "experienced", "custom"):
            raise ValueError("Invalid track")
        if not isinstance(data.get("onboarded"), bool):
            raise ValueError("Invalid onboarding state")
        if data.get("background", "new") not in ("new", "cs", "python"):
            raise ValueError("Invalid background")
        if data.get("goal", "build") not in ("build", "depth", "confidence"):
            raise ValueError("Invalid goal")
        if data.get("last_lesson") is not None and not isinstance(data["last_lesson"], str):
            raise ValueError("Invalid resume state")
        if not isinstance(data.get("familiar"), list) or not all(
            isinstance(item, str) for item in data["familiar"]
        ):
            raise ValueError("Invalid concepts")
        if not isinstance(data.get("lessons"), dict):
            raise ValueError("Invalid lessons")
        if not isinstance(data.get("reviews", {}), dict):
            raise ValueError("Invalid review schedule")
        for item in data.get("reviews", {}).values():
            if not isinstance(item, dict) or type(item.get("level", 0)) is not int:
                raise ValueError("Invalid review progress")
            due = datetime.fromisoformat(item["due"])
            if due.tzinfo is None or not 0 <= item.get("level", 0) <= 4:
                raise ValueError("Invalid review date")
        if not isinstance(data.get("feedback_enabled", False), bool):
            raise ValueError("Invalid feedback setting")
        if not isinstance(data.get("feedback", []), list):
            raise ValueError("Invalid feedback records")
        for entry in data["lessons"].values():
            if not isinstance(entry, dict):
                raise ValueError("Invalid lesson progress")
            if entry.get("stage", "build") not in ("build", "repair"):
                raise ValueError("Invalid exercise stage")
            repair = entry.get("repair", {})
            if not isinstance(repair, dict):
                raise ValueError("Invalid repair progress")
            for stage_data in (entry, repair):
                for files_key in ("files", "checked_files"):
                    if files_key in stage_data:
                        from pytuitor.workspace import validate_files

                        file_map = stage_data[files_key]
                        if not isinstance(file_map, dict) or not all(
                            isinstance(value, str) for value in file_map.values()
                        ):
                            raise ValueError("Invalid project draft")
                        # An oversized draft can still be recovered and exported manually.
                        # Execution enforces content limits without locking the learner out.
                        validate_files(dict.fromkeys(file_map, ""))
            for key in ("code", "checked_code"):
                if key in repair and not isinstance(repair[key], str):
                    raise ValueError("Invalid repair draft")
            if "hints" in repair and (type(repair["hints"]) is not int or repair["hints"] < 0):
                raise ValueError("Invalid repair hints")
            for key in ("code", "input", "checked_code"):
                if key in entry and not isinstance(entry[key], str):
                    raise ValueError("Invalid draft")
            if "completed" in entry and not isinstance(entry["completed"], bool):
                raise ValueError("Invalid completion")
            if "prediction" in entry and not isinstance(entry["prediction"], bool):
                raise ValueError("Invalid prediction")
            if "hints" in entry and (type(entry["hints"]) is not int or entry["hints"] < 0):
                raise ValueError("Invalid hints")
        if not isinstance(data.get("diagnostic", {}), dict):
            raise ValueError("Invalid diagnostic")
        if not all(isinstance(value, bool) for value in data.get("diagnostic", {}).values()):
            raise ValueError("Invalid diagnostic answer")

    def close(self) -> None:
        if not self._lock.closed:
            self._lock.close()

    def reset(self) -> None:
        previous = self.data
        self.data = fresh_profile()
        try:
            self.save()
        except OSError:
            self.data = previous
            raise

    def save(self) -> None:
        if self._migration_original is not None:
            backup = self.directory / "profile-before-v3.json"
            try:
                with backup.open("xb") as stream:
                    stream.write(self._migration_original)
            except FileExistsError:
                pass
            self._migration_original = None
        fd, temporary = tempfile.mkstemp(prefix=".profile-", dir=self.directory)
        try:
            with os.fdopen(fd, "w") as stream:
                json.dump(self.data, stream, indent=2)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, self.path)
        finally:
            Path(temporary).unlink(missing_ok=True)

    def entry(self, lesson: Lesson) -> dict:
        return self.data["lessons"].setdefault(lesson.id, {})

    def status(self, lesson: Lesson) -> str:
        entry = self.data["lessons"].get(lesson.id, {})
        if entry.get("completed"):
            return "completed"
        if all(concept in self.data["familiar"] for concept in lesson.concepts):
            return "familiar"
        if "code" in entry:
            return "in progress"
        return "new"

    def next_lesson(self, track: str | None = None) -> Lesson | None:
        lessons = track_lessons(track or self.data["track"])
        last = self.data.get("last_lesson")
        for lesson in lessons:
            if lesson.id == last and self.status(lesson) not in ("completed", "familiar"):
                return lesson
        return next(
            (lesson for lesson in lessons if self.status(lesson) not in ("completed", "familiar")),
            None,
        )

    def set_familiar(self, concepts: list[str]) -> None:
        self.data["familiar"] = [concept for concept in concepts if concept in CONCEPTS]

    def schedule_review(self, lesson: Lesson, *, practiced: bool = False) -> None:
        """Optional practice never affects course completion or navigation."""
        key = lesson.review_of or lesson.id
        if not practiced and key in self.data["reviews"]:
            return
        previous = self.data["reviews"].get(key, {})
        level = min(previous.get("level", 0) + int(practiced), 4)
        days = (1, 3, 7, 14, 30)[level]
        self.data["reviews"][key] = {
            "level": level,
            "due": (datetime.now(UTC) + timedelta(days=days)).isoformat(),
        }

    def due_reviews(self, *, include_future: bool = False) -> list[Lesson]:
        from pytuitor.curriculum import REVIEWS

        now = datetime.now(UTC)
        result = []
        for lesson in REVIEWS:
            if self.data["track"] != "custom" and lesson.track != self.data["track"]:
                continue
            schedule = self.data["reviews"].get(lesson.review_of)
            if schedule and (include_future or datetime.fromisoformat(schedule["due"]) <= now):
                result.append(lesson)
        return result

    def record_feedback(self, lesson: Lesson, event: str, stage: str) -> None:
        if self.data["feedback_enabled"]:
            self.data["feedback"].append(
                {
                    "lesson": lesson.id,
                    "event": event,
                    "stage": stage,
                    "date": datetime.now(UTC).date().isoformat(),
                }
            )
            self.data["feedback"] = self.data["feedback"][-2000:]

    def export_feedback(self) -> Path:
        """Export only an explicit allowlist; never source, stdin, or host paths."""
        directory = self.directory / "exports"
        directory.mkdir(exist_ok=True)
        path = directory / ("feedback-" + datetime.now().strftime("%Y%m%d-%H%M%S-%f") + ".json")
        records = [
            {key: record.get(key) for key in ("lesson", "event", "stage", "date")}
            for record in self.data["feedback"]
            if isinstance(record, dict)
        ]
        with path.open("x", encoding="utf-8") as stream:
            json.dump(
                {"schema": 1, "track": self.data["track"], "events": records}, stream, indent=2
            )
        return path
