from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_updates_task_status() -> None:
    task = Task("Morning walk", 30)

    assert task.is_completed is False

    task.mark_complete()

    assert task.is_completed is True


def test_add_task_increases_pet_task_count() -> None:
    pet = Pet("Mochi", "dog")
    task = Task("Morning walk", 30)

    assert len(pet.tasks) == 0

    pet.add_task(task)

    assert len(pet.tasks) == 1
    assert pet.tasks[0] is task


def test_sort_by_time_orders_tasks_chronologically() -> None:
    pet = Pet(
        "Mochi",
        "dog",
        tasks=[
            Task("Evening walk", 20, scheduled_time="18:30"),
            Task("Breakfast", 10, scheduled_time="07:05"),
            Task("Lunch", 10, scheduled_time="12:15"),
        ],
    )
    scheduler = Scheduler(Owner("Jordan", [pet]))

    assert [task.description for task in scheduler.sort_by_time()] == [
        "Breakfast",
        "Lunch",
        "Evening walk",
    ]


def test_filter_tasks_by_pet_and_completion_status() -> None:
    walk = Task("Walk", 20)
    completed_task = Task("Medicine", 5, is_completed=True)
    cat_task = Task("Feed", 5)
    dog = Pet("Mochi", "dog", [walk, completed_task])
    cat = Pet("Miso", "cat", [cat_task])
    scheduler = Scheduler(Owner("Jordan", [dog, cat]))

    assert scheduler.filter_tasks(pet_name="mochi") == [walk, completed_task]
    assert scheduler.filter_tasks(is_completed=False) == [walk, cat_task]
    assert scheduler.filter_tasks(pet_name="MOCHI", is_completed=True) == [
        completed_task
    ]


def test_completing_daily_task_adds_next_occurrence() -> None:
    today = date(2026, 10, 17)
    task = Task("Walk", 20, frequency="daily", scheduled_time="08:30", due_date=today)
    pet = Pet("Mochi", "dog", [task])
    scheduler = Scheduler(Owner("Jordan", [pet]))

    scheduler.mark_complete(task, completed_on=today)

    assert task.is_completed
    assert len(pet.tasks) == 2
    next_task = pet.tasks[1]
    assert next_task.description == task.description
    assert next_task.is_completed is False
    assert next_task.due_date == today + timedelta(days=1)
    assert next_task.scheduled_time == task.scheduled_time


def test_completing_weekly_task_adds_next_occurrence() -> None:
    today = date(2026, 10, 17)
    task = Task("Brush", 15, frequency="weekly", due_date=today)
    pet = Pet("Mochi", "dog", [task])
    scheduler = Scheduler(Owner("Jordan", [pet]))

    scheduler.mark_complete(task, completed_on=today)

    assert len(pet.tasks) == 2
    assert pet.tasks[1].due_date == today + timedelta(days=7)


def test_detect_conflicts_warns_for_shared_date_and_time() -> None:
    today = date(2026, 10, 17)
    dog = Pet(
        "Mochi",
        "dog",
        [Task("Walk", 30, scheduled_time="08:30", due_date=today)],
    )
    cat = Pet(
        "Miso",
        "cat",
        [Task("Medicine", 5, scheduled_time="08:30", due_date=today)],
    )
    scheduler = Scheduler(Owner("Jordan", [dog, cat]))

    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 1
    assert "Mochi: Walk" in warnings[0]
    assert "Miso: Medicine" in warnings[0]
    assert "08:30" in warnings[0]


def test_detect_conflicts_ignores_different_times_and_completed_tasks() -> None:
    today = date(2026, 10, 17)
    pet = Pet(
        "Mochi",
        "dog",
        [
            Task("Walk", 30, scheduled_time="08:30", due_date=today),
            Task("Feed", 5, scheduled_time="09:00", due_date=today),
            Task(
                "Completed medicine",
                5,
                scheduled_time="08:30",
                due_date=today,
                is_completed=True,
            ),
        ],
    )
    scheduler = Scheduler(Owner("Jordan", [pet]))

    assert scheduler.detect_conflicts() == []
    assert scheduler.detect_conflicts([pet.tasks[0], pet.tasks[2]]) == []


def test_scheduler_returns_empty_results_when_owner_has_no_pets() -> None:
    scheduler = Scheduler(Owner("Jordan"))

    assert scheduler.get_all_tasks() == []
    assert scheduler.sort_by_time() == []
    assert scheduler.filter_tasks() == []
    assert scheduler.detect_conflicts() == []
    assert scheduler.create_schedule(60) == []


def test_schedule_excludes_future_due_tasks() -> None:
    future_task = Task(
        "Future checkup",
        30,
        scheduled_time="08:00",
        due_date=date.today() + timedelta(days=1),
    )
    pet = Pet("Mochi", "dog", [future_task])
    scheduler = Scheduler(Owner("Jordan", [pet]))

    assert scheduler.create_schedule(60) == []


def test_completing_same_recurring_task_twice_does_not_duplicate_occurrence() -> None:
    today = date(2026, 10, 17)
    task = Task("Walk", 20, frequency="daily", due_date=today)
    pet = Pet("Mochi", "dog", [task])
    scheduler = Scheduler(Owner("Jordan", [pet]))

    scheduler.mark_complete(task, completed_on=today)
    scheduler.mark_complete(task, completed_on=today)

    assert len(pet.tasks) == 2