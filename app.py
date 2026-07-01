from pawpal_system import Owner, Pet, Schedule, Task
import streamlit as st

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
**PawPal+** is a pet care planning assistant. It helps pet owners plan care
tasks for their pets based on constraints like time, priority, and preferences.
"""
)

st.divider()

if "owners" not in st.session_state:
    st.session_state.owners = []  # list[Owner]
if "schedules" not in st.session_state:
    st.session_state.schedules = []  # list[dict]: name, owner_idx, pet_idxs, obj, available_minutes


def all_pet_options():
    """Return (label, owner_idx, pet_idx) for every pet across all owners."""
    options = []
    for oi, owner in enumerate(st.session_state.owners):
        for pi, pet in enumerate(owner.pets):
            options.append((f"{owner.name} / {pet.name}", oi, pi))
    return options


# ---------------------------------------------------------------------------
# Owners & Pets
# ---------------------------------------------------------------------------
st.subheader("Owners & Pets")

with st.form("add_owner_form", clear_on_submit=True):
    new_owner_name = st.text_input("Owner name", placeholder="e.g. Jordan")
    if st.form_submit_button("Add owner") and new_owner_name.strip():
        st.session_state.owners.append(Owner(new_owner_name.strip()))

if not st.session_state.owners:
    st.info("No owners yet. Add one above.")

for oi, owner in enumerate(st.session_state.owners):
    with st.expander(f"👤 {owner.name}", expanded=True):
        with st.form(f"add_pet_form_{oi}", clear_on_submit=True):
            st.markdown("**Add a pet**")
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                pet_name = st.text_input("Pet name", placeholder="e.g. Mochi", key=f"pet_name_{oi}")
            with c2:
                species = st.selectbox("Species", ["dog", "cat", "other"], key=f"species_{oi}")
            with c3:
                breed = st.text_input("Breed", placeholder="optional", key=f"breed_{oi}")
            with c4:
                age = st.number_input("Age", min_value=0, max_value=40, value=0, key=f"age_{oi}")
            if st.form_submit_button("Add pet") and pet_name.strip():
                owner.add_pet(Pet(pet_name.strip(), species, breed=breed, age=int(age) or None))

        if not owner.pets:
            st.caption("No pets yet for this owner.")

        for pi, pet in enumerate(owner.pets):
            with st.expander(f"🐾 {pet.name} ({pet.species})"):
                with st.form(f"add_task_form_{oi}_{pi}", clear_on_submit=True):
                    st.markdown("**Add a task**")
                    t1, t2, t3, t4 = st.columns(4)
                    with t1:
                        task_title = st.text_input(
                            "Task title", placeholder="e.g. Morning walk", key=f"task_title_{oi}_{pi}"
                        )
                    with t2:
                        duration = st.number_input(
                            "Duration (minutes)", min_value=1, max_value=240, value=20, key=f"duration_{oi}_{pi}"
                        )
                    with t3:
                        priority = st.selectbox(
                            "Priority", ["low", "medium", "high"], index=2, key=f"priority_{oi}_{pi}"
                        )
                    with t4:
                        preferences = st.text_input("Preferences", placeholder="optional", key=f"preferences_{oi}_{pi}")
                    if st.form_submit_button("Add task") and task_title.strip():
                        pet.add_task(
                            Task(activity=task_title, duration=int(duration), priority=priority, preferences=preferences)
                        )

                if pet.tasks:
                    st.table(
                        [
                            {
                                "Activity": task.activity,
                                "Duration (min)": task.duration,
                                "Priority": task.priority,
                                "Preferences": task.preferences,
                            }
                            for task in pet.tasks
                        ]
                    )
                else:
                    st.caption("No tasks yet for this pet.")

st.divider()

# ---------------------------------------------------------------------------
# Schedules
# ---------------------------------------------------------------------------
st.subheader("Schedules")
st.caption("Create one or more schedules per owner, each pooling tasks from the selected pets.")

if not st.session_state.owners:
    st.info("Add an owner and at least one pet before creating a schedule.")
else:
    owner_choice = st.selectbox(
        "Owner",
        options=list(range(len(st.session_state.owners))),
        format_func=lambda i: st.session_state.owners[i].name,
        key="schedule_owner_choice",
    )
    owner_obj = st.session_state.owners[owner_choice]

    if not owner_obj.pets:
        st.warning(f"{owner_obj.name} has no pets yet. Add a pet above first.")
    else:
        with st.form("add_schedule_form", clear_on_submit=True):
            pet_choices = st.multiselect(
                "Pets to include",
                options=list(range(len(owner_obj.pets))),
                format_func=lambda i: owner_obj.pets[i].name,
                key="schedule_pet_choice",
            )
            schedule_name = st.text_input("Schedule name", placeholder="e.g. Weekday schedule", key="schedule_name_input")

            if st.form_submit_button("Create schedule"):
                if not pet_choices:
                    st.warning("Select at least one pet for the schedule.")
                else:
                    pets = [owner_obj.pets[i] for i in pet_choices]
                    label = schedule_name.strip() or f"Schedule {len(st.session_state.schedules) + 1}"
                    st.session_state.schedules.append(
                        {
                            "name": label,
                            "owner_idx": owner_choice,
                            "pet_idxs": pet_choices,
                            "obj": Schedule(owner_obj, pets=pets),
                            "available_minutes": 120,
                        }
                    )

if not st.session_state.schedules:
    st.info("No schedules yet. Create one above.")

# ---------------------------------------------------------------------------
# Add one task to multiple schedules at once
# ---------------------------------------------------------------------------
if st.session_state.schedules:
    st.markdown("### Add one task to multiple schedules")
    st.caption("Adds an independent copy of the same task to every schedule you select.")
    pet_options = all_pet_options()

    with st.form("recurring_task_form", clear_on_submit=True):
        r1, r2, r3, r4 = st.columns(4)
        with r1:
            pet_choice = st.selectbox(
                "Pet",
                options=list(range(len(pet_options))),
                format_func=lambda i: pet_options[i][0],
                key="recurring_pet_choice",
            )
        with r2:
            r_title = st.text_input("Task title", placeholder="e.g. Evening walk", key="recurring_title")
        with r3:
            r_duration = st.number_input(
                "Duration (minutes)", min_value=1, max_value=240, value=20, key="recurring_duration"
            )
        with r4:
            r_priority = st.selectbox("Priority", ["low", "medium", "high"], index=2, key="recurring_priority")
        r_preferences = st.text_input("Preferences", placeholder="optional", key="recurring_preferences")

        schedule_targets = st.multiselect(
            "Add to schedules",
            options=list(range(len(st.session_state.schedules))),
            format_func=lambda i: st.session_state.schedules[i]["name"],
            key="recurring_schedule_targets",
        )

        if st.form_submit_button("Add task to selected schedules"):
            if not r_title.strip():
                st.warning("Enter a task title.")
            elif not schedule_targets:
                st.warning("Select at least one schedule.")
            else:
                _, oi, pi = pet_options[pet_choice]
                pet = st.session_state.owners[oi].pets[pi]
                task = Task(activity=r_title, duration=int(r_duration), priority=r_priority, preferences=r_preferences)
                target_schedules = [st.session_state.schedules[i]["obj"] for i in schedule_targets]
                Schedule.add_recurring_task(target_schedules, pet, task)
                st.success(f"Added '{r_title}' to {len(schedule_targets)} schedule(s).")

st.divider()

# ---------------------------------------------------------------------------
# Generate & view schedules
# ---------------------------------------------------------------------------
if st.session_state.schedules:
    st.subheader("Generate Schedules")
    for si, sched in enumerate(st.session_state.schedules):
        owner = st.session_state.owners[sched["owner_idx"]]
        pet_names = ", ".join(owner.pets[i].name for i in sched["pet_idxs"])
        with st.expander(f"📅 {sched['name']} — {owner.name} ({pet_names})", expanded=True):
            pooled = sched["obj"].tasks
            if pooled:
                st.write("Pooled tasks:")
                st.table(
                    [
                        {
                            "Pet": pet.name,
                            "Activity": task.activity,
                            "Duration (min)": task.duration,
                            "Priority": task.priority,
                            "Preferences": task.preferences,
                        }
                        for pet, task in pooled
                    ]
                )
            else:
                st.caption("No tasks pooled in this schedule yet.")

            sched["available_minutes"] = st.number_input(
                "Available time today (minutes)",
                min_value=1,
                max_value=1440,
                value=sched["available_minutes"],
                key=f"available_minutes_{si}",
            )

            if st.button("Generate schedule", key=f"generate_{si}"):
                if not pooled:
                    st.warning("This schedule has no tasks to plan.")
                else:
                    sched["obj"].build_plan(int(sched["available_minutes"]))
                    st.success("Schedule generated!")
                    st.text(sched["obj"].get_reasoning())
