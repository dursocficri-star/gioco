import math
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory


app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 2048
APP_DIR = Path(__file__).resolve().parent


@app.get("/")
def index():
    return send_from_directory(APP_DIR, "index.html")


@app.post("/api/location")
def log_location():
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or data.get("consent") is not True:
        return jsonify(error="Consenso esplicito richiesto."), 400

    latitude = data.get("latitude")
    longitude = data.get("longitude")
    accuracy = data.get("accuracy")
    values = (latitude, longitude, accuracy)
    if any(
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        for value in values
    ):
        return jsonify(error="Coordinate non valide."), 400
    if not (-90 <= latitude <= 90 and -180 <= longitude <= 180 and accuracy >= 0):
        return jsonify(error="Coordinate fuori intervallo."), 400

    app.logger.info(
        "location consent=true latitude=%.6f longitude=%.6f accuracy_m=%.1f",
        latitude,
        longitude,
        accuracy,
    )
    return jsonify(ok=True), 202
