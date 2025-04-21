import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib

# Load dataset
data = pd.read_csv("dataset/eco_routes.csv")

X = data[["traffic_time", "aqi"]]
y = data["eco_score"]

# Train Model
model = RandomForestRegressor(n_estimators=100)
model.fit(X, y)

# Save Model
joblib.dump(model, "models/model.pkl")

print("Model trained and saved successfully!")
