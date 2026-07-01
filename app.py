from pawpal_system import Owner, Pet, Schedule, Task
import streamlit as st

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care
tasks for their pet based on constraints like time, priority, and preferences.
"""
)

st.divider()

st.subheader("Owner & Pet")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

st.markdown("### Tasks")
st.caption("Add a few care tasks for your pet.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with col4:
    preferences = st.text_input("Preferences", value="")

if st.button("Add task"):
    st.session_state.tasks.append(
        Task(activity=task_title, duration=int(duration), priority=priority, preferences=preferences)
    )

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(
        [
            {
                "Activity": task.activity,
                "Duration (min)": task.duration,
                "Priority": task.priority,
                "Preferences": task.preferences,
            }
            for task in st.session_state.tasks
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
available_minutes = st.number_input("Available time today (minutes)", min_value=1, max_value=1440, value=120)

if st.button("Generate schedule"):
    if not st.session_state.tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        pet = Pet(pet_name, species, tasks=list(st.session_state.tasks))
        owner = Owner(owner_name, pets=[pet])
        schedule = Schedule(owner)
        schedule.build_plan(int(available_minutes))

        st.success("Schedule generated!")
        st.text(schedule.get_reasoning())
