from pawpal_system import Pet, Task


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