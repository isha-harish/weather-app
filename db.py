from flask_pymongo import PyMongo
from flask import Flask
from config import OPENWEATHER_API_KEY

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/weather_app"  # Your MongoDB URI
mongo = PyMongo(app)

# Accessing the collection
weather_data = mongo.db.weather_data
