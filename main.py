"""Run a multi-pet scheduling demo in the terminal."""

from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner("Jordan")
    dog = Pet("Mochi", "dog")
    cat = Pet("Miso", "cat")
    owner.add_pet(dog)
    owner.add_pet(cat)

    dog.add_task(
        Task(
            "Morning walk",
            30,
            frequency="daily",
            priority="high",
            scheduled_time="08:30",
        )
    )
    dog.add_task(
        Task(
            "Brush coat",
            10,
            frequency="weekly",
            priority="low",
            scheduled_time="14:00",
        )
    )
    cat.add_task(
        Task(
            "Serve breakfast",
            5,
            frequency="daily",
            priority="high",
            scheduled_time="07:00",
        )
    )
    cat.add_task(
        Task(
            "Give medicine",
            5,
            frequency="daily",
            priority="high",
            scheduled_time="08:30",
        )
    )

    scheduler = Scheduler(owner)
    pet_by_task_id = {
        id(task): pet.name for pet in owner.pets for task in pet.tasks
    }

    print("Tasks sorted by scheduled time:")
    for task in scheduler.sort_by_time():
        print(f"- {task.scheduled_time} {pet_by_task_id[id(task)]}: {task.description}")

    print("\nPending tasks for Mochi:")
    for task in scheduler.filter_tasks(pet_name="Mochi", is_completed=False):
        print(f"- {task.scheduled_time} {task.description}")

    print("\nSchedule conflict warnings:")
    warnings = scheduler.detect_conflicts()
    if warnings:
        for warning in warnings:
            print(f"- {warning}")
    else:
        print("- No exact-time conflicts found.")

    recurring_task = dog.tasks[0]
    scheduler.mark_complete(recurring_task)
    next_occurrence = next(
        task
        for task in dog.tasks
        if task.description == recurring_task.description
        and task.due_date == date.today() + timedelta(days=1)
    )
    print(
        "\nRecurring task:"
        f"\n- Completed {recurring_task.description}; next occurrence is "
        f"{next_occurrence.due_date:%Y-%m-%d} at {next_occurrence.scheduled_time}."
    )

    available_minutes = 45
    schedule = scheduler.sort_by_time(scheduler.create_schedule(available_minutes))
    print("\nToday's Schedule")
    print(f"Owner: {owner.name} | Available time: {available_minutes} minutes")
    for task in schedule:
        print(f"- {pet_by_task_id.get(id(task), 'Pet')}: {task.describe()}")
    print(f"Total scheduled: {sum(task.duration_minutes for task in schedule)} minutes")


if __name__ == "__main__":
    main()
