from flask import Flask, request, jsonify, Response, send_file
from db import mongo
from services.weather_service import get_weather_data, fetch_youtube_videos, fetch_nearby_places
from services.weather_service import suggest_activity, suggest_travel_destinations

from bson.objectid import ObjectId
import requests
import csv
import io
import dicttoxml
from config import OPENWEATHER_API_KEY

app = Flask(__name__)

# Helper function to convert ObjectId to string for proper JSON serialization
def object_id_to_str(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, dict):
        return {key: object_id_to_str(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [object_id_to_str(item) for item in obj]
    else:
        return obj

# ---------------------------------------------
# CRUD Endpoints
# ---------------------------------------------

# CREATE: Fetch weather data from OpenWeather and store it in MongoDB
@app.route("/weather", methods=["POST"])
def fetch_weather():
    try:
        data = request.get_json()
        location = data.get("location")  # e.g., 'New York'
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        
        # (Optional) Validate that start_date is before end_date
        if start_date and end_date:
            if start_date > end_date:
                return jsonify({"error": "start_date must be before end_date"}), 400
        
        # Make a request to the OpenWeatherMap API for current weather data
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPENWEATHER_API_KEY}"
        response = requests.get(url)
        
        if response.status_code == 200:
            weather_data = response.json()
            weather_data = {
                "location": location,
                "temperature": weather_data["main"]["temp"],
                "description": weather_data["weather"][0]["description"],
                "humidity": weather_data["main"]["humidity"],
                "date": weather_data["dt"],  # Timestamp of the weather data
            }

            # Insert the weather data into MongoDB
            mongo.db.weather_data.insert_one(weather_data)

            # Convert ObjectId fields for proper JSON serialization
            weather_data = object_id_to_str(weather_data)

            return jsonify({"message": "Weather data saved successfully", "data": weather_data}), 201
        else:
            return jsonify({"error": "Failed to fetch weather data", "status_code": response.status_code}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


# READ: Retrieve weather records from the database
@app.route("/weather", methods=["GET"])
def get_weather_records():
    try:
        location = request.args.get("location")
        query = {"location": location} if location else {}
        records = list(mongo.db.weather_data.find(query))
        records = object_id_to_str(records)
        return jsonify(records), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# UPDATE: Update a specific weather record by its ID
@app.route("/weather/<id>", methods=["PUT"])
def update_weather(id):
    try:
        update_data = request.get_json()
        result = mongo.db.weather_data.update_one({"_id": ObjectId(id)}, {"$set": update_data})
        if result.modified_count:
            return jsonify({"message": "Record updated successfully"}), 200
        else:
            return jsonify({"error": "Record not found or no changes made"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# DELETE: Delete a specific weather record by its ID
@app.route("/weather/<id>", methods=["DELETE"])
def delete_weather(id):
    try:
        result = mongo.db.weather_data.delete_one({"_id": ObjectId(id)})
        if result.deleted_count:
            return jsonify({"message": "Record deleted successfully"}), 200
        else:
            return jsonify({"error": "Record not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------------------------------------
# Additional API Integration: YouTube Videos
# ---------------------------------------------
@app.route("/youtube", methods=["GET"])
def get_youtube_videos():
    try:
        location = request.args.get("location")
        if not location:
            return jsonify({"error": "location parameter is required"}), 400
        youtube_data = fetch_youtube_videos(location)
        return jsonify(youtube_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------------------------------------
# Nearby Places (OpenStreetMap)
# ---------------------------------------------
@app.route("/places", methods=["GET"])
def get_nearby_places():
    try:
        location = request.args.get("location")
        if not location:
            return jsonify({"error": "location parameter is required"}), 400
        places_data = fetch_nearby_places(location)
        return jsonify(places_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------------------------------------
# Data Export Endpoints
# ---------------------------------------------

# Export data as CSV
@app.route("/export/csv", methods=["GET"])
def export_csv():
    try:
        data = list(mongo.db.weather_data.find())
        output = io.StringIO()
        writer = csv.writer(output)
        # Write header row
        writer.writerow(["_id", "location", "temperature", "description", "humidity", "date"])
        for record in data:
            record = object_id_to_str(record)
            writer.writerow([
                record.get("_id", ""),
                record.get("location", ""),
                record.get("temperature", ""),
                record.get("description", ""),
                record.get("humidity", ""),
                record.get("date", "")
            ])
        output.seek(0)
        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=weather_data.csv"}
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/activities", methods=["GET"])
def get_activity_suggestions():
    try:
        location = request.args.get("location")
        if not location:
            return jsonify({"error": "Location parameter is required"}), 400

        weather_data = get_weather_data(location, "2025-04-07", "2025-04-07")  # Date can be dynamically set
        activities = suggest_activity(weather_data)
        
        return jsonify({"suggested_activities": activities}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/travel_suggestions", methods=["GET"])
def get_travel_suggestions():
    try:
        preferences = request.args
        if not preferences.get("weather") or not preferences.get("activity"):
            return jsonify({"error": "Weather and activity preferences are required"}), 400
        
        destinations = suggest_travel_destinations(preferences)
        if destinations:
            return jsonify({"recommended_destinations": destinations}), 200
        else:
            return jsonify({"error": "No destinations match your preferences"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)