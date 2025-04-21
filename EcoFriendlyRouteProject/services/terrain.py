import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Load API keys from .env file

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
ELEVATION_API_URL = "https://maps.googleapis.com/maps/api/elevation/json"

def get_terrain_data(source, destination):
    try:
        # Convert source & destination to latitude-longitude (if needed)
        source_coords = get_lat_long(source)
        dest_coords = get_lat_long(destination)

        # Get elevation data for both points
        source_elevation = fetch_elevation(source_coords)
        dest_elevation = fetch_elevation(dest_coords)

        return {
            "source_elevation": source_elevation,
            "destination_elevation": dest_elevation,
            "terrain_type": classify_terrain(source_elevation, dest_elevation)
        }
    except Exception as e:
        return {"error": str(e)}

def get_lat_long(location):
    """Fetch latitude and longitude of a location using Google Geocoding API"""
    geo_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(geo_url).json()
    if response["status"] == "OK":
        latlong = response["results"][0]["geometry"]["location"]
        return latlong["lat"], latlong["lng"]
    return None

def fetch_elevation(coords):
    """Get elevation for given coordinates"""
    lat, lng = coords
    response = requests.get(f"{ELEVATION_API_URL}?locations={lat},{lng}&key={GOOGLE_MAPS_API_KEY}")
    data = response.json()
    if "results" in data:
        return data["results"][0]["elevation"]
    return None

def classify_terrain(source_elevation, dest_elevation):
    """Classify terrain based on elevation difference"""
    elevation_diff = abs(source_elevation - dest_elevation)
    if elevation_diff < 10:
        return "Flat Terrain"
    elif elevation_diff < 100:
        return "Hilly Terrain"
    else:
        return "Mountainous Terrain"

