"""
Unit tests for habit_manager.py.

Run with:
    python -m unittest discover -s tests -v

Streak tests use dates relative to today() (via days_ago helper) rather
than hardcoded calendar dates, so the suite passes correctly no matter
what day it's actually run on -- important since current_streak() is
now defined relative to "today".
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(SRC_DIR))

from habit_manager import (  # noqa: E402
    AlreadyCheckedInError,
    DuplicateHabitError,
    Habit,
    HabitManager,
    HabitNotFoundError,
    InvalidInputError,
)
from storage import Storage  # noqa: E402


def days_ago(n: int) -> str:
    return (date.today() - timedelta(days=n)).isoformat()


def make_manager(tmp_dir: str) -> HabitManager:
    return HabitManager(Storage(Path(tmp_dir) / "habits.json"))


class TestAddHabit(unittest.TestCase):
    def test_add_habit_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            manager = make_manager(tmp)
            habit = manager.add_habit("Read", "Read for 20 minutes")
            self.assertEqual(habit.name, "Read")
            self.assertEqual(len(manager.list_habits()), 1)

    def test_add_habit_rejects_empty_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            manager = make_manager(tmp)
            with self.assertRaises(InvalidInputError):
                manager.add_habit("   ", "Something")

    def test_duplicate_habit_name_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            manager = make_manager(tmp)
            manager.add_habit("Read", "Read books")
            with self.assertRaises(DuplicateHabitError):
                manager.add_habit("  read  ", "Read again")


class TestCheckIn(unittest.TestCase):
    def test_first_check_in_marks_today_completed(self):
        with tempfile.TemporaryDirectory() as tmp:
            manager = make_manager(tmp)
            habit = manager.add_habit("Exercise", "30 min workout")
            updated = manager.check_in(habit.id)
            self.assertTrue(updated.is_completed_today())
            self.assertEqual(updated.current_streak(), 1)

    def test_duplicate_check_in_same_day_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            manager = make_manager(tmp)
            habit = manager.add_habit("Exercise", "30 min workout")
            manager.check_in(habit.id)
            with self.assertRaises(AlreadyCheckedInError):
                manager.check_in(habit.id)
            # The duplicate attempt must not add a second record.
            reloaded = manager.find_by_id(habit.id)
            self.assertEqual(reloaded.completed_dates.count(days_ago(0)), 1)

    def test_check_in_unknown_habit_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            manager = make_manager(tmp)
            with self.assertRaises(HabitNotFoundError):
                manager.check_in("doesnotexist")


class TestStreakLogic(unittest.TestCase):
    """current_streak() = consecutive completed days ending TODAY."""

    def test_empty_completion_history_has_zero_streak(self):
        habit = Habit(id="1", name="X", description="d", created_at=days_ago(0), completed_dates=[])
        self.assertEqual(habit.current_streak(), 0)

    def test_consecutive_streak_ending_today(self):
        habit = Habit(
            id="1", name="X", description="d", created_at=days_ago(3),
            completed_dates=[days_ago(3), days_ago(2), days_ago(1), days_ago(0)],
        )
        self.assertEqual(habit.current_streak(), 4)

    def test_current_streak_is_zero_when_today_is_missing(self):
        # Completed 3 days in a row, but not today -- streak is dead, not "3".
        habit = Habit(
            id="1", name="X", description="d", created_at=days_ago(3),
            completed_dates=[days_ago(3), days_ago(2), days_ago(1)],
        )
        self.assertEqual(habit.current_streak(), 0)

    def test_missing_day_breaks_streak_even_if_today_is_done(self):
        # Yesterday-2 was skipped; only the run touching today counts.
        habit = Habit(
            id="1", name="X", description="d", created_at=days_ago(3),
            completed_dates=[days_ago(3), days_ago(2), days_ago(0)],
        )
        self.assertEqual(habit.current_streak(), 1)

    def test_streak_of_two_with_one_gap_further_back(self):
        habit = Habit(
            id="1", name="X", description="d", created_at=days_ago(4),
            completed_dates=[days_ago(4), days_ago(3), days_ago(1), days_ago(0)],
        )
        self.assertEqual(habit.current_streak(), 2)

    def test_unordered_dates_computed_correctly(self):
        habit = Habit(
            id="1", name="X", description="d", created_at=days_ago(2),
            completed_dates=[days_ago(0), days_ago(2), days_ago(1)],
        )
        self.assertEqual(habit.current_streak(), 3)

    def test_duplicate_dates_do_not_inflate_streak(self):
        habit = Habit(
            id="1", name="X", description="d", created_at=days_ago(1),
            completed_dates=[days_ago(1), days_ago(1), days_ago(0), days_ago(0)],
        )
        self.assertEqual(habit.current_streak(), 2)

    def test_invalid_date_strings_are_ignored(self):
        habit = Habit(
            id="1", name="X", description="d", created_at=days_ago(1),
            completed_dates=[days_ago(1), "not-a-date", days_ago(0)],
        )
        self.assertEqual(habit.current_streak(), 2)

    def test_future_dates_are_ignored(self):
        tomorrow = (date.today() + timedelta(days=1)).isoformat()
        habit = Habit(
            id="1", name="X", description="d", created_at=days_ago(1),
            completed_dates=[days_ago(1), days_ago(0), tomorrow],
        )
        self.assertEqual(habit.current_streak(), 2)

    def test_longest_streak_can_exceed_current_streak(self):
        habit = Habit(
            id="1", name="X", description="d", created_at=days_ago(10),
            completed_dates=[days_ago(10), days_ago(9), days_ago(8), days_ago(7), days_ago(0)],
        )
        self.assertEqual(habit.longest_streak(), 4)
        self.assertEqual(habit.current_streak(), 1)

    def test_longest_streak_with_no_history_is_zero(self):
        habit = Habit(id="1", name="X", description="d", created_at=days_ago(0), completed_dates=[])
        self.assertEqual(habit.longest_streak(), 0)


class TestPersistenceAndLoadValidation(unittest.TestCase):
    def test_data_survives_restart(self):
        with tempfile.TemporaryDirectory() as tmp:
            data_file = Path(tmp) / "habits.json"
            manager1 = HabitManager(Storage(data_file))
            habit = manager1.add_habit("Meditate", "10 minutes")
            manager1.check_in(habit.id)

            manager2 = HabitManager(Storage(data_file))  # simulates app restart
            reloaded = manager2.find_by_id(habit.id)

            self.assertIsNotNone(reloaded)
            self.assertEqual(reloaded.current_streak(), 1)
            self.assertEqual(manager2.load_warnings, [])

    def test_missing_file_starts_empty_without_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            manager = HabitManager(Storage(Path(tmp) / "missing.json"))
            self.assertEqual(manager.list_habits(), [])
            self.assertEqual(manager.load_warnings, [])


    def test_missing_file_is_created_on_first_load(self):
        with tempfile.TemporaryDirectory() as tmp:
            data_file = Path(tmp) / "habits.json"
            manager = HabitManager(Storage(data_file))
            self.assertEqual(manager.list_habits(), [])
            self.assertTrue(data_file.exists())
            self.assertEqual(data_file.read_text(encoding="utf-8").strip(), '{\n  "habits": []\n}')

    def test_invalid_description_type_is_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            data_file = Path(tmp) / "habits.json"
            data_file.write_text(
                '{"habits": [{"id": "bad1", "name": "Read", "description": 123, '
                '"created_at": "2026-01-01", "completed_dates": []}]}',
                encoding="utf-8",
            )
            manager = HabitManager(Storage(data_file))
            self.assertEqual(manager.list_habits(), [])
            self.assertTrue(any("description" in w.lower() for w in manager.load_warnings))

    def test_future_created_at_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            data_file = Path(tmp) / "habits.json"
            future = (date.today() + timedelta(days=1)).isoformat()
            data_file.write_text(
                '{"habits": [{"id": "future1", "name": "Future", "description": "d", '
                f'"created_at": "{future}", "completed_dates": []}}]}}',
                encoding="utf-8",
            )
            manager = HabitManager(Storage(data_file))
            self.assertEqual(manager.list_habits(), [])
            self.assertTrue(any("future creation date" in w.lower() for w in manager.load_warnings))

    def test_empty_file_starts_empty_with_warning(self):
        with tempfile.TemporaryDirectory() as tmp:
            data_file = Path(tmp) / "habits.json"
            data_file.write_text("", encoding="utf-8")
            manager = HabitManager(Storage(data_file))
            self.assertEqual(manager.list_habits(), [])
            self.assertTrue(manager.load_warnings)

    def test_corrupted_json_recovers_with_backup(self):
        with tempfile.TemporaryDirectory() as tmp:
            data_file = Path(tmp) / "habits.json"
            data_file.write_text("{not valid json!!", encoding="utf-8")
            manager = HabitManager(Storage(data_file))
            self.assertEqual(manager.list_habits(), [])
            self.assertTrue(manager.load_warnings)
            self.assertEqual(len(list(Path(tmp).glob("*.corrupted*.bak"))), 1)

    def test_invalid_schema_recovers_with_backup(self):
        with tempfile.TemporaryDirectory() as tmp:
            data_file = Path(tmp) / "habits.json"
            data_file.write_text('{"not_habits": []}', encoding="utf-8")
            manager = HabitManager(Storage(data_file))
            self.assertEqual(manager.list_habits(), [])
            self.assertTrue(manager.load_warnings)

    def test_duplicate_habit_ids_on_load_keep_only_the_first(self):
        with tempfile.TemporaryDirectory() as tmp:
            data_file = Path(tmp) / "habits.json"
            data_file.write_text(
                '{"habits": ['
                '{"id": "dup1", "name": "First", "description": "d", '
                '"created_at": "2026-01-01", "completed_dates": []},'
                '{"id": "dup1", "name": "Second", "description": "d", '
                '"created_at": "2026-01-01", "completed_dates": []}'
                ']}',
                encoding="utf-8",
            )
            manager = HabitManager(Storage(data_file))
            self.assertEqual(len(manager.list_habits()), 1)
            self.assertEqual(manager.list_habits()[0].name, "First")
            self.assertTrue(any("duplicate" in w.lower() for w in manager.load_warnings))

    def test_malformed_habit_entry_is_skipped_not_fatal(self):
        with tempfile.TemporaryDirectory() as tmp:
            data_file = Path(tmp) / "habits.json"
            data_file.write_text(
                '{"habits": ['
                '{"id": "ok1", "name": "Good Habit", "description": "d", '
                '"created_at": "2026-01-01", "completed_dates": []},'
                '{"id": "bad1", "name": "", "description": "d", '
                '"created_at": "2026-01-01", "completed_dates": []}'
                ']}',
                encoding="utf-8",
            )
            manager = HabitManager(Storage(data_file))
            self.assertEqual(len(manager.list_habits()), 1)
            self.assertEqual(manager.list_habits()[0].name, "Good Habit")


if __name__ == "__main__":
    unittest.main()
