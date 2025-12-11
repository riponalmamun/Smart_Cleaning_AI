# test_calendar.py

from services.calendar_service import create_cleaning_event, create_cleaning_task

if __name__ == "__main__":
    print("🔹 Testing: Create Cleaning Event...")
    event_result = create_cleaning_event(
        date_str="2025-11-15",
        title="Test Cleaning Event",
        description="This is a test cleaning event."
    )
    print("Event Result:")
    print(event_result)

    print("\n🔹 Testing: Create Cleaning Task...")
    task_result = create_cleaning_task(
        date_str="2025-11-16",
        task_title="Test Cleaning Task"
    )
    print("Task Result:")
    print(task_result)
