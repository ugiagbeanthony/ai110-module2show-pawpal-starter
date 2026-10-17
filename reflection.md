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

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI to brainstorm the class responsibilities and relationships, draft the Mermaid diagram and Python skeleton, and then help implement the multi-pet task scheduler. Concrete prompts that listed the required attributes, methods, and behavior were the most helpful because they produced code and a design I could check against the project requirements.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

The early design used a `DailyPlan` class and treated planning as a per-pet responsibility. When the requirements emphasized a `Scheduler` that must process tasks across all pets, I did not keep that design unchanged: I replaced `DailyPlan` with `Scheduler` and ensured it retrieves tasks through `Owner.get_all_tasks()`. I checked the behavior with a two-pet runtime example that verified task aggregation, priority ordering, time-budget selection, and completion, and I ran the two focused pytest cases for task completion and adding a task to a pet; both passed.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
