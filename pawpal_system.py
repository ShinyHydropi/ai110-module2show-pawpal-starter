"""Core scheduling logic for PawPal+."""

from __future__ import annotations

from dataclasses import dataclass, field

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Task:
    activity: str
    duration: int
    priority: str
    preferences: str = ""


@dataclass
class Pet:
    name: str
    species: str
    breed: str = ""
    age: int | None = None
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)


@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def get_all_tasks(self) -> dict[str, list[Task]]:
        return {pet.name: list(pet.tasks) for pet in self.pets}


class Schedule:
    def __init__(self, pet_name: str, tasks: list[Task] | None = None):
        self.pet_name = pet_name
        self.tasks: list[Task] = tasks if tasks is not None else []
        self._planned_tasks: list[Task] = []
        self._skipped_tasks: list[Task] = []
        self._available_minutes: int | None = None

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def build_plan(self, available_minutes: int) -> list[Task]:
        """Choose and order tasks that fit within available_minutes.

        Tasks are considered in priority order (high, then medium, then low),
        and within a priority tier, longer tasks are scheduled first so short
        tasks can be used to fill remaining gaps.
        """
        self._available_minutes = available_minutes
        ordered_candidates = sorted(
            self.tasks,
            key=lambda task: (PRIORITY_ORDER.get(task.priority, len(PRIORITY_ORDER)), -task.duration),
        )

        planned: list[Task] = []
        skipped: list[Task] = []
        remaining = available_minutes
        for task in ordered_candidates:
            if task.duration <= remaining:
                planned.append(task)
                remaining -= task.duration
            else:
                skipped.append(task)

        self._planned_tasks = planned
        self._skipped_tasks = skipped
        return planned

    def get_reasoning(self) -> str:
        if not self._planned_tasks and not self._skipped_tasks:
            return "No plan has been generated yet. Call build_plan() first."

        lines = [f"Daily plan for {self.pet_name}:"]
        for index, task in enumerate(self._planned_tasks, start=1):
            reason = f"{task.priority} priority"
            if task.preferences:
                reason += f", matches preference '{task.preferences}'"
            lines.append(f"{index}. {task.activity} ({task.duration} min) - {reason}")

        if self._skipped_tasks:
            lines.append("Skipped (not enough time remaining):")
            for task in self._skipped_tasks:
                lines.append(f"- {task.activity} ({task.duration} min, {task.priority} priority)")

        return "\n".join(lines)
