import requests

def get_directions(source, destination):
    api_key = "AIzaSyAg3FyW8z4g-XJQhwoH-pbC2tlFa8c7Crk"
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": source,
        "destination": destination,
        "key": api_key
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()
