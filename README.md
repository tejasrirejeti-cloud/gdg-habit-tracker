# 🌱 GDGoC Habit Tracker

> A lightweight, reliable CLI habit tracker built with Python, featuring persistent local storage, streak analytics, defensive data validation, corrupted-data recovery, and automated testing.

**Built for the GDGoC MRUH Organizer Selection Process 2026–2027.**

---

## 🚀 Project Overview

The **GDGoC Habit Tracker** is a simple terminal-based application designed to make daily habit tracking quick while demonstrating practical software engineering principles.

The project focuses on:

- 🧩 Clean modular architecture
- 💾 Reliable local persistence
- 🛡️ Defensive validation
- 🔥 Current and longest streak calculation
- 🧹 Data normalization
- ♻️ Corrupted-data recovery
- 🧪 Automated testing
- 🖥️ Simple CLI interaction

---

## ✨ Key Features

### 📝 Habit Management
- Create new habits
- Add descriptions
- Prevent duplicate habit names
- Validate user input
- Automatically record creation dates
- Assign unique habit IDs

### ✅ Daily Check-In
- Complete habits for the current day
- Prevent duplicate check-ins
- Save progress immediately
- Handle invalid stored completion dates safely

### 📊 Progress Tracking
View:
- Habit name
- Current streak
- Today's completion status

Habit details include:
- Name
- Description
- Creation date
- Today's status
- Current streak
- Longest streak
- Total check-ins
- Last completed date

### 🔥 Streak Analytics
- **Current Streak** — consecutive completed days ending today
- **Longest Streak** — longest historical sequence of consecutive days
- **Total Check-ins**
- **Last Completed Date**

### 🛡️ Defensive Data Handling
Safely handles:
- Missing data files
- Empty files
- Corrupted JSON
- Invalid records
- Duplicate IDs
- Invalid dates
- Future dates
- Duplicate completion dates
- Invalid user input

---

## 🖥️ Screenshots

### Main Menu
![Main Menu](docs/main-menu.png)

### Daily Check-In
![Daily Check-In](docs/check-in.png)

### Progress Dashboard
![Progress Dashboard](docs/progress.png)

---

## 🎥 Project Walkthrough

A **1–2 minute walkthrough** demonstrates:

1. Launching the application
2. Adding habits
3. Performing daily check-ins
4. Viewing progress
5. Opening habit details
6. Demonstrating duplicate check-in protection
7. Showing persistence
8. Exiting the application

### 🎬 Demo Video

**[▶️ Watch the 1–2 Minute Walkthrough](docs/demo.mp4)**

> For a true inline GitHub README player, upload the same video through the GitHub README editor as a GitHub-hosted video attachment.

---

## 🧭 Application Menu

```text
1. Add Habit
2. Daily Check-In
3. View Progress
4. Habit Details
5. Exit
```

---

## 🏗️ Architecture

```text
                    ┌──────────────────────┐
                    │        User          │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     CLI Interface    │
                    │      main.py         │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Habit Manager     │
                    │   habit_manager.py   │
                    └───────┬───────┬──────┘
                            │       │
                            ▼       ▼
                     Validation  Streak Logic
                            │       │
                            └───┬───┘
                                ▼
                    ┌──────────────────────┐
                    │    Storage Layer     │
                    │      storage.py      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     habits.json      │
                    │   Local Persistence  │
                    └──────────────────────┘
```

---

## 📁 Project Structure

```text
habit-tracker/
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
├── src/
│   ├── main.py
│   ├── habit_manager.py
│   ├── storage.py
│   └── utils.py
│
├── tests/
│   └── test_habit_manager.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 🧩 Module Responsibilities

### `src/main.py`
Handles CLI menus, user interaction, input collection, progress display, errors, and graceful exit.

### `src/habit_manager.py`
Contains habit creation, retrieval, validation, daily check-ins, duplicate prevention, streak calculation, and data normalization.

### `src/storage.py`
Handles JSON loading/saving, missing files, corrupted-data recovery, and atomic file replacement.

### `src/utils.py`
Contains reusable helper functionality.

### `tests/test_habit_manager.py`
Contains automated tests covering core functionality and edge cases.

---

## ⚙️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python** | Application development |
| **JSON** | Local data persistence |
| **unittest** | Automated testing |
| **Git** | Version control |
| **GitHub** | Repository hosting |

The project intentionally keeps dependencies minimal and relies primarily on Python's standard library.

---

## ▶️ Getting Started

### Prerequisites
- Python 3.x
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/tejasrirejeti-cloud/gdg-habit-tracker.git
cd gdg-habit-tracker
```

### 2. Run the Application

```bash
python src/main.py
```

### 3. Run the Tests

```bash
python -m unittest discover -s tests -v
```

Expected result:

```text
Ran 27 tests
OK
```

---

## 💾 Data Persistence

Habit data is stored locally in:

