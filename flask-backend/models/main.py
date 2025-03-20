from flask import Flask, render_template, request, jsonify, send_file, url_for
import joblib
import numpy as np
import cv2
import tensorflow as tf
import matplotlib.pyplot as plt
import io
import os
import logging
import subprocess
import time
import pickle
from datetime import datetime
import pandas as pd
from tensorflow.keras.models import load_model
from flask_cors import CORS
import requests  # For USGS API

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG)

# Define file paths
BASE_PATH = r"C:\Users\Niharika Kashyap\Documents\jupyter[1]\jupyter"
flood_model_path = os.path.join(BASE_PATH, "flood2.pkl")  # Updated to flood.pkl

# Load flood model
try:
    flood_model = joblib.load(flood_model_path)
    logging.info("Flood model loaded successfully.")
except Exception as e:
    logging.error(f"Error loading flood model: {e}")
    flood_model = None

# USGS API URL for earthquake data
USGS_API_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"
@app.route('/predict_flood', methods=['POST'])
def predict_flood():
    try:
        data = request.get_json()
        latitude = float(data["latitude"])
        longitude = float(data["longitude"])
        rainfall = float(data["rainfall"])

        if flood_model is None:
            return jsonify({'error': "Flood model not loaded."}), 500
        
        flood_input = np.array([[latitude, longitude, rainfall]])
        flood_probability = flood_model.predict(flood_input)[0]

        if hasattr(flood_model, "predict_proba"):
            flood_probability = flood_model.predict_proba(flood_input)[0][1]

        flood_risk = "Low Risk"
        if flood_probability > 0.8:
            flood_risk = "High Risk"
        elif flood_probability > 0.5:
            flood_risk = "Moderate Risk"

        return jsonify({
            'flood_probability': round(flood_probability, 2),
            'flood_risk': flood_risk
        })
    except Exception as e:
        logging.error(f"Error in predict_flood: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/predict_earthquake', methods=['POST'])
def predict_earthquake():
    try:
        data = request.get_json()
        latitude = float(data["latitude"])
        longitude = float(data["longitude"])

        params = {
            "format": "geojson",
            "latitude": latitude,
            "longitude": longitude,
            "maxradiuskm": 100,
            "limit": 5,
            "orderby": "time"
        }
        response = requests.get(USGS_API_URL, params=params)
        earthquake_data = response.json()

        earthquakes = []
        for feature in earthquake_data.get("features", []):
            properties = feature.get("properties", {})
            earthquakes.append({
                "magnitude": properties.get("mag", "N/A"),
                "place": properties.get("place", "Unknown location"),
                "time": properties.get("time", "N/A")
            })

        if not earthquakes:
            return jsonify({"message": "No recent earthquakes found in this area."})

        return jsonify({"earthquakes": earthquakes})

    except Exception as e:
        logging.error(f"Error in predict_earthquake: {e}")
        return jsonify({"error": str(e)}), 400

# Start all Flask apps in the background
APPS = [
    ("app1.py", 5001),
    ("app2.py", 5002),
]

processes = []
for app_file, port in APPS:
    proc = subprocess.Popen(["python", app_file])
    processes.append(proc)
    time.sleep(2)  # Small delay to ensure apps start

# Home route
@app.route("/")
def home():
    return """
        <h1>Main App</h1>
        <ul>
            <li><a href="http://127.0.0.1:5001/">Go to App 1</a></li>
            <li><a href="http://127.0.0.1:5002/">Go to App 2</a></li>
        </ul>
    """

if __name__ == "__main__":
    app.run(port=5000, debug=True)