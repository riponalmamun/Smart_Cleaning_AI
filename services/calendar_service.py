# services/calendar_service.py
import os
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# -----------------------------
# Google Calendar API scope
# -----------------------------
SCOPES = ['https://www.googleapis.com/auth/calendar']


# -----------------------------
# Google Calendar Connection
# -----------------------------
def get_calendar_service():
    """
    Authenticate and return a Google Calendar service instance.
    Uses OAuth 2.0 token for persistent login.
    """
    creds = None
    token_path = 'token.json'
    creds_path = 'credentials.json'

    # Load existing credentials if available
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # Refresh or create new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save credentials
        with open(token_path, 'w') as token_file:
            token_file.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
        print("✅ Google Calendar service created successfully.")
        return service
    except HttpError as e:
        print(f"❌ Failed to create Google Calendar service: {e}")
        return None


# -----------------------------
# Standard Cleaning Event
# -----------------------------
def create_cleaning_event(date_str: str, title: str = "Cleaning Appointment",
                          description: str = "", duration_hours: int = 2):
    """
    Create a cleaning calendar event on a specific date.
    Example: create_cleaning_event("2025-11-15", "Kitchen Cleaning")
    """
    try:
        service = get_calendar_service()
        if not service:
            return {"status": "error", "message": "Failed to connect to Google Calendar."}

        event_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        start_time = event_date.replace(hour=9, minute=0)
        end_time = start_time + datetime.timedelta(hours=duration_hours)

        event_body = {
            "summary": title,
            "description": description,
            "start": {"dateTime": start_time.isoformat(), "timeZone": "Asia/Dhaka"},
            "end": {"dateTime": end_time.isoformat(), "timeZone": "Asia/Dhaka"},
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "email", "minutes": 24 * 60},  # 1 day before
                    {"method": "popup", "minutes": 60}        # 1 hour before
                ]
            },
            "colorId": "5"  # Yellow
        }

        created_event = service.events().insert(calendarId='primary', body=event_body).execute()
        return {
            "status": "success",
            "event_id": created_event.get("id"),
            "event_link": created_event.get("htmlLink"),
            "summary": created_event.get("summary"),
            "start_time": created_event["start"].get("dateTime"),
            "message": "Event created successfully in Google Calendar."
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}


# -----------------------------
# Cleaning Task (All-Day)
# -----------------------------
def create_cleaning_task(date_str: str, task_title: str = "Cleaning Task"):
    """
    Create an all-day cleaning task as a Google Calendar event.
    Example: create_cleaning_task("2025-11-15")
    """
    try:
        service = get_calendar_service()
        if not service:
            return {"status": "error", "message": "Failed to connect to Google Calendar."}

        event_body = {
            "summary": f"📋 {task_title}",
            "start": {"date": date_str, "timeZone": "Asia/Dhaka"},
            "end": {"date": date_str, "timeZone": "Asia/Dhaka"},
            "reminders": {"useDefault": False},
            "colorId": "11"  # Red
        }

        created_task = service.events().insert(calendarId='primary', body=event_body).execute()
        return {
            "status": "success",
            "task_id": created_task.get("id"),
            "task_link": created_task.get("htmlLink"),
            "summary": created_task.get("summary"),
            "date": date_str,
            "message": "Task created successfully in Google Calendar."
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}


# -----------------------------
# AI / Chat-based Appointment
# -----------------------------
def create_calendar_event(title: str, start_time: datetime.datetime,
                          end_time: datetime.datetime, description: str, email: str):
    """
    Create a calendar event dynamically (used for chat-based AI scheduling).
    """
    try:
        service = get_calendar_service()
        if not service:
            return {"status": "error", "message": "Failed to connect to Google Calendar."}

        event = {
            "summary": title,
            "description": description,
            "start": {"dateTime": start_time.isoformat(), "timeZone": "Asia/Dhaka"},
            "end": {"dateTime": end_time.isoformat(), "timeZone": "Asia/Dhaka"},
            "attendees": [{"email": email}],
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "email", "minutes": 30},
                    {"method": "popup", "minutes": 10}
                ]
            },
            "colorId": "2"  # Green
        }

        created_event = service.events().insert(calendarId="primary", body=event).execute()

        return {
            "status": "success",
            "event_id": created_event.get("id"),
            "event_link": created_event.get("htmlLink"),
            "summary": created_event.get("summary"),
            "start_time": created_event["start"].get("dateTime"),
            "message": "AI-based appointment created successfully."
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
