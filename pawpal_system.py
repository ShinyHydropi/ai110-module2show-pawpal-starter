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
    status: str = "pending"

    def mark_complete(self) -> None:
        self.status = "completed"


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
    def __init__(self, owner: Owner, pets: list[Pet] | None = None):
        self.owner = owner
        self.pets: list[Pet] = pets if pets is not None else list(owner.pets)
        self.tasks: list[tuple[Pet, Task]] = [
            (pet, task) for pet in self.pets for task in pet.tasks
        ]
        self._planned_tasks: list[tuple[Pet, Task]] = []
        self._skipped_tasks: list[tuple[Pet, Task]] = []
        self._available_minutes: int | None = None

    def add_task(self, pet: Pet, task: Task) -> None:
        self.tasks.append((pet, task))

    def build_plan(self, available_minutes: int) -> list[tuple[Pet, Task]]:
        """Choose and order tasks that fit within a shared time budget.

        Tasks from all of the owner's pets are pooled together and considered
        in priority order (high, then medium, then low), with longer tasks
        scheduled first within a priority tier so short tasks can be used to
        fill remaining gaps.
        """
        self._available_minutes = available_minutes
        ordered_candidates = sorted(
            self.tasks,
            key=lambda pair: (PRIORITY_ORDER.get(pair[1].priority, len(PRIORITY_ORDER)), -pair[1].duration),
        )

        planned: list[tuple[Pet, Task]] = []
        skipped: list[tuple[Pet, Task]] = []
        remaining = available_minutes
        for pet, task in ordered_candidates:
            if task.duration <= remaining:
                planned.append((pet, task))
                remaining -= task.duration
            else:
                skipped.append((pet, task))

        self._planned_tasks = planned
        self._skipped_tasks = skipped
        return planned

    def print_plan(self) -> None:
        if not self._planned_tasks:
            print("No plan has been generated yet. Call build_plan() first.")
            return

        print(f"Today's schedule for {self.owner.name}'s pets:")
        for index, (pet, task) in enumerate(self._planned_tasks, start=1):
            print(f"{index}. [{pet.name}] {task.activity} ({task.duration} min)")

    def get_reasoning(self) -> str:
        if not self._planned_tasks and not self._skipped_tasks:
            return "No plan has been generated yet. Call build_plan() first."

        lines = [f"Daily plan for {self.owner.name}'s pets:"]
        for index, (pet, task) in enumerate(self._planned_tasks, start=1):
            reason = f"{task.priority} priority"
            if task.preferences:
                reason += f", matches preference '{task.preferences}'"
            lines.append(f"{index}. [{pet.name}] {task.activity} ({task.duration} min) - {reason}")

        if self._skipped_tasks:
            lines.append("Skipped (not enough time remaining):")
            for pet, task in self._skipped_tasks:
                lines.append(f"- [{pet.name}] {task.activity} ({task.duration} min, {task.priority} priority)")

        return "\n".join(lines)
