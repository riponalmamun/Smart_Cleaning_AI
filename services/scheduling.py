# services/scheduling.py
from datetime import datetime, timedelta
import dateparser
from services.calendar_service import create_calendar_event
from services.conversation_service import save_message, get_user_messages


def parse_date_from_message(message: str):
    """
    Try to extract a datetime from a user message using dateparser.
    """
    keywords = ["book", "appointment", "schedule", "cleaning"]
    
    # Primary parsing
    parsed_date = dateparser.parse(
        message,
        languages=["en"],
        settings={
            "PREFER_DATES_FROM": "future",
            "TIMEZONE": "Asia/Dhaka",
            "RETURN_AS_TIMEZONE_AWARE": False,
            "RELATIVE_BASE": datetime.now(),
            "STRICT_PARSING": True
        }
    )

    if parsed_date:
        return parsed_date

    # Fallback: remove keywords and try again
    filtered_msg = message.lower()
    for kw in keywords:
        filtered_msg = filtered_msg.replace(kw, "")
    
    parsed_date = dateparser.parse(
        filtered_msg,
        languages=["en"],
        settings={
            "PREFER_DATES_FROM": "future",
            "TIMEZONE": "Asia/Dhaka",
            "RETURN_AS_TIMEZONE_AWARE": False,
            "RELATIVE_BASE": datetime.now()
        }
    )
    return parsed_date


def create_chat_appointment(user_email: str, message: str, service_name: str = "Smart Cleaning"):
    """
    Create a Google Calendar appointment based on a user message.
    Saves conversation history and returns event details.
    """
    # Save user message
    save_message(user_email, f"User: {message}")

    # Parse date
    appointment_time = parse_date_from_message(message)
    if not appointment_time:
        response = "Could not detect date/time from your message."
        save_message(user_email, f"Bot: {response}")
        return {"status": "error", "response": response}

    start_time = appointment_time
    end_time = start_time + timedelta(hours=1)

    # Create calendar event
    event_result = create_calendar_event(
        title=f"{service_name} Appointment",
        start_time=start_time,
        end_time=end_time,
        description=f"Auto-booked based on chat: '{message}'",
        email=user_email
    )

    # Prepare bot response
    response = f"✅ Appointment created for {start_time.strftime('%Y-%m-%d %H:%M')}"

    # Save bot response
    save_message(user_email, f"Bot: {response}")

    # Retrieve conversation history
    conversation_history = get_user_messages(user_email)

    return {
        "status": "success",
        "response": response,
        "calendar_event": event_result,
        "conversation_history": conversation_history
    }
