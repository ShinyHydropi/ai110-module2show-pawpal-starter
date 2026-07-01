import pytest

from pawpal_system import Owner, Pet, Schedule, Task


def test_negative_duration_raises_value_error():
    with pytest.raises(ValueError):
        Task("walk", -5, "high")


def test_mark_complete_changes_status():
    task = Task("walk", 30, "high")
    assert task.status == "pending"

    task.mark_complete()

    assert task.status == "completed"


def test_adding_task_increases_pet_task_count():
    pet = Pet("Mo", "dog")
    assert len(pet.tasks) == 0

    pet.add_task(Task("groom", 20, "low"))

    assert len(pet.tasks) == 1


# --- sorting edge cases ---------------------------------------------------


def test_unknown_priority_sorts_after_known_priorities():
    pet = Pet("Mo", "dog")
    owner = Owner("Alex", [pet])
    unknown = Task("mystery", 10, "urgent")
    low = Task("nap", 10, "low")
    pet.add_task(unknown)
    pet.add_task(low)

    schedule = Schedule(owner)
    plan = schedule.build_plan(available_minutes=100)

    activities = [task.activity for _, task in plan]
    assert activities.index("mystery") > activities.index("nap")


def test_priority_is_case_sensitive():
    pet = Pet("Mo", "dog")
    owner = Owner("Alex", [pet])
    capitalized = Task("walk", 10, "High")
    lowercase = Task("feed", 10, "low")
    pet.add_task(capitalized)
    pet.add_task(lowercase)

    schedule = Schedule(owner)
    plan = schedule.build_plan(available_minutes=100)

    activities = [task.activity for _, task in plan]
    assert activities.index("walk") > activities.index("feed")


def test_same_priority_orders_longer_duration_first():
    pet = Pet("Mo", "dog")
    owner = Owner("Alex", [pet])
    short_task = Task("quick pet", 5, "medium")
    long_task = Task("long walk", 45, "medium")
    pet.add_task(short_task)
    pet.add_task(long_task)

    schedule = Schedule(owner)
    plan = schedule.build_plan(available_minutes=100)

    assert [task.activity for _, task in plan] == ["long walk", "quick pet"]


def test_equal_priority_and_duration_preserves_pool_order():
    pet = Pet("Mo", "dog")
    owner = Owner("Alex", [pet])
    first = Task("first", 10, "medium")
    second = Task("second", 10, "medium")
    pet.add_task(first)
    pet.add_task(second)

    schedule = Schedule(owner)
    plan = schedule.build_plan(available_minutes=100)

    assert [task.activity for _, task in plan] == ["first", "second"]


# --- build_plan boundary conditions ---------------------------------------


def test_zero_available_minutes_skips_everything():
    pet = Pet("Mo", "dog")
    owner = Owner("Alex", [pet])
    pet.add_task(Task("walk", 10, "high"))

    schedule = Schedule(owner)
    plan = schedule.build_plan(available_minutes=0)

    assert plan == []
    assert len(schedule._skipped_tasks) == 1


def test_negative_available_minutes_skips_everything():
    pet = Pet("Mo", "dog")
    owner = Owner("Alex", [pet])
    pet.add_task(Task("walk", 10, "high"))

    schedule = Schedule(owner)
    plan = schedule.build_plan(available_minutes=-5)

    assert plan == []


def test_task_duration_exactly_matches_remaining_budget():
    pet = Pet("Mo", "dog")
    owner = Owner("Alex", [pet])
    pet.add_task(Task("walk", 30, "high"))

    schedule = Schedule(owner)
    plan = schedule.build_plan(available_minutes=30)

    assert len(plan) == 1


def test_zero_duration_task_included_even_with_zero_budget():
    pet = Pet("Mo", "dog")
    owner = Owner("Alex", [pet])
    pet.add_task(Task("check tag", 0, "high"))

    schedule = Schedule(owner)
    plan = schedule.build_plan(available_minutes=0)

    assert len(plan) == 1


def test_empty_task_pool_returns_empty_plan():
    pet = Pet("Mo", "dog")
    owner = Owner("Alex", [pet])

    schedule = Schedule(owner)
    plan = schedule.build_plan(available_minutes=60)

    assert plan == []


