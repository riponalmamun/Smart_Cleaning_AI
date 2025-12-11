# routers/chatbot.py
from fastapi import APIRouter, Query
from pydantic import BaseModel
from services.chat_service import ai_chat

router = APIRouter(prefix="/chatbot", tags=["AI Chat Assistant"])


class ChatRequest(BaseModel):
    user_email: str
    message: str
    confirmation: str = None  # Optional: yes/no for appointment


@router.post("/chat")
def chat_with_ai(body: ChatRequest):
    """
    Chat with AI Assistant.
    - Returns AI response
    - Handles conversation history
    - Can confirm appointment if user says 'yes'
    """
    response = ai_chat(
        user_email=body.user_email,
        user_message=body.message,
        confirmation=body.confirmation
    )
    return {"response": response}
