# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

Add JSON persistence for PawPal owner/pet/task data, implement priority-first scheduling and a next-available-slot algorithm, connect those features to the Streamlit UI and terminal demo, add focused tests, and update the project documentation and final UML.

**What did the agent do?**

The agent reviewed the existing models, UI, tests, demo, and docs, then modified `pawpal_system.py`, `app.py`, `main.py`, `tests/test_pawpal.py`, `README.md`, `.gitignore`, `diagrams/uml_final.mmd`, and this log (`ai_interactions.md`). It used standard-library JSON dictionary conversion for `Owner.save_to_json()` and `Owner.load_from_json()`, added priority-then-time ordering and next-slot search, wired the UI to load/save `data.json`, expanded the CLI sample, and added persistence/scheduling tests. It then ran the pytest suite, CLI demo, and Streamlit workflow checks.

**What did you have to verify or fix manually?**

I reviewed the scheduling rules and kept conflict warnings distinct from next-slot search: conflicts report exact matching start times, while the slot finder checks overlapping durations. A UI smoke test revealed that the next-slot search missed a free gap before the first task because a loop variable reused the search-start variable; I renamed it and added a regression test. I also checked the captured CLI output against the README example and ignored `data.json` in Git so personal pet data is not committed. The custom JSON conversion avoids adding a dependency while explicitly serializing dates as ISO strings and validating fields during loading.

---

## Prompt Comparison (SF11)

> Compare two different prompts (or two different models) on the same task.

| | Option A | Option B |
|-|----------|----------|
| **Model / tool used** | | |
| **Prompt** | | |
| **Response summary** | | |
| **What was useful** | | |
| **Problems noticed** | | |
| **Decision** | | |

**Which approach did you use in your final implementation and why?**

<!-- Your conclusion -->
