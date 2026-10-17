# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial design has four classes: `Owner`, `Pet`, `Task`, and `DailyPlan`. An owner keeps basic information, preferences, and their pets. A pet stores its name, species, and care tasks. A task describes one care activity, including its title, duration, and priority. A daily plan associates a pet with the tasks selected for the day and the available time, and can explain the plan. The relationships are simple: an owner can have multiple pets, each pet can have multiple tasks, and a daily plan is for one pet and contains its selected tasks.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

The design changed after reviewing the skeleton and refining the requirements. I replaced `DailyPlan` with a `Scheduler` that reads tasks through `Owner.get_all_tasks()`, so scheduling considers every pet rather than just one. I also expanded `Task` to track its description, duration, frequency, completion status, and priority. The scheduler orders pending tasks by priority and duration, selects tasks that fit the available time, and can mark an owner's task complete. This makes the multi-pet data flow explicit and keeps pet/task storage separate from scheduling behavior.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The scheduler excludes tasks that are completed or not yet due, orders eligible tasks by priority and then duration, and selects tasks that fit within the available minutes. It also sorts displayed tasks chronologically and warns about tasks with the same due date and start time. I prioritized due status, importance, and the time budget because they directly determine what care can be planned today. Owner preferences are not currently part of the scheduler.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

Conflict detection checks only whether tasks have the exact same due date and start time; it does not compare task durations to find partial overlaps. This keeps the warning logic easy to understand and avoids implying a conflict when tasks may be rescheduled, but it can miss cases such as a 30-minute walk at 8:00 overlapping a task at 8:15. A future version could compare time intervals if more detailed scheduling is needed.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI to brainstorm the class responsibilities and relationships, draft the Mermaid diagram and Python skeleton, and then help implement the multi-pet task scheduler. Concrete prompts that listed the required attributes, methods, and behavior were the most helpful because they produced code and a design I could check against the project requirements.

The most effective features were being able to review related project files together, make coordinated edits across the backend, UI, diagram, and documentation, and run focused tests or UI checks to verify those changes. I kept implementation work in the project conversation and opened a separate testing-focused chat for test planning. Separating that phase gave testing its own scope and made it easier to focus on edge cases without mixing them into the feature implementation discussion.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

The early design used a `DailyPlan` class and treated planning as a per-pet responsibility. When the requirements emphasized a `Scheduler` that must process tasks across all pets, I did not keep that design unchanged: I replaced `DailyPlan` with `Scheduler` and ensured it retrieves tasks through `Owner.get_all_tasks()`. I checked the behavior with a two-pet runtime example that verified task aggregation, priority ordering, time-budget selection, and completion, and I ran the two focused pytest cases for task completion and adding a task to a pet; both passed.

For readability, AI review considered shortening `filter_tasks()` into a nested list comprehension. I kept the explicit pet loop because it makes the pet-name check and per-pet task filtering easier to follow; the number of tasks is small enough that a more compact form would not meaningfully improve performance.

I verified the scheduler changes by running the test suite (11 passed) and exercising the multi-pet Streamlit workflow, including conflict warnings and recurring-task completion. These checks helped confirm that the methods work together through the UI, not just in isolation.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

The 11 tests cover adding a task, completing a task, chronological ordering, filtering by pet and completion status, daily and weekly recurrence, conflict warnings, empty owners, future-due tasks, and repeated completion. These tests check the main flows as well as cases that could otherwise create incorrect plans or duplicate recurring tasks. I also used a Streamlit smoke test to verify that multiple pets and tasks could be added, filters and conflict warnings appeared, a schedule could be generated, and completing a recurring task created its next occurrence.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am fairly confident in the covered behavior (4 out of 5), since the automated tests pass and I exercised the UI workflow. I would next test tasks that partially overlap by duration, date boundaries such as completing a late task after its due date, and multiple tasks sharing one time slot. I would also add more automated tests for the Streamlit UI and time-budget choices.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am most satisfied that the scheduler works across multiple pets and that the UI makes its results understandable: tasks can be filtered and sorted, conflicts are called out with the affected pets and time, and completing recurring care adds its next occurrence.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would improve conflict detection to check overlapping time intervals, rather than only exact start-time matches, and make the time-budget selection behavior more transparent when a task does not fit. I would also connect owner preferences to scheduling and add automated UI tests.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

I learned that being the lead architect means turning requirements into clear responsibilities and relationships, then checking whether the implementation and tests still match them. AI helped me explore and implement ideas quickly, but I still had to choose the right scope, reject unnecessary complexity, and verify the behavior instead of assuming generated code was correct.
