import requests

AQI_API_URL = "https://api.openaq.org/v2/latest"

def get_aqi_data(location):
    try:
        # Make request to OpenAQ API
        response = requests.get(f"{AQI_API_URL}?city={location}")
        data = response.json()

        if "results" in data and len(data["results"]) > 0:
            aqi_info = data["results"][0]["measurements"]
            return {
                "PM2.5": next((x["value"] for x in aqi_info if x["parameter"] == "pm25"), None),
                "PM10": next((x["value"] for x in aqi_info if x["parameter"] == "pm10"), None),
                "NO2": next((x["value"] for x in aqi_info if x["parameter"] == "no2"), None),
                "O3": next((x["value"] for x in aqi_info if x["parameter"] == "o3"), None)
            }
        return {"error": "No AQI data available for this location"}
    except Exception as e:
        return {"error": str(e)}
