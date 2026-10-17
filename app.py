from datetime import date, time
from pathlib import Path

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

DATA_FILE = Path(__file__).with_name("data.json")


def save_owner(owner: Owner) -> None:
    """Persist the current owner data to the app's JSON data file."""
    owner.save_to_json(DATA_FILE)


def mark_task_complete(owner: Owner, task: Task) -> None:
    """Complete a task, create its recurrence if applicable, and persist it."""
    Scheduler(owner).mark_complete(task)
    save_owner(owner)


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.caption("Plan care tasks for all of your pets.")

if "owner" not in st.session_state:
    try:
        if DATA_FILE.exists():
            st.session_state["owner"] = Owner.load_from_json(DATA_FILE)
        else:
            st.session_state["owner"] = Owner("Jordan")
            save_owner(st.session_state["owner"])
    except (OSError, ValueError, TypeError, KeyError) as error:
        st.error(f"Could not load PawPal data from {DATA_FILE.name}: {error}")
        st.stop()

owner: Owner = st.session_state["owner"]

with st.form("owner_form"):
    owner_name = st.text_input("Owner name", value=owner.name)
    owner_submitted = st.form_submit_button("Save owner")

if owner_submitted:
    if owner_name.strip():
        owner.name = owner_name.strip()
        save_owner(owner)
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
        save_owner(owner)
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
            save_owner(owner)
            st.success(f"Added a task for {owner.pets[pet_index].name}.")
        else:
            st.error("Enter a description for the task.")

    scheduler = Scheduler(owner)
    st.subheader("Care tasks")
    filter_col, status_col = st.columns(2)
    with filter_col:
        selected_pet = st.selectbox(
            "Filter by pet",
            ["All pets", *(pet.name for pet in owner.pets)],
            key="task_pet_filter",
        )
    with status_col:
        selected_status = st.selectbox(
            "Filter by status",
            ["All", "Pending", "Completed"],
            key="task_status_filter",
        )

    filtered_tasks = scheduler.filter_tasks(
        pet_name=None if selected_pet == "All pets" else selected_pet,
        is_completed={
            "Pending": False,
            "Completed": True,
        }.get(selected_status),
    )
    sorted_tasks = scheduler.sort_by_time(filtered_tasks)
    pet_names_by_task_id = {
        id(task): pet.name for pet in owner.pets for task in pet.tasks
    }

    if sorted_tasks:
        st.table(
            [
                {
                    "Due date": task.due_date.isoformat(),
                    "Time": task.scheduled_time,
                    "Pet": pet_names_by_task_id[id(task)],
                    "Task": task.description,
                    "Duration": f"{task.duration_minutes} min",
                    "Priority": task.priority.title(),
                    "Frequency": task.frequency,
                    "Status": "Completed" if task.is_completed else "Pending",
                }
                for task in sorted_tasks
            ]
        )
        pending_tasks = [task for task in sorted_tasks if not task.is_completed]
        if pending_tasks:
            task_to_complete = st.selectbox(
                "Select a pending task to complete",
                pending_tasks,
                format_func=lambda task: (
                    f"{pet_names_by_task_id[id(task)]}: {task.description} "
                    f"({task.due_date:%Y-%m-%d} at {task.scheduled_time})"
                ),
                key="task_to_complete",
            )
            st.button(
                "Mark selected task complete",
                key="complete_selected_task",
                on_click=mark_task_complete,
                args=(owner, task_to_complete),
            )
    else:
        st.info("No tasks match those filters.")

    conflict_warnings = scheduler.detect_conflicts()
    if conflict_warnings:
        st.subheader("Schedule warnings")
        for warning in conflict_warnings:
            st.warning(warning)
        st.caption(
            "These pending tasks share an exact start time. Consider changing "
            "one task's scheduled time before relying on today's plan."
        )

    st.subheader("Find an available time")
    with st.form("available_slot_form"):
        slot_date = st.date_input("Date to check", value=date.today())
        slot_duration = st.number_input(
            "Task duration (minutes)", min_value=1, max_value=240, value=20
        )
        slot_start_time = st.time_input("Search starting at", value=time(7, 0))
        slot_end_time = st.time_input("Search until", value=time(22, 0))
        slot_submitted = st.form_submit_button("Find next available slot")

    if slot_submitted:
        try:
            slot = scheduler.find_next_available_slot(
                due_date=slot_date,
                duration_minutes=int(slot_duration),
                start_time=slot_start_time.strftime("%H:%M"),
                end_time=slot_end_time.strftime("%H:%M"),
            )
        except ValueError as error:
            st.error(str(error))
        else:
            if slot is None:
                st.warning("No available slot fits within that time window.")
            else:
                st.success(
                    f"Next available slot: {slot_date:%Y-%m-%d} at {slot} "
                    f"({int(slot_duration)} minutes)."
                )

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
        schedule = scheduler.sort_by_priority_and_time(
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
