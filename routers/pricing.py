# routes/pricing.py

from fastapi import APIRouter
from services.prediction_service import suggest_price

router = APIRouter(
    prefix="/price",
    tags=["Intelligent Pricing"]
)

@router.get("/")
def intelligent_pricing(area: str, frequency: int, rating: float):
    """
    Recommend a fair cleaning price
    Example: /price/?area=Dhanmondi&frequency=2&rating=4.5
    """
    result = suggest_price(area, frequency, rating)
    # Ensure the response is a flat JSON
    if "recommended_price" in result and isinstance(result["recommended_price"], dict) and "error" in result["recommended_price"]:
        # Return empty string if error key exists but is empty
        return {"recommended_price": ""}
    return result
