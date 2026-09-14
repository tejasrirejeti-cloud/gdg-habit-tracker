"""Command-line interface for the GDG Habit Tracker."""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

from habit_manager import (
    AlreadyCheckedInError,
    DuplicateHabitError,
    Habit,
    HabitManager,
    HabitNotFoundError,
    InvalidInputError,
)
from storage import Storage
from utils import banner, divider, fail, note, ok, warn

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "habits.json"

MENU = """
  1. Add Habit
  2. Daily Check-In
  3. View Progress
  4. Habit Details
  5. Exit
"""


def prompt(text: str) -> str:
    try:
        return input(text)
    except EOFError:
        print()
        print(fail("Input ended unexpectedly. Exiting."))
        raise SystemExit(1)


def prompt_menu_choice() -> str:
    valid = {"1", "2", "3", "4", "5"}
    while True:
        choice = prompt("Choose an option -> ").strip()
        if choice in valid:
            return choice
        print(fail(f"'{choice}' isn't a valid option. Pick 1-5."))


def _select_habit(habits: list[Habit], prompt_text: str) -> Habit | None:
    for index, habit in enumerate(habits, start=1):
        print(f"  {index}. {habit.name}")
    print()
    selection = prompt(prompt_text).strip()

    if selection == "0":
        print(note("Cancelled."))
        return None
    if not selection.isdigit() or not 1 <= int(selection) <= len(habits):
        print(fail("Invalid selection."))
        return None
    return habits[int(selection) - 1]


def handle_add_habit(manager: HabitManager) -> None:
    print(divider())
    print("Add a New Habit")
    print(divider())
    name = prompt("Habit name: ")
    description = prompt("Habit description: ")
    try:
        habit = manager.add_habit(name, description)
    except (InvalidInputError, DuplicateHabitError) as exc:
        print(fail(str(exc)))
        return

    print()
    print(ok("Habit created successfully!"))
    print(f"\n  {habit.name}\n  {habit.description}\n")
    print("Your first check-in is waiting.")


def handle_check_in(manager: HabitManager) -> None:
    print(divider())
    print("Daily Check-In")
    print(divider())
    habits = manager.list_habits()
    if not habits:
        print(note("No habits yet. Add one first."))
        return

    print("Choose a habit:\n")
    habit = _select_habit(habits, "Select habit (or 0 to cancel) -> ")
    if habit is None:
        return

    try:
        updated = manager.check_in(habit.id)
    except (HabitNotFoundError, AlreadyCheckedInError) as exc:
        print(warn(str(exc)))
        return

    print()
    print(ok("Check-in recorded!"))
    print(f"\n  {updated.name}")
    print(f"  Current streak: {updated.current_streak()} day(s)")


def _print_progress_table(habits: list[Habit]) -> None:
    if not habits:
        print(note("No habits yet. Start building your first streak!"))
        return

    rows: list[tuple[str, str, str, str]] = []
    for index, habit in enumerate(habits, start=1):
        name = habit.name if len(habit.name) <= 24 else habit.name[:21] + "..."
        rows.append(
            (
                str(index),
                name,
                f"{habit.current_streak()} day(s)",
                "Completed" if habit.is_completed_today() else "Pending",
            )
        )

    headers = ("#", "Habit", "Current Streak", "Today")
    widths = [len(headers[0]), len(headers[1]), len(headers[2]), len(headers[3])]
    for row in rows:
        widths = [max(width, len(value)) for width, value in zip(widths, row)]

    border = "+" + "+".join("-" * (width + 2) for width in widths) + "+"
    header_line = "|" + "|".join(f" {value:<{width}} " for value, width in zip(headers, widths)) + "|"
    print(border)
    print(header_line)
    print(border)
    for row in rows:
        print("|" + "|".join(f" {value:<{width}} " for value, width in zip(row, widths)) + "|")
    print(border)


def handle_view_progress(manager: HabitManager) -> None:
    print(divider())
    print("Progress Overview")
    print(divider())
    _print_progress_table(manager.list_habits())


def handle_view_details(manager: HabitManager) -> None:
    print(divider())
    print("Habit Details")
    print(divider())
    habits = manager.list_habits()
    if not habits:
        print(note("No habits yet. Add one first."))
        return

    habit = _select_habit(habits, "Select habit (or 0 to cancel) -> ")
    if habit is None:
        return

    print()
    print(f"Name:             {habit.name}")
    print(f"Description:      {habit.description}")
    print(f"Created:          {habit.created_at}")
    print(f"Today:            {'Completed' if habit.is_completed_today() else 'Pending'}")
    print(f"Current streak:   {habit.current_streak()} day(s)")
    print(f"Longest streak:   {habit.longest_streak()} day(s)")
    print(f"Total check-ins:  {len(set(habit.completed_dates))}")
    print(f"Last completed:   {habit.last_completed() or 'never'}")


def run() -> None:
    print(banner("GDG HABIT TRACKER", "Build consistency. Track growth."))
    print(f"\nTODAY -- {date.today():%B %d, %Y}")

    manager = HabitManager(Storage(DATA_FILE))
    for message in manager.load_warnings:
        print(warn(message))

    actions = {
        "1": handle_add_habit,
        "2": handle_check_in,
        "3": handle_view_progress,
        "4": handle_view_details,
    }

    while True:
        print(MENU)
        choice = prompt_menu_choice()
        print()

        if choice == "5":
            print(ok("Goodbye! Keep the streak alive."))
            break

        actions[choice](manager)
        print()


def main() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

    try:
        run()
    except KeyboardInterrupt:
        print()
        print(note("Interrupted. Goodbye!"))
        raise SystemExit(0)


if __name__ == "__main__":
    main()
