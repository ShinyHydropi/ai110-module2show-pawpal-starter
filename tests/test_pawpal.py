from pawpal_system import Pet, Task


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
