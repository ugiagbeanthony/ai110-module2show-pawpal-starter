"""Core data models and scheduling logic for PawPal+."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Task:
    """A single pet-care activity."""

    description: str
    duration_minutes: int
    frequency: str = "daily"
    is_completed: bool = False
    priority: str = "medium"

    def __post_init__(self) -> None:
        """Normalize task text and validate its scheduling fields."""
        self.description = self.description.strip()
        self.frequency = self.frequency.strip()
        self.priority = self.priority.strip().lower()
        if not self.description:
            raise ValueError("Task description cannot be empty.")
        if self.duration_minutes <= 0:
            raise ValueError("Task duration must be greater than zero minutes.")
        if not self.frequency:
            raise ValueError("Task frequency cannot be empty.")
        if self.priority not in {"low", "medium", "high"}:
            raise ValueError("Task priority must be low, medium, or high.")

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.is_completed = True

    def describe(self) -> str:
        """Return a readable summary of this task."""
        status = "completed" if self.is_completed else "pending"
        return (
            f"{self.description} ({self.duration_minutes} min, "
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

    def organize_tasks(self) -> list[Task]:
        """Return pending tasks ordered by priority, then shorter duration."""
        priority_order = {"high": 0, "medium": 1, "low": 2}
        pending_tasks = [
            task for task in self.owner.get_all_tasks() if not task.is_completed
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

    def mark_complete(self, task: Task) -> None:
        """Mark one of this owner's tasks complete."""
        if not any(owner_task is task for owner_task in self.owner.get_all_tasks()):
            raise ValueError("Cannot complete a task that does not belong to this owner.")
        task.mark_complete()
