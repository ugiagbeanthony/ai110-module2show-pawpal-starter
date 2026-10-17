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

`Task` stores a care activity's description, duration, frequency, priority, completion status, due date, and scheduled time. `Pet` owns its care tasks, and `Owner` manages multiple pets and returns their combined tasks through `get_all_tasks()`. `Scheduler` retrieves tasks through that owner method, sorts and filters them, selects tasks that fit a time budget, reports exact-time conflicts, and adds the next daily or weekly occurrence when a task is completed. The Streamlit app stores its `Owner` in `st.session_state` so pets and tasks persist across reruns; its forms call the model methods to add pets and tasks, complete tasks, and generate a schedule. Run `streamlit run app.py` for the interactive app or `python main.py` for a terminal demo.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

Today's Schedule
Owner: Jordan | Available time: 45 minutes
- Serve breakfast (5 min, daily, high priority, pending)
- Morning walk (30 min, daily, high priority, pending)
- Brush coat (10 min, weekly, low priority, pending)
Total scheduled: 45 minutes

```
# Paste your pytest output here
```

## Smarter Scheduling

- **Sort by time:** `Scheduler.sort_by_time()` sorts by due date and zero-padded `HH:MM` time.
- **Filter tasks:** `Scheduler.filter_tasks()` can filter across all pets by a case-insensitive pet name, completion status, or both.
- **Select tasks for the day:** `Scheduler.organize_tasks()` excludes completed and future-due tasks, then sorts by priority and duration; `create_schedule()` selects tasks that fit the available minutes.
- **Detect conflicts:** `Scheduler.detect_conflicts()` returns warning strings when pending tasks for any pets share the same due date and exact start time.
- **Repeat care tasks:** `Task.next_occurrence()` creates a fresh daily or weekly task using `timedelta`; `Scheduler.mark_complete()` adds that next occurrence to the same pet.

Run `python main.py` to see sorting, pet/status filtering, recurrence, and conflict warnings in the terminal.

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
