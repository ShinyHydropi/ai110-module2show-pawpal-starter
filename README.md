# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## ✨ Features

- **Task tracking** — `Task` stores an activity, duration, priority, and optional preferences, and can be marked complete with `mark_complete()`.
- **Pet management** — `Pet` holds a list of care tasks; `add_task()` appends a new task to a pet's list.
- **Multi-pet owners** — `Owner` holds a list of pets; `add_pet()` adds a pet, and `get_all_tasks()` returns every pet's tasks keyed by pet name.
- **Schedule pooling** — `Schedule` pools tasks from one or more of an owner's pets at creation time; `add_task()` adds a single additional task to the pool.
- **Recurring tasks across schedules** — the static method `Schedule.add_recurring_task()` adds an independent copy of the same task to each schedule in a given list, so a repeating task doesn't have to be re-entered for every schedule.
- **Priority-based plan building** — `build_plan()` sorts pooled tasks by priority (high → low), then duration, and greedily fits as many as possible into the available time budget, keeping track of both planned and skipped tasks.
- **Plan output** — `print_plan()` prints a numbered daily plan to the console; `get_reasoning()` returns a human-readable explanation of the plan, including why each task was included and which were skipped for lack of time.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
Today's schedule for McCrea's pets:
1. [Mo] walk (30 min)
2. [Mo] do a trick (40 min)
3. [Eve] do a trick (40 min)
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Test output:

```
============================================== test session starts ===============================================
platform win32 -- Python 3.13.5, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\fredd\Python_files\ai110-module2show-pawpal-starter
plugins: anyio-4.13.0
collected 21 items                                                                                                

tests\test_pawpal.py .....................                                                                  [100%]

=============================================== 21 passed in 0.07s ===============================================
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | build_plan() | e.g., by priority, duration |
| Filtering | build_plan() | e.g., skip tasks if time runs out |
| Recurring tasks | add_recurring_task | e.g., across schedules for multiple days |

## 📸 Demo Walkthrough

### UI features & actions

- **Owners & Pets** — Add any number of owners by name. Each owner gets an expandable card where you can add any number of pets (name, species, breed, age). Each pet gets its own nested card for adding tasks (title, duration, priority, preferences) and viewing that pet's task table.
- **Schedules** — Pick an owner, multiselect which of their pets to include, and name the schedule to create it. You can create multiple schedules per owner (e.g., "Weekday" and "Weekend"), each pooling tasks from a different subset of pets.
- **Add one task to multiple schedules** — Pick a pet, fill in a task once, and select any number of existing schedules; an independent copy of the task is added to each one, backed by `Schedule.add_recurring_task()`.
- **Generate Schedules** — Each schedule card shows its pooled tasks, lets you set the available minutes for the day, and has its own "Generate schedule" button that runs `build_plan()` and displays the reasoning.

### Example workflow

1. Add owner "McCrea".
2. Add two pets under McCrea: "Mo" (dog) and "Eve" (frog).
3. Add tasks to Mo: "walk" (30 min, high priority), "groom" (20 min, low priority), "do a trick" (40 min, medium priority).
4. Add the task "do a trick" (40 min, medium priority) to Eve as well.
5. Create a schedule named "Today" for McCrea, including both Mo and Eve.
6. Set "Available time today" to 120 minutes and click "Generate schedule".
7. Review the plan and reasoning: high-priority tasks are scheduled first, and any tasks that don't fit are listed as skipped.

### Key Scheduler behaviors

- Tasks are pooled from a schedule's pets at creation time (or added later via `add_task()`/`add_recurring_task()`) — adding a task directly to a pet afterward does not automatically re-pool it into existing schedules.
- `build_plan()` orders candidates by priority first (high → medium → low), then by duration (longest first among equal priority), and greedily fills the available time budget.
- Tasks that don't fit in the remaining time are recorded as skipped rather than dropped; both planned and skipped tasks are explained in `get_reasoning()`.
- `add_recurring_task()` copies each task independently, so completing or editing one schedule's copy doesn't affect the same task on another schedule.

### Sample CLI output (`main.py`)

```
Today's schedule for McCrea's pets:
1. [Mo] walk (30 min)
2. [Mo] do a trick (40 min)
3. [Eve] do a trick (40 min)
```