def test_rebuilding_plan_replaces_previous_results():
    pet = Pet("Mo", "dog")
    owner = Owner("Alex", [pet])
    pet.add_task(Task("walk", 30, "high"))
    pet.add_task(Task("feed", 10, "medium"))

    schedule = Schedule(owner)
    schedule.build_plan(available_minutes=100)
    assert len(schedule._planned_tasks) == 2

    second_plan = schedule.build_plan(available_minutes=0)

    assert second_plan == []
    assert len(schedule._planned_tasks) == 0
    assert len(schedule._skipped_tasks) == 2


# --- recurring task edge cases --------------------------------------------


def test_recurring_task_copies_are_independent_across_schedules():
    pet = Pet("Mo", "dog")
    owner = Owner("Alex", [pet])
    template = Task("walk", 30, "high")

    monday = Schedule(owner)
    tuesday = Schedule(owner)
    Schedule.add_recurring_task([monday, tuesday], pet, template)

    monday.tasks[0][1].mark_complete()

    assert monday.tasks[0][1].status == "completed"
    assert tuesday.tasks[0][1].status == "pending"


def test_recurring_task_does_not_mutate_pet_task_list():
    pet = Pet("Mo", "dog")
    owner = Owner("Alex", [pet])
    template = Task("walk", 30, "high")

    schedule = Schedule(owner)
    Schedule.add_recurring_task([schedule], pet, template)

    assert len(pet.tasks) == 0
    assert len(schedule.tasks) == 1


def test_recurring_task_with_empty_schedule_list_is_noop():
    pet = Pet("Mo", "dog")
    template = Task("walk", 30, "high")

    Schedule.add_recurring_task([], pet, template)
    # No exception means success; nothing to assert on since no schedules exist.


# --- reasoning / printing state -------------------------------------------


def test_get_reasoning_before_build_plan_returns_placeholder():
    pet = Pet("Mo", "dog")
    owner = Owner("Alex", [pet])
    schedule = Schedule(owner)

    assert schedule.get_reasoning() == "No plan has been generated yet. Call build_plan() first."


def test_get_reasoning_lists_skipped_tasks_when_all_skipped():
    pet = Pet("Mo", "dog")
    owner = Owner("Alex", [pet])
    pet.add_task(Task("walk", 30, "high"))

    schedule = Schedule(owner)
    schedule.build_plan(available_minutes=0)
    reasoning = schedule.get_reasoning()

    assert "Skipped (not enough time remaining):" in reasoning
    assert "walk" in reasoning


def test_print_plan_before_build_plan_prints_placeholder(capsys):
    pet = Pet("Mo", "dog")
    owner = Owner("Alex", [pet])
    schedule = Schedule(owner)

    schedule.print_plan()

    captured = capsys.readouterr()
    assert "No plan has been generated yet" in captured.out


# --- owner / pet pooling edge cases ----------------------------------------


def test_duplicate_pet_names_collide_in_get_all_tasks():
    pet_a = Pet("Mo", "dog")
    pet_b = Pet("Mo", "cat")
    pet_a.add_task(Task("walk", 30, "high"))
    pet_b.add_task(Task("scratch post", 10, "low"))
    owner = Owner("Alex", [pet_a, pet_b])

    all_tasks = owner.get_all_tasks()

    # Only one "Mo" entry survives because get_all_tasks keys by name.
    assert list(all_tasks.keys()) == ["Mo"]
    assert len(all_tasks["Mo"]) == 1


def test_schedule_with_explicit_pet_subset_excludes_other_pets_tasks():
    pet_a = Pet("Mo", "dog")
    pet_b = Pet("Rex", "dog")
    pet_a.add_task(Task("walk", 30, "high"))
    pet_b.add_task(Task("feed", 10, "medium"))
    owner = Owner("Alex", [pet_a, pet_b])

    schedule = Schedule(owner, pets=[pet_a])

    assert len(schedule.tasks) == 1
    assert schedule.tasks[0][0] is pet_a
