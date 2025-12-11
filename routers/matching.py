from fastapi import APIRouter, Query
from services.route_service import get_distance_based_match

router = APIRouter(prefix="/match", tags=["Smart Job Matching"])

@router.get("/")
def match_cleaner(customer_lat: float, customer_lon: float, cleaner_lat: float, cleaner_lon: float):
    """Suggest best cleaner based on distance"""
    result = get_distance_based_match(customer_lat, customer_lon, cleaner_lat, cleaner_lon)
    return result
