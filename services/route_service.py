import requests
import os
from dotenv import load_dotenv

load_dotenv()
OPENROUTE_API_KEY = os.getenv("OPENROUTE_API_KEY")

def get_distance_based_match(customer_lat, customer_lon, cleaner_lat, cleaner_lon):
    """Get distance between customer and cleaner using OpenRouteService"""
    try:
        url = "https://api.openrouteservice.org/v2/directions/driving-car"
        headers = {
            "Authorization": OPENROUTE_API_KEY,
            "Content-Type": "application/json"
        }
        # Correct format: [[lon, lat], [lon, lat]]
        body = {
            "coordinates": [
                [customer_lon, customer_lat],
                [cleaner_lon, cleaner_lat]
            ]
        }
        
        response = requests.post(url, json=body, headers=headers)
        data = response.json()
        
        # Check if request was successful
        if response.status_code != 200:
            return {"error": f"API Error: {data.get('error', {}).get('message', 'Unknown error')}"}
        
        # Correct path for distance
        distance_meters = data["routes"][0]["segments"][0]["distance"]
        distance_km = distance_meters / 1000
        
        return {
            "distance_km": round(distance_km, 2), 
            "message": "Cleaner matched successfully"
        }
    except KeyError as e:
        return {"error": f"Unexpected API response structure: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}