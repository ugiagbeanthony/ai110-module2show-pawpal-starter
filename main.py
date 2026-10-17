"""Run a small multi-pet PawPal+ schedule demo in the terminal."""

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner("Jordan")

    dog = Pet("Mochi", "dog")
    cat = Pet("Miso", "cat")
    owner.add_pet(dog)
    owner.add_pet(cat)

    dog.add_task(
        Task("Morning walk", 30, frequency="daily", priority="high")
    )
    dog.add_task(
        Task("Brush coat", 10, frequency="weekly", priority="low")
    )
    cat.add_task(
        Task("Serve breakfast", 5, frequency="daily", priority="high")
    )

    available_minutes = 45
    schedule = Scheduler(owner).create_schedule(available_minutes)

    print("Today's Schedule")
    print(f"Owner: {owner.name} | Available time: {available_minutes} minutes")
    for task in schedule:
        print(f"- {task.describe()}")
    print(f"Total scheduled: {sum(task.duration_minutes for task in schedule)} minutes")


if __name__ == "__main__":
    main()
