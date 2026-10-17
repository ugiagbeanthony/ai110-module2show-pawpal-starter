# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Implementation summary

`Task` stores a care activity's description, duration, frequency, priority, completion status, due date, and scheduled time. `Pet` owns its care tasks, and `Owner` manages multiple pets, returns their combined tasks through `get_all_tasks()`, and saves/loads the complete data model as JSON. `Scheduler` retrieves tasks through that owner method, sorts and filters them, schedules high-priority tasks first and then by due date/time, selects tasks that fit a time budget, finds the next open time slot, reports exact-time conflicts, and adds the next daily or weekly occurrence when a task is completed.

The Streamlit app loads `data.json` at startup and writes changes after the owner, pet, or task is updated. `data.json` is local app state and is ignored by Git so private/user-specific pet information is not committed. The app stores the loaded owner in `st.session_state` between reruns. Run `streamlit run app.py` for the interactive app or `python main.py` for a terminal demo.

### Data persistence

`Owner.save_to_json()` converts pets, tasks, completion flags, priority, scheduled times, and ISO-formatted due dates to JSON. `Owner.load_from_json()` validates the file and rebuilds the dataclass objects. `app.py` loads `data.json` at startup and saves after owner, pet, task, or completion updates. `.gitignore` excludes the generated data file so local pet data is not committed. The persistence changes are in `pawpal_system.py`, `app.py`, `.gitignore`, and `tests/test_pawpal.py`; `data.json` is created when the app first runs.

## Sample Output

The automated test output and complete CLI demo output are included below.

## 🧪 Testing PawPal+

Run the test suite from the repository root:

```bash
python -m pytest
```

The tests cover task completion and addition, chronological and priority-first sorting, filtering by pet and completion state, daily and weekly recurrence, conflict detection, open-slot search around overlapping tasks, JSON persistence, empty-owner behavior, future-due task exclusion, and preventing duplicate recurrence when completing a task twice.

Successful test run:

```text
============================= test session starts =============================
platform win32 -- Python 3.14.7, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\bbydr\ai110-module2show-pawpal-starter
collected 19 items

tests\test_pawpal.py ...................                                 [100%]

============================= 19 passed in 0.07s ==============================
```

**Confidence level:** ★★★★☆ (4/5). The core model and scheduler behaviors listed above pass automated tests; broader UI interaction and date-boundary scenarios could use more dedicated tests.

## Smarter Scheduling

- **Sort by time:** `Scheduler.sort_by_time()` sorts by due date and zero-padded `HH:MM` time.
- **Priority-based scheduling:** `Scheduler.sort_by_priority_and_time()` schedules high-priority tasks before medium and low, then orders each priority by due date and time. `create_schedule()` uses this ordering before applying the available-minute budget.
- **Filter tasks:** `Scheduler.filter_tasks()` can filter across all pets by a case-insensitive pet name, completion status, or both.
- **Select tasks for the day:** `Scheduler.organize_tasks()` excludes completed and future-due tasks, then sorts by priority, due date, and time; `create_schedule()` selects tasks that fit the available minutes.
- **Detect conflicts:** `Scheduler.detect_conflicts()` returns warning strings when pending tasks for any pets share the same due date and exact start time.
- **Repeat care tasks:** `Task.next_occurrence()` creates a fresh daily or weekly task using `timedelta`; `Scheduler.mark_complete()` adds that next occurrence to the same pet.
- **Find an open slot:** `Scheduler.find_next_available_slot()` scans the selected time window and returns the earliest gap long enough for a requested task, accounting for overlapping task durations.
- **Persist owner data:** `Owner.save_to_json()` serializes the owner, pets, tasks, dates, status, priority, and schedule times; `Owner.load_from_json()` rebuilds and validates those objects at app startup.

Run `python main.py` to see chronological sorting, priority-first scheduling, pet/status filtering, a suggested open slot, recurrence, and conflict warnings in the terminal.

## Demo Walkthrough

1. Run `streamlit run app.py`. The app loads `Owner` data from `data.json`, or initializes and saves a new owner when no data file exists.
2. Enter the owner's name and add pets such as Mochi (dog) and Miso (cat).
3. Select a pet, enter a task description, duration, frequency, priority, scheduled time, and due date, then add the task.
4. Review the care-task table. Filter it by pet and completion status; tasks are displayed in due-date and time order. Select a pending task and mark it complete. Daily and weekly tasks create their next occurrence automatically.
5. Review any schedule warnings. Each warning identifies the pets and tasks that share an exact date and start time; adjust a task's time to avoid the collision. Use "Find an available time" to locate a gap long enough for another task, then enter the available minutes and generate today's priority-ordered schedule.

The terminal demo in `main.py` shows tasks entered out of chronological order, sorted display, filtering for one pet, an exact-time conflict warning, an open-slot suggestion, priority-first scheduling, and the next daily occurrence after completion.

Sample output from `python main.py`:

```text
Tasks sorted by scheduled time:
- 07:00 Miso: Serve breakfast
- 08:30 Mochi: Morning walk
- 08:30 Miso: Give medicine
- 14:00 Mochi: Brush coat

Pending tasks for Mochi:
- 08:30 Morning walk
- 14:00 Brush coat

Schedule conflict warnings:
- Warning: Mochi: Morning walk, Miso: Give medicine share 08:30 on 2026-10-17.

Next available 20-minute slot:
- 07:05

Recurring task:
- Completed Morning walk; next occurrence is 2026-10-18 at 08:30.

Today's Priority-Based Schedule
Owner: Jordan | Available time: 45 minutes
- Miso: 08:30 Give medicine (5 min, daily, high priority, pending)
- Miso: 07:00 Serve breakfast (5 min, daily, medium priority, pending)
- Mochi: 14:00 Brush coat (10 min, weekly, low priority, pending)
Total scheduled: 20 minutes
```
