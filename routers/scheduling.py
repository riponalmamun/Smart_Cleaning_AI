# routers/scheduling.py - Complete Conversational Flow
from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime, timedelta
import json
import re
from openai import OpenAI
from services.prediction_service import predict_next_schedule
from services.calendar_service import create_calendar_event
from services.conversation_service import save_message, get_user_messages, get_current_conversation
import os

router = APIRouter(prefix="/schedule", tags=["Predictive Scheduling"])

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define services
SERVICES = {
    "1": {
        "name": "Standard Cleaning",
        "description": "Basic cleaning of all rooms, dusting, vacuuming, and surface wiping",
        "duration": 2
    },
    "2": {
        "name": "Deep Cleaning",
        "description": "Thorough cleaning including kitchen appliances, behind furniture, scrubbing bathrooms, and detailed dusting",
        "duration": 4
    },
    "3": {
        "name": "Move-in/Move-out Cleaning",
        "description": "Complete cleaning for vacant properties, including inside cabinets, appliances, and deep scrubbing",
        "duration": 6
    },
    "4": {
        "name": "Post-Construction Cleaning",
        "description": "Removal of construction debris, dust, and thorough cleaning of all surfaces",
        "duration": 8
    },
    "5": {
        "name": "Office Cleaning",
        "description": "Professional cleaning of office spaces, desks, floors, and common areas",
        "duration": 3
    }
}

class ChatMessage(BaseModel):
    message: str
    email: str

@router.get("/")
def auto_schedule(dates: str):
    result = predict_next_schedule(dates)
    return {"predicted_next_schedule": result}


