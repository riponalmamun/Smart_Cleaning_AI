# services/prediction_service.py
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load API keys from .env
load_dotenv()
HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Initialize Hugging Face Inference Client
client = InferenceClient(token=HF_API_KEY)


def predict_next_schedule(dates: str):
    """
    Predicts the next cleaning schedule based on given dates.
    :param dates: Comma-separated string of dates (YYYY-MM-DD)
    :return: Predicted next schedule text
    """
    prompt = f"Given these cleaning dates: {dates}, suggest the next optimal cleaning date in YYYY-MM-DD format."
    
    try:
        response = client.text_generation(
            model="google/flan-t5-base",  # Upgraded model
            prompt=prompt,
            max_new_tokens=30
        )
        return {"predicted_next_schedule": response.strip()}
    except Exception as e:
        # Fallback: simple date prediction
        import datetime
        date_list = [datetime.datetime.strptime(d.strip(), "%Y-%m-%d") for d in dates.split(",")]
        if len(date_list) >= 2:
            interval = (date_list[-1] - date_list[-2]).days
            next_date = date_list[-1] + datetime.timedelta(days=interval)
            return {"predicted_next_schedule": next_date.strftime("%Y-%m-%d")}
        return {"predicted_next_schedule": f"Error: {str(e)}"}


def suggest_price(area: str, frequency: int, rating: float):
    """
    Suggest a cleaning price based on area, frequency, and rating.
    :param area: Name of the area (e.g., Dhanmondi)
    :param frequency: Cleaning frequency per month
    :param rating: Customer rating (1-5)
    :return: Suggested price text
    """
    prompt = (
        f"What is a fair price in BDT for cleaning service in {area} area, "
        f"{frequency} times per month, customer rating {rating}/5? Answer with just the price."
    )
    
    try:
        response = client.text_generation(
            model="google/flan-t5-base",  # Upgraded model
            prompt=prompt,
            max_new_tokens=30
        )
        return {"recommended_price": response.strip()}
    except Exception as e:
        # Fallback: simple pricing logic
        base_price = 1500  # Base price in BDT
        area_multiplier = 1.2 if area.lower() in ["gulshan", "banani", "dhanmondi"] else 1.0
        frequency_discount = 0.9 if frequency >= 4 else 1.0
        rating_bonus = 1 + (rating - 3) * 0.1  # ±10% per rating point from 3.0
        
        price = base_price * area_multiplier * frequency_discount * rating_bonus
        return {"recommended_price": f"BDT {int(price)} per session"}


def chatbot_response(query: str):
    """
    Generate AI chatbot response for a user query.
    :param query: User question or request
    :return: AI-generated response
    """
    prompt = f"Answer the following question as a helpful assistant: {query}"
    
    try:
        response = client.text_generation(
            model="google/flan-t5-base",  # Upgraded model
            prompt=prompt,
            max_new_tokens=100
        )
        return {"response": response.strip()}
    except Exception as e:
        return {"response": f"Error: {str(e)}"}