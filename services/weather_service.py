import requests
from config import OPENWEATHER_API_KEY, YOUTUBE_API_KEY
from datetime import datetime
import logging
import urllib.parse


# Set up logging to capture API requests and responses
logging.basicConfig(level=logging.DEBUG)

def get_lat_lon_from_city(city_name):
    encoded_city_name = urllib.parse.quote(city_name)
    geocode_url = f"https://nominatim.openstreetmap.org/search?format=json&q={encoded_city_name}"
    
    headers = {
        "User-Agent": "WeatherApp/1.0 (https://yourwebsite.com; theishaharish@gmail.com)"  # Add a User-Agent string
    }

    logging.debug(f"Geocode URL: {geocode_url}")  # Log the URL being requested
    response = requests.get(geocode_url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        logging.debug(f"Geocode Response: {data}")  # Log the response data
        
        if data:
            lat = data[0]['lat']
            lon = data[0]['lon']
            logging.debug(f"Latitude: {lat}, Longitude: {lon}")  # Log latitude and longitude
            return {"lat": lat, "lon": lon}
        else:
            logging.error(f"Location not found for: {city_name}")  # Log if location not found
            return {"error": "Location not found"}
    else:
        logging.error(f"Failed to fetch geocode data for: {city_name}, Status Code: {response.status_code}")  # Log error response
        return {"error": "Failed to fetch geocode data"}
# Fetch weather data from OpenWeather API
def fetch_weather_from_api(location, start_timestamp, end_timestamp):
    if isinstance(location, str):  # If it's a city name (string)
        location = get_lat_lon_from_city(location)  # Convert city name to lat/lon

    logging.debug(f"Location data: {location}")

    # Now location is a dictionary with lat and lon
    url = f"http://api.openweathermap.org/data/2.5/onecall/timemachine?lat={location['lat']}&lon={location['lon']}&dt={start_timestamp}&appid={OPENWEATHER_API_KEY}"
    
    logging.debug(f"Fetching weather data from URL: {url}")
    
    response = requests.get(url)
    logging.debug(f"Response code: {response.status_code}")
    
    if response.status_code == 200:
        weather_data = response.json()
        logging.debug(f"Weather data received: {weather_data}")
        return weather_data
    else:
        logging.error(f"Error from API when fetching weather data: {response.json()}")
        return {"error": "Failed to fetch weather data"}

def get_weather_data(location, start_date_str, end_date_str):
    # Convert start and end date strings to datetime objects
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    # Convert datetime objects to timestamps
    start_timestamp = int(start_date.timestamp())
    end_timestamp = int(end_date.timestamp())

    logging.debug(f"Start timestamp: {start_timestamp}, End timestamp: {end_timestamp}")

    # Fetch the weather data using the one-call API endpoint
    weather_data = fetch_weather_from_api(location, start_timestamp, end_timestamp)
    return weather_data

# Fetch YouTube videos related to a location
def fetch_youtube_videos(location):
    # URL encode the location query for YouTube search
    encoded_location = urllib.parse.quote(location)
    youtube_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={encoded_location}&key={YOUTUBE_API_KEY}"
    
    logging.debug(f"Fetching YouTube videos from URL: {youtube_url}")
    
    response = requests.get(youtube_url)
    logging.debug(f"Response code: {response.status_code}")
    
    if response.status_code == 200:
        youtube_data = response.json()
        logging.debug(f"YouTube data received: {youtube_data}")
        return youtube_data
    else:
        logging.error(f"Error fetching YouTube data: {response.json()}")
        return {"error": "Failed to fetch YouTube data"}

# Fetch nearby places from OpenStreetMap using reverse geocoding
def fetch_nearby_places(location):
    location_data = get_lat_lon_from_city(location)
    if "lat" in location_data and "lon" in location_data:
        lat = location_data['lat']
        lon = location_data['lon']
        
        # Use reverse geocoding or other available endpoints
        nearby_url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
        
        # Adding a User-Agent header for compliance with OSM's usage policy
        headers = {
            "User-Agent": "WeatherApp/1.0 (https://yourwebsite.com; your_email@example.com)"
        }
        
        response = requests.get(nearby_url, headers=headers)
        if response.status_code == 200:
            places_data = response.json()
            return places_data
        else:
            # If reverse geocoding fails, provide detailed error message
            return {"error": f"Failed to fetch nearby places. Status Code: {response.status_code}, Response: {response.text}"}
    else:
        return {"error": "Invalid location data"}
    

def suggest_activity(weather_data):
    temperature = weather_data.get("main", {}).get("temp", 0)
    weather_description = weather_data.get("weather", [{}])[0].get("description", "").lower()
    activities = []

    # Based on temperature
    if temperature > 30:
        activities.append("Go to the beach")
    elif temperature > 20:
        activities.append("Go for a hike or walk in the park")
    elif temperature > 10:
        activities.append("Visit a museum or art gallery")
    else:
        activities.append("Indoor activities like cooking or reading")

    # Based on weather conditions
    if "rain" in weather_description or "snow" in weather_description:
        activities.append("Stay inside, maybe watch a movie or read a book")

    if "sun" in weather_description:
        activities.append("Enjoy outdoor sports like tennis or cycling")

    return activities

def suggest_travel_destinations(preferences):
    preferred_weather = preferences.get("weather", "").lower()
    preferred_activity = preferences.get("activity", "").lower()
    recommended_destinations = []

    # Example destinations and their weather conditions
    destinations = {
        "Los Angeles": {"weather": "sunny", "temp": 28, "activity": "beach"},
        "New York": {"weather": "cloudy", "temp": 15, "activity": "city tour"},
        "Miami": {"weather": "sunny", "temp": 30, "activity": "beach"},
        "Aspen": {"weather": "snowy", "temp": -5, "activity": "skiing"},
    }

    for destination, data in destinations.items():
        # Filter destinations based on preferences
        if preferred_weather in data["weather"] and preferred_activity in data["activity"]:
            recommended_destinations.append(destination)

    return recommended_destinations
