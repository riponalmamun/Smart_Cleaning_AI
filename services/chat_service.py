# services/chat_service.py
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from services.conversation_service import get_user_messages, save_message
from config import OPENAI_API_KEY

# Set the OpenAI API key
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Initialize the chat model
chat_model = ChatOpenAI(model_name="gpt-4", temperature=0.7)

def ai_chat(user_email: str, user_message: str) -> str:
    """
    Chat with AI assistant using conversation history.
    """
    # Save user message
    save_message(user_email, f"User: {user_message}")

    # Retrieve last 10 conversation messages for context
    history = get_user_messages(user_email)
    messages = [SystemMessage(content="You are a helpful AI assistant for Smart Cleaning services.")]

    for msg in history[-10:]:
        messages.append(HumanMessage(content=msg['message']))

    # Get AI response
    ai_response = chat_model(messages=messages).content

    # Save AI response
    save_message(user_email, f"Bot: {ai_response}")

    return ai_response


def cohere_chatbot(prompt):
    """
    Simple chatbot function using OpenAI (for compatibility with scheduling.py)
    """
    try:
        messages = [
            SystemMessage(content="You are a helpful cleaning service assistant."),
            HumanMessage(content=prompt)
        ]
        response = chat_model(messages=messages).content
        return response
    except Exception as e:
        return f"Error: {str(e)}"