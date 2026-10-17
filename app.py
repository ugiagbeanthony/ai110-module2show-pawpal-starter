from datetime import date

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.caption("Plan care tasks for all of your pets.")

if "owner" not in st.session_state:
    st.session_state["owner"] = Owner("Jordan")

owner: Owner = st.session_state["owner"]

with st.form("owner_form"):
    owner_name = st.text_input("Owner name", value=owner.name)
    owner_submitted = st.form_submit_button("Save owner")

if owner_submitted:
    if owner_name.strip():
        owner.name = owner_name.strip()
        st.success("Owner name saved.")
    else:
        st.error("Owner name cannot be empty.")

st.subheader(f"{owner.name}'s pets")

with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    pet_submitted = st.form_submit_button("Add pet")

if pet_submitted:
    if pet_name.strip():
        owner.add_pet(Pet(name=pet_name, species=species))
        st.success(f"Added {pet_name.strip()} to your pets.")
    else:
        st.error("Enter a name for the pet.")

if not owner.pets:
    st.info("Add a pet to start tracking care tasks.")
else:
    with st.form("add_task_form", clear_on_submit=True):
        pet_index = st.selectbox(
            "Pet",
            options=list(range(len(owner.pets))),
            format_func=lambda index: (
                f"{owner.pets[index].name} ({owner.pets[index].species})"
            ),
        )
        description = st.text_input("Task description")
        duration_minutes = st.number_input(
            "Duration (minutes)", min_value=1, max_value=240, value=20
        )
        frequency = st.selectbox(
            "Frequency", ["daily", "twice daily", "weekly", "as needed"]
        )
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        scheduled_time = st.time_input("Scheduled time")
        due_date = st.date_input("Due date", value=date.today())
        task_submitted = st.form_submit_button("Add task")

    if task_submitted:
        if description.strip():
            owner.pets[pet_index].add_task(
                Task(
                    description=description,
                    duration_minutes=int(duration_minutes),
                    frequency=frequency,
                    priority=priority,
                    scheduled_time=scheduled_time.strftime("%H:%M"),
                    due_date=due_date,
                )
            )
            st.success(f"Added a task for {owner.pets[pet_index].name}.")
        else:
            st.error("Enter a description for the task.")

    st.subheader("Pets and care tasks")
    scheduler = Scheduler(owner)
    for index, pet in enumerate(owner.pets):
        with st.expander(f"{pet.name} ({pet.species})", expanded=True):
            if not pet.tasks:
                st.write("No care tasks yet.")
            for task_index, task in enumerate(scheduler.sort_by_time(pet.tasks)):
                status = "Completed" if task.is_completed else "Pending"
                st.write(f"{task.describe()}")
                st.button(
                    "Mark complete",
                    key=f"complete_{index}_{task_index}",
                    disabled=task.is_completed,
                    on_click=scheduler.mark_complete,
                    args=(task,),
                )
                st.caption(f"Status: {status}")

    conflict_warnings = scheduler.detect_conflicts()
    if conflict_warnings:
        st.subheader("Schedule warnings")
        for warning in conflict_warnings:
            st.warning(warning)

    st.subheader("Today's schedule")
    with st.form("schedule_form"):
        available_minutes = st.number_input(
            "Time available today (minutes)",
            min_value=0,
            max_value=1440,
            value=60,
        )
        schedule_submitted = st.form_submit_button("Generate schedule")

    if schedule_submitted:
        schedule = scheduler.sort_by_time(
            scheduler.create_schedule(int(available_minutes))
        )
        if schedule:
            for task in schedule:
                pet_name_for_task = next(
                    pet.name
                    for pet in owner.pets
                    if any(pet_task is task for pet_task in pet.tasks)
                )
                st.write(
                    f"- **{task.scheduled_time} — {pet_name_for_task}:** "
                    f"{task.description} "
                    f"({task.duration_minutes} min, {task.priority} priority)"
                )
            total_minutes = sum(task.duration_minutes for task in schedule)
            st.caption(
                f"Scheduled {len(schedule)} task(s), totaling {total_minutes} minutes."
            )
        else:
            st.info("No pending tasks fit into the available time.")
