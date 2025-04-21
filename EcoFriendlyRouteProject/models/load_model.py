import joblib
import numpy as np

model = joblib.load("models/model.pkl")  # Load trained ML model

def predict_route(source, destination, traffic_data, aqi_data):
    traffic = traffic_data["routes"][0]["legs"][0]["duration"]["value"]
    aqi = aqi_data["results"][0]["measurements"][0]["value"]

    features = np.array([[traffic, aqi]])
    eco_score = model.predict(features)[0]
    
    return round(eco_score, 2)
