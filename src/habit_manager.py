"""Domain logic for habits, check-ins, streaks, and data validation."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Dict, List, Optional

from storage import Storage
from utils import clean_text, generate_habit_id, is_blank, parse_date, today_str


class DuplicateHabitError(Exception):
    """A habit with this name already exists."""


class InvalidInputError(Exception):
    """User input failed validation."""


class HabitNotFoundError(Exception):
    """No habit matches the requested ID."""


class AlreadyCheckedInError(Exception):
    """The habit was already checked in today."""


@dataclass
class Habit:
    id: str
    name: str
    description: str
    created_at: str
    completed_dates: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, object]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "completed_dates": list(self.completed_dates),
        }

    def current_streak(self) -> int:
        """Return consecutive completed days ending today.

        A current streak is considered active only when today's check-in
        exists. A missed today therefore produces a streak of zero.
        """
        completed = _valid_past_or_present_dates(self.completed_dates)
        today = date.today()
        if today not in completed:
            return 0

        streak = 0
        cursor = today
        while cursor in completed:
            streak += 1
            cursor -= timedelta(days=1)
        return streak

    def longest_streak(self) -> int:
        """Return the longest consecutive-day run in the full history."""
        ordered = sorted(_valid_past_or_present_dates(self.completed_dates))
        if not ordered:
            return 0

        longest = current = 1
        for previous, current_date in zip(ordered, ordered[1:]):
            if (current_date - previous).days == 1:
                current += 1
            else:
                current = 1
            longest = max(longest, current)
        return longest

    def last_completed(self) -> Optional[str]:
        """Return the most recent valid check-in date, if any."""
        ordered = sorted(_valid_past_or_present_dates(self.completed_dates))
        return ordered[-1].isoformat() if ordered else None

    def is_completed_today(self) -> bool:
        """Return whether the habit has a valid check-in for today."""
        return date.today() in _valid_past_or_present_dates(self.completed_dates)


def _valid_past_or_present_dates(date_strings: object) -> set[date]:
    """Parse, de-duplicate, and retain only valid dates up to today."""
    if not isinstance(date_strings, list):
        return set()

    today = date.today()
    parsed: set[date] = set()
    for raw in date_strings:
        if not isinstance(raw, str):
            continue
        try:
            parsed_date = parse_date(raw)
        except (ValueError, TypeError):
            continue
        if parsed_date <= today:
            parsed.add(parsed_date)
    return parsed


class HabitManager:
    """Own the in-memory habits and coordinate persistence."""

    def __init__(self, storage: Storage):
        self._storage = storage
        self.habits: List[Habit] = []
        self.load_warnings: List[str] = []
        self._load()

    def _load(self) -> None:
        result = self._storage.load()
        self.load_warnings = list(result.warnings)

        seen_ids: set[str] = set()
        habits: List[Habit] = []
        needs_resave = result.recovered_from_error

        for raw in result.data.get("habits", []):
            habit, cleaned = self._parse_habit_entry(raw, seen_ids)
            if habit is None:
                needs_resave = True
                continue
            habits.append(habit)
            seen_ids.add(habit.id)
            needs_resave = needs_resave or cleaned

        self.habits = habits
        if needs_resave:
            self._save()

    def _parse_habit_entry(self, raw: object, seen_ids: set[str]) -> tuple[Optional[Habit], bool]:
        """Validate and normalize one persisted habit record."""
        if not isinstance(raw, dict):
            self.load_warnings.append("Skipped a habit entry that wasn't a valid object.")
            return None, True

        habit_id = raw.get("id")
        name = raw.get("name")
        description = raw.get("description")
        created_at = raw.get("created_at")
        raw_dates = raw.get("completed_dates")

        if not isinstance(habit_id, str) or is_blank(habit_id):
            self.load_warnings.append("Skipped a habit entry with a missing/invalid ID.")
            return None, True
        if habit_id in seen_ids:
            self.load_warnings.append(f"Skipped a duplicate habit ID ('{habit_id}').")
            return None, True
        if not isinstance(name, str) or is_blank(name):
            self.load_warnings.append(f"Skipped habit '{habit_id}' with a missing/invalid name.")
            return None, True
        if not isinstance(description, str) or is_blank(description):
            self.load_warnings.append(f"Skipped habit '{habit_id}' with a missing/invalid description.")
            return None, True
        if not isinstance(created_at, str):
            self.load_warnings.append(f"Skipped habit '{clean_text(name)}' with a missing/invalid creation date.")
            return None, True
        try:
            created_date = parse_date(created_at)
        except (ValueError, TypeError):
            self.load_warnings.append(f"Skipped habit '{clean_text(name)}' with an invalid creation date.")
            return None, True
        if created_date > date.today():
            self.load_warnings.append(f"Skipped habit '{clean_text(name)}' with a future creation date.")
            return None, True
        if not isinstance(raw_dates, list):
            self.load_warnings.append(f"Skipped habit '{clean_text(name)}' with invalid check-in history.")
            return None, True

        valid_dates = _valid_past_or_present_dates(raw_dates)
        clean_dates = sorted(d.isoformat() for d in valid_dates)
        had_invalid_or_duplicate_dates = len(clean_dates) != len(raw_dates)
        if had_invalid_or_duplicate_dates:
            self.load_warnings.append(
                f"Cleaned up invalid, duplicate, or future check-in dates for '{clean_text(name)}'."
            )

        normalized_name = clean_text(name)
        normalized_description = clean_text(description)
        cleaned = (
            normalized_name != name
            or normalized_description != description
            or created_date.isoformat() != created_at
            or had_invalid_or_duplicate_dates
        )

        return Habit(
            id=habit_id,
            name=normalized_name,
            description=normalized_description,
            created_at=created_date.isoformat(),
            completed_dates=clean_dates,
        ), cleaned

    def _save(self) -> None:
        self._storage.save({"habits": [habit.to_dict() for habit in self.habits]})

    def list_habits(self) -> List[Habit]:
        return list(self.habits)

    def find_by_id(self, habit_id: str) -> Optional[Habit]:
        return next((habit for habit in self.habits if habit.id == habit_id), None)

    def _name_exists(self, name: str) -> bool:
        normalized = clean_text(name).casefold()
        return any(clean_text(habit.name).casefold() == normalized for habit in self.habits)

    def add_habit(self, name: str, description: str) -> Habit:
        name = clean_text(name)
        description = clean_text(description)

        if is_blank(name):
            raise InvalidInputError("Habit name cannot be empty.")
        if is_blank(description):
            raise InvalidInputError("Habit description cannot be empty.")
        if len(name) > 60:
            raise InvalidInputError("Habit name is too long (max 60 characters).")
        if len(description) > 200:
            raise InvalidInputError("Description is too long (max 200 characters).")
        if self._name_exists(name):
            raise DuplicateHabitError(f"A habit named '{name}' already exists.")

        habit = Habit(
            id=generate_habit_id(),
            name=name,
            description=description,
            created_at=today_str(),
        )
        self.habits.append(habit)
        self._save()
        return habit

    def check_in(self, habit_id: str) -> Habit:
        habit = self.find_by_id(habit_id)
        if habit is None:
            raise HabitNotFoundError("No habit found with that selection.")
        if habit.is_completed_today():
            raise AlreadyCheckedInError(f"{habit.name} is already completed for today.")

        habit.completed_dates.append(today_str())
        habit.completed_dates = sorted(set(habit.completed_dates))
        self._save()
        return habit
