"""Core data models and scheduling interface for PawPal+."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Task:
    """A care activity that may be included in a pet's daily plan."""

    title: str
    duration_minutes: int
    priority: str

    def describe(self) -> str:
        pass


@dataclass
class Pet:
    """A pet and the care tasks associated with it."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task: Task) -> None:
        pass


@dataclass
class DailyPlan:
    """A pet's proposed care plan for a given amount of available time."""

    pet: Pet
    available_minutes: int
    tasks: list[Task] = field(default_factory=list)
    explanations: list[str] = field(default_factory=list)

    def build_schedule(self) -> None:
        pass

    def total_duration(self) -> int:
        pass

    def explain_schedule(self) -> list[str]:
        pass


@dataclass
class Owner:
    """An owner who manages pets and their care preferences."""

    name: str
    pets: list[Pet] = field(default_factory=list)
    preferences: list[str] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass

    def remove_pet(self, pet: Pet) -> None:
        pass

    def create_daily_plan(self, pet: Pet, available_minutes: int) -> DailyPlan:
        pass