@router.post("/chat")
async def conversational_appointment(body: ChatMessage):
    """
    Complete conversational booking flow:
    1. Greet & Show services
    2. User selects service
    3. Ask for date/time
    4. Confirm booking
    5. Save to calendar
    """
    user_message = body.message.strip()
    user_email = body.email
    
    save_message(user_email, f"User: {user_message}")
    history = get_user_messages(user_email, limit=30)
    
    # Extract conversation state
    selected_service = extract_selected_service(history)
    pending_appointment = extract_pending_appointment(history)
    
    # STEP 4: Handle confirmation
    if pending_appointment:
        if re.search(r'\b(yes|yeah|sure|ok|confirm|yep|correct|right|হ্যাঁ|ঠিক|করুন)\b', user_message.lower()):
            event_result = create_calendar_event(
                title=f"Smart Cleaning - {pending_appointment['service_name']}",
                start_time=pending_appointment["start_time"],
                end_time=pending_appointment["end_time"],
                description=f"{pending_appointment['service_description']}\nBooked via chat assistant",
                email=user_email
            )
            
            if event_result.get("status") == "success":
                response = f"✅ Perfect! Your {pending_appointment['service_name']} appointment is confirmed for {pending_appointment['start_time'].strftime('%B %d, %Y at %I:%M %p')}. I've added it to your Google Calendar. You'll receive reminders before the appointment. Looking forward to serving you!"
                save_message(user_email, f"Bot: {response}")
                save_message(user_email, "BOOKING_CONFIRMED")
                
                return {
                    "response": response,
                    "appointment_confirmed": True,
                    "calendar_event": event_result,
                    "conversation_history": get_current_conversation(user_email)
                }
            else:
                response = f"❌ Error adding to calendar: {event_result.get('message')}. Please contact support."
                save_message(user_email, f"Bot: {response}")
                return {
                    "response": response,
                    "appointment_confirmed": False,
                    "conversation_history": get_current_conversation(user_email)
                }
        
        elif re.search(r'\b(no|nope|cancel|না|বাতিল)\b', user_message.lower()):
            response = "No problem! The appointment wasn't booked. Would you like to schedule a different time or service?"
            save_message(user_email, f"Bot: {response}")
            save_message(user_email, "BOOKING_CANCELLED")
            return {
                "response": response,
                "appointment_confirmed": False,
                "conversation_history": get_current_conversation(user_email)
            }
    
    # Use OpenAI to understand user intent
    try:
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        conversation_context = "\n".join([f"{m['message']}" for m in history[-10:]])
        
        system_prompt = f"""You are a friendly cleaning service booking assistant. Current date/time: {current_date}.

Available Services:
{json.dumps(SERVICES, indent=2)}

Conversation State:
- Selected Service: {selected_service if selected_service else 'None'}
- Pending Appointment: {pending_appointment if pending_appointment else 'None'}

Your task: Analyze the user's message and return JSON:
{{
  "intent": "greeting|service_inquiry|service_selection|datetime_provided|general_question",
  "selected_service_id": "1-5" or null,
  "datetime": "YYYY-MM-DD HH:MM" or null,
  "response": "Your friendly response to the user"
}}

Conversation Flow:
1. If greeting/inquiry → Show services list
2. If service selected → Acknowledge and ask for date/time
3. If date/time provided → Confirm details and ask for final confirmation
4. Always be conversational and friendly"""

        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Previous context:\n{conversation_context}\n\nCurrent message: {user_message}"}
            ],
            temperature=0.7
        )
        
        ai_response = completion.choices[0].message.content
        print(f"DEBUG OpenAI: {ai_response}")
        
        result = json.loads(ai_response)
        intent = result.get("intent")
        response_text = result.get("response")
        
        # STEP 1: Greeting or Service Inquiry
        if intent in ["greeting", "service_inquiry"]:
            if not response_text:
                response_text = "Hello! 👋 Welcome to Smart Cleaning Services. Here are the cleaning services we offer:\n\n"
                for sid, service in SERVICES.items():
                    response_text += f"{sid}. **{service['name']}** ({service['duration']} hours)\n   - {service['description']}\n\n"
                response_text += "Which service would you like to book today?"
            
            save_message(user_email, f"Bot: {response_text}")
            return {
                "response": response_text,
                "appointment_confirmed": False,
                "conversation_history": get_current_conversation(user_email)
            }
        
        # STEP 2: Service Selection
        if intent == "service_selection" and result.get("selected_service_id"):
            service_id = result["selected_service_id"]
            if service_id in SERVICES:
                service = SERVICES[service_id]
                save_message(user_email, f"SELECTED_SERVICE: {service_id}|{service['name']}|{service['duration']}")
                
                if not response_text:
                    response_text = f"Great choice! **{service['name']}** includes:\n{service['description']}\n\nThis typically takes about {service['duration']} hours. When would you like to schedule this service? For example: 'tomorrow at 10 AM' or 'December 15 at 2 PM'"
                
                save_message(user_email, f"Bot: {response_text}")
                return {
                    "response": response_text,
                    "appointment_confirmed": False,
                    "service_selected": service['name'],
                    "conversation_history": get_current_conversation(user_email)
                }
        
        # STEP 3: DateTime Provided
        if result.get("datetime") and selected_service:
            start_time = datetime.strptime(result["datetime"], "%Y-%m-%d %H:%M")
            end_time = start_time + timedelta(hours=selected_service['duration'])
            
            response_text = f"📅 Perfect! Let me confirm your booking:\n\n🧹 Service: **{selected_service['name']}**\n🗓️ Date: {start_time.strftime('%B %d, %Y')}\n🕐 Time: {start_time.strftime('%I:%M %p')}\n⏱️ Duration: {selected_service['duration']} hours\n\n**Does this look good to you?** Reply 'Yes' to confirm or 'No' to reschedule."
            
            save_message(user_email, f"Bot: {response_text}")
            save_message(user_email, f"PENDING_APPOINTMENT: {start_time.isoformat()}|{end_time.isoformat()}|{selected_service['id']}|{selected_service['name']}|{selected_service['description']}")
            
            return {
                "response": response_text,
                "appointment_confirmed": False,
                "pending_confirmation": True,
                "suggested_datetime": start_time.strftime('%Y-%m-%d %H:%M'),
                "conversation_history": get_current_conversation(user_email)
            }
        
        # Default response
        if not response_text:
            response_text = "I'm here to help you book a cleaning service! Could you tell me which service you're interested in, or when you'd like to schedule?"
        
        save_message(user_email, f"Bot: {response_text}")
        return {
            "response": response_text,
            "appointment_confirmed": False,
            "conversation_history": get_current_conversation(user_email)
        }
        
    except Exception as e:
        print(f"Error: {e}")
        response = f"I apologize for the error. Let me help you book a cleaning service. Which of our services interests you?\n\n1. Standard Cleaning (2h)\n2. Deep Cleaning (4h)\n3. Move-in/Move-out (6h)\n4. Post-Construction (8h)\n5. Office Cleaning (3h)"
        save_message(user_email, f"Bot: {response}")
        return {
            "response": response,
            "appointment_confirmed": False,
            "conversation_history": get_current_conversation(user_email)
        }


def extract_selected_service(history):
    """Extract selected service from history"""
    for msg in reversed(history):
        if "BOOKING_CONFIRMED" in msg["message"] or "BOOKING_CANCELLED" in msg["message"]:
            return None
        if "SELECTED_SERVICE:" in msg["message"]:
            try:
                parts = msg["message"].split("SELECTED_SERVICE: ")[1].split("|")
                return {
                    "id": parts[0],
                    "name": parts[1],
                    "duration": int(parts[2]),
                    "description": SERVICES[parts[0]]['description']
                }
            except:
                pass
    return None


def extract_pending_appointment(history):
    """Extract pending appointment from history"""
    for msg in reversed(history):
        if "BOOKING_CONFIRMED" in msg["message"] or "BOOKING_CANCELLED" in msg["message"]:
            return None
        if "PENDING_APPOINTMENT:" in msg["message"]:
            try:
                parts = msg["message"].split("PENDING_APPOINTMENT: ")[1].split("|")
                return {
                    "start_time": datetime.fromisoformat(parts[0]),
                    "end_time": datetime.fromisoformat(parts[1]),
                    "service_id": parts[2],
                    "service_name": parts[3],
                    "service_description": parts[4]
                }
            except:
                pass
    return None