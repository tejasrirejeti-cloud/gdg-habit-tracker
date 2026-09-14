# GDG Habit Tracker 🚀

A polished command-line habit tracker built with Python to help users build consistency through daily check-ins, deterministic streak tracking, and reliable local persistence.

> **Built for the GDGoC MRUH Organizer Selection Process 2026–2027.**

---

## ✨ Why This Project?

Most simple habit trackers treat a streak as little more than a count of completed check-ins.

This project takes a stricter approach:

> **Current Streak = consecutive completed calendar days ending today.**

If a habit was completed for several days in a row but **not today**, the current streak becomes **0**.

Historical achievement is preserved separately through **Longest Streak**.

The project focuses on four engineering priorities:

- 🎯 **Simple user experience** through a clean CLI
- 🔥 **Deterministic streak logic** with clearly defined rules
- 💾 **Reliable local persistence** across application restarts
- 🧪 **Robust validation and testing** for real-world edge cases

The goal was to keep the project small while making the core behavior correct, testable, and reliable.

---

## 🎯 Features

- ➕ Add habits with a name and description
- ✏️ Validate and normalize user input
- 🚫 Prevent duplicate habit names
- ✅ Daily check-in for the current day
- 🔒 Prevent duplicate same-day check-ins
- 🔥 Calculate current streaks
- 🏆 Calculate longest historical streaks
- 📊 View progress for all habits
- 🔎 View detailed information for individual habits
- 💾 Persist habit data locally using JSON
- ⚡ Atomic file writes for safer persistence
- 🛡️ Recover from missing, empty, corrupted, or malformed data
- 🧹 Normalize invalid stored dates and records
- 🖥️ Windows-friendly command-line interface
- 🧪 **27 automated tests** covering core behavior and edge cases
- 🚫 Zero third-party runtime dependencies

---

## 🖥️ Application Preview

### Main Menu

![Main Menu](docs/main-menu.png)

### Daily Check-In

![Daily Check-In](docs/check-in.png)

### Progress Dashboard

![Progress Dashboard](docs/progress.png)

The CLI uses ASCII characters for maximum compatibility with Windows PowerShell, Windows Terminal, and Command Prompt. The banner uses Unicode where supported and falls back gracefully when necessary.

---

## 🎬 Demo

### 🎥 Project Walkthrough

The project includes a **1–2 minute walkthrough video** demonstrating the working application.

The walkthrough covers:

1. Launching the application
2. Adding a habit
3. Performing a daily check-in
4. Viewing progress and streaks
5. Viewing habit details
6. Exiting the application
7. Restarting the application
8. Verifying that the habit and today's check-in persisted

### ▶️ Demo Video

The repository contains the complete walkthrough at:

**[🎥 Open the 1–2 minute Project Walkthrough](docs/demo.mp4)**

> The video demonstrates the actual working application rather than a static presentation.

### Demo Flow

| Time | Action |
|---|---|
| 0:00–0:10 | Launch the application and show the main menu |
| 0:10–0:30 | Add a `Python Practice` habit |
| 0:30–0:45 | Perform a daily check-in |
| 0:45–1:05 | Open View Progress and show the current streak |
| 1:05–1:15 | Open Habit Details |
| 1:15–1:25 | Exit and restart the application |
| 1:25–1:30 | Verify that the habit and today's check-in persisted |

### 📌 GitHub README Video Embedding

For the final submission, the walkthrough can also be embedded directly into the README using GitHub's hosted video attachment feature.

To create the inline player:

1. Open the repository on GitHub.
2. Edit `README.md`.
3. Drag the `demo.mp4` file into the GitHub README editor.
4. GitHub will upload the video and generate a hosted attachment.
5. Place the generated video attachment line inside this **Demo** section.
6. Commit the README changes.

The repository copy of `docs/demo.mp4` is retained as part of the project documentation.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3.11+** | Application development |
| **JSON** | Local data persistence |
| **unittest** | Automated testing |
| **Python Standard Library** | Core functionality |

No framework, database, network service, or third-party runtime dependency is required.

---

## 🧠 Architecture

The application follows a simple separation of responsibilities:

