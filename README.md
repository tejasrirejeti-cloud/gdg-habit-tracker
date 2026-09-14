# GDG Habit Tracker 🚀

A polished command-line habit tracker built with Python that helps users build consistency through daily check-ins, active streaks, and reliable local persistence.

> **Built for the GDGoC MRUH Organizer Selection Process 2026–2027.**

## ✨ Why this project?

The project keeps the scope intentionally small, but treats the important parts seriously: a clear CLI, deterministic streak rules, validated local data, safe persistence, and tests for edge cases.

The key product rule is simple:

**Current streak = consecutive completed calendar days ending today.**

That means a habit with a strong run yesterday but no check-in today has a current streak of **0**. Its historical achievement is preserved separately through **Longest Streak**.

## 🎯 Features

- Add a habit with a name and description
- Validate and normalize user input
- Prevent duplicate habit names
- Daily check-in for the current day
- Prevent duplicate same-day check-ins
- Current streak and longest streak calculations
- Local JSON persistence across application restarts
- Atomic writes to reduce the chance of a truncated data file
- Recovery from missing, empty, corrupted, or malformed stored data
- Clean Windows-friendly command-line interface
- Automated tests covering core behavior and persistence edge cases

## 🖥️ Preview

### Main Menu

![Main Menu](docs/main-menu.png)

### Daily Check-In

![Daily Check-In](docs/check-in.png)

### Progress Dashboard

![Progress Dashboard](docs/progress.png)

The progress table uses ASCII characters for maximum compatibility with Windows PowerShell, Windows Terminal, and Command Prompt. The small Unicode banner is best-effort and falls back gracefully when a terminal cannot render it.

## 🛠️ Tech Stack

- **Python 3.11+**
- **JSON** for local persistence
- Python standard library only
- **unittest** for automated testing

No framework, database, network service, or third-party runtime dependency is required.

## 📁 Project Structure

```text
habit-tracker/
├── src/
│   ├── main.py            # CLI menus, prompts, and presentation
│   ├── habit_manager.py   # Domain model, validation, check-ins, streaks
│   ├── storage.py         # JSON persistence and recovery
│   └── utils.py           # Small shared helpers and terminal formatting
├── tests/
│   └── test_habit_manager.py
├── data/
│   └── habits.json        # Local data store
├── docs/
│   ├── main-menu.png
│   ├── check-in.png
│   └── progress.png
├── .gitignore
├── README.md
└── requirements.txt