```text
data/habits.json
```

Initial structure:

```json
{
  "habits": []
}
```

The application automatically creates the storage file when necessary.

Important changes are persisted immediately, including:
- Adding habits
- Completing habits

This keeps progress available after restarting the application.

---

## 🔥 How Streaks Work

### Current Streak

A current streak represents consecutive completed days ending **today**.

Example:

```text
Today       ✅
Yesterday   ✅
2 days ago  ✅
3 days ago  ❌
```

Current streak:

```text
🔥 3 days
```

If the habit was not completed today:

```text
🔥 0 days
```

### Longest Streak

The longest streak finds the longest historical sequence of consecutive completion dates.

Example:

```text
Monday      ✅
Tuesday     ✅
Wednesday   ❌
Thursday    ✅
Friday      ✅
Saturday    ✅
```

Longest streak:

```text
🔥 3 days
```

---

## 🛡️ Data Validation & Recovery

The application validates persisted data before using it.

It checks:
- Habit IDs
- Habit names
- Descriptions
- Creation dates
- Completion dates
- JSON structure

It also handles corrupted or invalid storage safely and attempts to recover without unnecessarily crashing the application.

---

## 🧹 Data Normalization

The application protects against inconsistent stored data such as:

```text
Duplicate habit IDs
Malformed dates
Future completion dates
Duplicate completion dates
Invalid records
Missing required fields
Whitespace inconsistencies
```

Valid information is normalized before being used.

---

## 🧪 Testing

The project contains **27 automated unit tests** covering:

- Habit creation
- Habit retrieval
- Duplicate habit prevention
- Input validation
- Daily check-ins
- Duplicate check-in prevention
- Current streak calculation
- Longest streak calculation
- Historical dates
- Future dates
- Invalid dates
- Persistence
- Missing files
- Corrupted JSON
- Data normalization
- Edge cases

Run:

```bash
python -m unittest discover -s tests -v
```

Expected:

```text
Ran 27 tests
OK
```

---

## 🧠 Engineering Decisions

### Why JSON?
JSON is:
- Human-readable
- Lightweight
- Easy to inspect
- Easy to modify
- Suitable for a small local application
- Free from database setup overhead

### Why Separate Storage Logic?
Separating persistence from business logic keeps the code clean, improves testability, and makes future storage migration easier.

### Why Validate Persisted Data?
Stored data can become invalid because of manual edits, application changes, unexpected file changes, corruption, or duplicate records. The application therefore validates data before using it.

### Why Save Immediately?
Check-ins are meaningful user actions, so progress is persisted immediately to reduce the risk of losing work.

---

## 🔐 Reliability Highlights

The project is designed to remain stable with:

```text
❌ Missing storage file
❌ Empty storage file
❌ Corrupted JSON
❌ Invalid habit records
❌ Duplicate habit IDs
❌ Duplicate completion dates
❌ Malformed dates
❌ Future completion dates
❌ Duplicate daily check-ins
❌ Invalid user input
```

The application attempts to recover safely rather than failing unnecessarily.

---

## 🎯 What This Project Demonstrates

- 🐍 Python programming
- 🧱 Modular architecture
- 💾 JSON persistence
- 🛡️ Input and data validation
- ♻️ Defensive programming
- 📅 Date manipulation
- 🔥 Streak calculation
- 🧪 Automated testing
- 🌿 Git and GitHub
- 🖥️ CLI application design
- 🧹 Data normalization
- ⚠️ Edge-case handling

---

## 🔮 Future Improvements

- 📅 Calendar-based habit history
- 📈 Graphical progress charts
- 🗄️ SQLite database support
- 🔔 Habit reminders
- 🌐 Web interface
- 📱 Mobile-friendly interface
- 👤 User accounts
- ☁️ Cloud synchronization
- 📊 Weekly and monthly analytics
- 🏆 Habit achievement badges

---

## 👩‍💻 Author

**Tejasri Rejeti**

B.Tech — Computer Science & Engineering (AI & ML)

GitHub:  
https://github.com/tejasrirejeti-cloud

---

## 🌐 Built for GDGoC MRUH

This project was created as part of the **Google Developer Groups on Campus — Malla Reddy University (GDGoC MRUH) Organizer Selection Process 2026–2027**.

The project reflects my approach to building practical solutions with:

> **Clean Code + Reliability + Testing + User Experience**

---

## ⭐ Project Highlights

```text
27 automated tests
        +
Reliable JSON persistence
        +
Corrupted-data recovery
        +
Streak tracking
        +
Input validation
        +
Clean CLI
        +
Defensive data handling
        +
Documented architecture
        +
Demo video
        =
A practical, maintainable Python project
```

---

## 🙌 Thank You

Thank you for taking the time to explore the project.

I built this project with the goal of demonstrating not only that I can make an application work, but also that I can think about **reliability, usability, testing, and maintainability** while building it.