```text
┌──────────────────────────┐
│        CLI Layer         │
│        main.py           │
│  Menus • Input • Output  │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│     Business Logic       │
│     habit_manager.py     │
│ Validation • Check-ins   │
│ Streaks • Habit Rules    │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│     Persistence Layer    │
│        storage.py        │
│ JSON • Recovery • Atomic │
│          Writes          │
└──────────────────────────┘
Responsibilities

main.py

Handles CLI menus
Collects user input
Displays application output
Keeps presentation separate from business rules

habit_manager.py

Manages habits
Validates habit data
Handles check-ins
Prevents duplicate check-ins
Calculates current and longest streaks
Sanitizes loaded habit records and completion dates

storage.py

Loads and saves JSON data
Handles missing and corrupted files
Validates the top-level storage structure
Performs safer atomic writes

utils.py

Provides shared terminal formatting
Handles date parsing
Cleans text input
Generates habit IDs
Provides small reusable helpers

tests/

Verifies business logic
Tests persistence behavior
Covers edge cases and malformed data
📁 Project Structure
habit-tracker/
├── src/
│   ├── main.py
│   ├── habit_manager.py
│   ├── storage.py
│   └── utils.py
│
├── tests/
│   └── test_habit_manager.py
│
├── data/
│   └── habits.json
│
├── docs/
│   ├── main-menu.png
│   ├── check-in.png
│   ├── progress.png
│   └── demo.mp4
│
├── .gitignore
├── README.md
└── requirements.txt
⚙️ Installation
Requirements
Python 3.11 or newer
Git

No additional Python packages are required.

Windows PowerShell
git clone https://github.com/tejasrirejeti-cloud/gdg-habit-tracker.git
cd gdg-habit-tracker
python --version
macOS / Linux
git clone https://github.com/tejasrirejeti-cloud/gdg-habit-tracker.git
cd gdg-habit-tracker
python3 --version
▶️ Run the Application
Windows PowerShell
python src\main.py
macOS / Linux
python3 src/main.py

On first launch, the application creates the required local data file if it does not already exist:

data/habits.json
🧭 Application Menu

The application provides five simple actions:

1. Add Habit
2. Daily Check-In
3. View Progress
4. Habit Details
5. Exit
1️⃣ Add Habit

Creates a new habit using:

Habit name
Habit description

The application validates the input and rejects duplicate habit names.

2️⃣ Daily Check-In

Allows the user to select a habit and mark it as completed for today.

A habit cannot be checked in twice on the same day.

3️⃣ View Progress

Displays the progress of all habits, including:

Habit name
Current streak
Today's completion status
4️⃣ Habit Details

Displays detailed information about a selected habit:

Name
Description
Creation date
Today's status
Current streak
Longest streak
Total check-ins
Last completed date
5️⃣ Exit

Safely exits the application.

Data is persisted immediately after changes, so the application does not depend on the user selecting Exit to save progress.

📊 Streak Logic
Current Streak

A current streak counts consecutive completed calendar days ending today.

Completion History	Current Streak
3 days ago → 2 days ago → yesterday → today	4
3 days ago → 2 days ago → yesterday → no check-in today	0
Yesterday → today	2
Gap → yesterday → today	2

The important distinction is that the current streak must touch today.

Longest Streak

Longest streak represents the largest uninterrupted sequence of completed days anywhere in the habit's history.

It remains available even after the current streak ends.

For example:

History:
Mon → Tue → Wed → Thu → [missed] → Sat → Sun

Longest Streak = 4
Current Streak = 2

This separates current consistency from historical achievement.

Date Handling

Before streak calculations:

Dates are parsed and validated
Duplicate dates are removed
Malformed dates are ignored
Future dates are ignored
Valid dates are normalized

This keeps streak calculations deterministic and prevents invalid stored data from inflating results.

💾 Data Persistence

Habit data is stored locally in:

data/habits.json

Example structure:

{
  "habits": [
    {
      "id": "c88c0db2",
      "name": "Python Practice",
      "description": "Practice Python for 30 minutes",
      "created_at": "2026-09-14",
      "completed_dates": [
        "2026-09-14"
      ]
    }
  ]
}
Safe Persistence

The application uses atomic file writes:

Create temporary file
        ↓
Write complete JSON data
        ↓
Flush and sync
        ↓
Replace original file

The temporary file is created in the same directory before os.replace() is used to replace the existing data file.

This reduces the risk of leaving a partially written JSON file after an interrupted write.

Recovery

The application handles:

Missing data files
Empty files
Corrupted JSON
Invalid top-level JSON structures
Malformed habit records
Duplicate habit IDs
Invalid completion dates
Duplicate completion dates
Future completion dates

When possible, corrupted source files are preserved as .corrupted*.bak backups before recovery.

🧪 Testing

Run the complete test suite with:

python -m unittest discover -s tests -v

The project contains:

27 automated tests

The tests cover:

Habit creation
Habit input validation
Empty names and descriptions
Duplicate habit names
First check-in
Duplicate same-day check-ins
Unknown habit check-in attempts
Consecutive streaks
Missed-day behavior
Current streak when today is missing
Longest streak calculation
Unordered completion dates
Duplicate completion dates
Invalid date strings
Future dates
Persistence across restarts
Missing data files
Empty data files
Corrupted JSON
Invalid JSON schemas
Duplicate habit IDs
Malformed individual habit records

A successful test run ends with:

Ran 27 tests

OK
🔐 Reliability & Edge-Case Handling

The project is designed to remain predictable even when local data is imperfect.

Input Validation

The application validates:

Habit names
Habit descriptions
Duplicate habit names
Stored habit IDs
Creation dates
Completion dates
Schema Validation

Before using stored data, the application checks that the JSON structure is valid.

Raw JSON
   ↓
Schema Validation
   ↓
Record Validation
   ↓
Date Validation
   ↓
Normalization
   ↓
Habit Manager
Malformed Records

Invalid individual habit records are skipped instead of allowing one bad record to crash the entire application.

Duplicate IDs

Duplicate habit IDs are detected during loading and invalid duplicates are skipped.

Date Sanitization

Completion dates are cleaned before streak calculations:

malformed dates are removed
duplicate dates are removed
future dates are ignored
Corruption Recovery

If the main data file is unreadable or corrupted, the application attempts to preserve the corrupted file as a backup and continues with a clean state instead of exposing a raw Python traceback.

💡 Design Decisions
Why JSON?

JSON is appropriate for this project because the application manages a small, local collection of habits.

It is:

Lightweight
Human-readable
Easy to inspect
Offline-friendly
Simple to implement using Python's standard library
Why No Framework?

The project intentionally uses Python's standard library.

This keeps the application:

Easy to clone
Easy to run
Easy to understand
Easy to test
Free from unnecessary runtime dependencies
Why Separate Current and Longest Streak?

The two metrics answer different questions:

Current Streak

"How consistent am I right now?"

Longest Streak

"What is the best streak I have achieved?"

Keeping them separate ensures historical progress is not lost when the current streak breaks.

Why Separate Business Logic from the CLI?

The streak and validation logic are kept outside main.py.

This makes the most important behavior directly unit-testable without having to simulate terminal input and output.

📸 Screenshots

The repository includes screenshots captured from the working application:

Screenshot	Description
docs/main-menu.png	Main application menu
docs/check-in.png	Daily check-in flow
docs/progress.png	Progress dashboard

These screenshots show the actual CLI interface rather than mockups.

🚀 Future Improvements

The following are possible future extensions and are not currently implemented:

📤 CSV export of habit history
📊 Weekly completion summaries
📅 Monthly habit reports
🗂️ Habit archiving
🔔 Optional reminders
🖥️ Additional CLI filtering and sorting

The current version intentionally keeps the architecture lightweight and focused on the core habit-tracking problem.

👩‍💻 About the Author
Tejasri Rejeti

B.Tech — Computer Science & Engineering (Artificial Intelligence & Machine Learning)

Interested in building practical AI/ML solutions, developer tools, and community-driven projects.

🔗 GitHub:
https://github.com/tejasrirejeti-cloud

🔗 LinkedIn:
https://www.linkedin.com/in/tejasri-rejeti-561280372/

🌐 Built for the GDGoC Community

This project was developed as part of the:

GDGoC MRUH Organizer Selection Process 2026–2027

The project reflects an approach centered around:

🧠 Clear problem-solving
🛠️ Practical engineering
🧪 Test-driven thinking
🔐 Reliability and edge-case handling
🤝 Developer-community mindset
📚 Clear technical documentation
🏷️ GDGoC MRUH

Google Developer Groups on Campus — Malla Reddy University

Organizer Selection Process 2026–2027

Project: GDG Habit Tracker
Applicant: Tejasri Rejeti

⭐ Project Highlights
🔥 Deterministic streak logic that correctly handles missed days
🧠 Clear separation of concerns between CLI, business logic, and persistence
💾 Reliable JSON persistence across application restarts
⚡ Atomic file writes for safer data storage
🛡️ Corrupted-data recovery and validation
🧹 Date sanitization before streak calculations
🧪 27 automated tests covering core functionality and edge cases
🚫 Zero third-party runtime dependencies
🎥 1–2 minute product walkthrough
📖 Complete technical documentation
🚀 Built with Python, careful engineering, and the belief that a small project done correctly beats a large project done carelessly.

Made with ❤️ for the GDGoC MRUH community.





