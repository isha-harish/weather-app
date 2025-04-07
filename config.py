MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "weather_app"

import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
