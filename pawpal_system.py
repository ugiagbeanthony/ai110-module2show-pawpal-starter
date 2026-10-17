"""Core data models and scheduling logic for PawPal+."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta


@dataclass
class Task:
    """A single pet-care activity."""

    description: str
    duration_minutes: int
    frequency: str = "daily"
    is_completed: bool = False
    priority: str = "medium"
    scheduled_time: str = "09:00"
    due_date: date = field(default_factory=date.today)

    def __post_init__(self) -> None:
        """Normalize task text and validate its scheduling fields."""
        self.description = self.description.strip()
        self.frequency = self.frequency.strip().lower()
        self.priority = self.priority.strip().lower()
        self.scheduled_time = self.scheduled_time.strip()
        if not self.description:
            raise ValueError("Task description cannot be empty.")
        if self.duration_minutes <= 0:
            raise ValueError("Task duration must be greater than zero minutes.")
        if not self.frequency:
            raise ValueError("Task frequency cannot be empty.")
        if self.priority not in {"low", "medium", "high"}:
            raise ValueError("Task priority must be low, medium, or high.")
        try:
            parsed_time = datetime.strptime(self.scheduled_time, "%H:%M")
        except ValueError as error:
            raise ValueError("Scheduled time must use HH:MM 24-hour format.") from error
        if parsed_time.strftime("%H:%M") != self.scheduled_time:
            raise ValueError("Scheduled time must use HH:MM 24-hour format.")

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.is_completed = True

    def next_occurrence(self, completed_on: date | None = None) -> Task | None:
        """Create the next daily or weekly occurrence after the completion date."""
        interval_days = {"daily": 1, "weekly": 7}.get(self.frequency)
        if interval_days is None:
            return None

        base_date = max(self.due_date, completed_on or date.today())
        return Task(
            description=self.description,
            duration_minutes=self.duration_minutes,
            frequency=self.frequency,
            priority=self.priority,
            scheduled_time=self.scheduled_time,
            due_date=base_date + timedelta(days=interval_days),
        )

    def describe(self) -> str:
        """Return a readable summary of this task."""
        status = "completed" if self.is_completed else "pending"
        return (
            f"{self.scheduled_time} {self.description} "
            f"({self.duration_minutes} min, "
            f"{self.frequency}, {self.priority} priority, {status})"
        )


@dataclass
class Pet:
    """A pet and its care tasks."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Normalize pet details and reject missing names or species."""
        self.name = self.name.strip()
        self.species = self.species.strip()
        if not self.name:
            raise ValueError("Pet name cannot be empty.")
        if not self.species:
            raise ValueError("Pet species cannot be empty.")

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a care task, raising ValueError if it is not attached."""
        self.tasks.remove(task)


@dataclass
class Owner:
    """An owner who manages multiple pets."""

    name: str
    pets: list[Pet] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Normalize the owner's name and reject an empty name."""
        self.name = self.name.strip()
        if not self.name:
            raise ValueError("Owner name cannot be empty.")

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's care."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet, raising ValueError if it is not owned."""
        self.pets.remove(pet)

    def get_all_tasks(self) -> list[Task]:
        """Return all tasks from every pet in the owner's care."""
        return [task for pet in self.pets for task in pet.tasks]


@dataclass
class Scheduler:
    """Retrieves, organizes, and manages tasks for all of an owner's pets."""

    owner: Owner

    def get_all_tasks(self) -> list[Task]:
        """Retrieve tasks through the owner's multi-pet accessor."""
        return self.owner.get_all_tasks()

    def sort_by_time(self, tasks: list[Task] | None = None) -> list[Task]:
        """Sort tasks by due date and their zero-padded HH:MM clock time."""
        tasks_to_sort = self.owner.get_all_tasks() if tasks is None else tasks
        return sorted(tasks_to_sort, key=lambda task: (task.due_date, task.scheduled_time))

    def filter_tasks(
        self,
        pet_name: str | None = None,
        is_completed: bool | None = None,
    ) -> list[Task]:
        """Filter all owner tasks by pet name, completion state, or both."""
        matching_tasks: list[Task] = []
        for pet in self.owner.pets:
            if pet_name is not None and pet.name.casefold() != pet_name.strip().casefold():
                continue
            matching_tasks.extend(
                task
                for task in pet.tasks
                if is_completed is None or task.is_completed is is_completed
            )
        return matching_tasks

    def detect_conflicts(self, tasks: list[Task] | None = None) -> list[str]:
        """Return warnings for pending tasks with the same date and start time."""
        tasks_to_check = (
            self.filter_tasks(is_completed=False)
            if tasks is None
            else [task for task in tasks if not task.is_completed]
        )
        task_pets = {
            id(task): pet.name
            for pet in self.owner.pets
            for task in pet.tasks
        }
        tasks_by_slot: dict[tuple[date, str], list[Task]] = {}
        for task in tasks_to_check:
            slot = (task.due_date, task.scheduled_time)
            tasks_by_slot.setdefault(slot, []).append(task)

        warnings: list[str] = []
        for (due_date, scheduled_time), tasks_at_slot in sorted(tasks_by_slot.items()):
            if len(tasks_at_slot) < 2:
                continue
            descriptions = ", ".join(
                f"{task_pets.get(id(task), 'Unknown pet')}: {task.description}"
                for task in tasks_at_slot
            )
            warnings.append(
                f"Warning: {descriptions} share {scheduled_time} on {due_date:%Y-%m-%d}."
            )
        return warnings

    def organize_tasks(self) -> list[Task]:
        """Return due pending tasks ordered by priority, then shorter duration."""
        priority_order = {"high": 0, "medium": 1, "low": 2}
        pending_tasks = [
            task
            for task in self.owner.get_all_tasks()
            if not task.is_completed and task.due_date <= date.today()
        ]
        return sorted(
            pending_tasks,
            key=lambda task: (
                priority_order[task.priority],
                task.duration_minutes,
                task.description.casefold(),
            ),
        )

    def create_schedule(self, available_minutes: int) -> list[Task]:
        """Select priority-ordered pending tasks that fit the time budget."""
        if available_minutes < 0:
            raise ValueError("Available time cannot be negative.")

        scheduled_tasks: list[Task] = []
        remaining_minutes = available_minutes
        for task in self.organize_tasks():
            if task.duration_minutes <= remaining_minutes:
                scheduled_tasks.append(task)
                remaining_minutes -= task.duration_minutes
        return scheduled_tasks

    def mark_complete(self, task: Task, completed_on: date | None = None) -> None:
        """Complete an owned task and add its next daily or weekly occurrence."""
        pet = next(
            (
                owner_pet
                for owner_pet in self.owner.pets
                if any(owner_task is task for owner_task in owner_pet.tasks)
            ),
            None,
        )
        if pet is None:
            raise ValueError("Cannot complete a task that does not belong to this owner.")
        if task.is_completed:
            return

        task.mark_complete()
        next_task = task.next_occurrence(completed_on)
        if next_task is not None:
            pet.add_task(next_task)
