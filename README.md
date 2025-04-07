# Weather App Backend

This Weather App is a Python project that provides real-time weather data, travel suggestions based on weather and activities, YouTube video recommendations, and nearby places based on a given location. The app integrates various external APIs such as OpenWeather, YouTube, and OpenStreetMap for a rich user experience.


## Features

- **Weather Data:** Fetch real-time weather data from the OpenWeather API and store it in MongoDB.
- **Travel Suggestions:** Based on the weather and activity preferences, suggest suitable travel destinations.
- **Activity Suggestions:** Suggest activities based on current weather conditions.
- **Nearby Places:** Fetch nearby places from OpenStreetMap based on the given location.
- **YouTube Videos:** Provide YouTube video recommendations for the specified location.
- **Data Export:** Export weather data in CSV format for analysis.


## Technologies Used

- **Backend:** Flask (Python)
- **Database:** MongoDB
- **APIs:**
  - OpenWeather API (Weather Data)
  - YouTube API (Video Recommendations)
  - OpenStreetMap API (Nearby Places and Geocoding)


## Project Structure

```
weather_app/
│
├── app.py                # Main Flask app file
├── config.py             # Configuration file (includes API keys)
├── db.py                 # MongoDB connection setup
├── services/             # Contains service logic for fetching data from APIs
│   ├── weather_service.py
│   └── ... 
├── requirements.txt      # List of project dependencies
└── README.md             # Project documentation
```

## PM Accelerator Mission 

By making industry-leading tools and education available to individuals from all backgrounds, we level the playing field for future PM leaders. This is the PM Accelerator motto, as we grant aspiring and experienced PMs what they need most – Access. We introduce you to industry leaders, surround you with the right PM ecosystem, and discover the new world of AI product management skills.


## Installation

Follow the steps below to get your environment set up.

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/weather-app.git
cd weather-app
```

### 2. Set up a virtual environment
Create and activate a virtual environment

### 3.Install the required dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Flask Application

```bash
pip install -r requirements.txt
```

## API Endpoints 

### 1. Weather endpoints

POST /weather: Fetch weather data and store it in MongoDB.

```bash
{
  "location": "New York",
  "start_date": "2025-04-01",
  "end_date": "2025-04-07"
}
```

http://127.0.0.1:5000/weather


GET /weather: Retrieve weather records from the database by location.

http://localhost:5000/weather?location=New%20York

PUT /weather/<id>: Update a specific weather record by its ID.

http://127.0.0.1:5000/weather/<id>

```bash
{
  "temperature": 295.15,
  "description": "clear sky"
}
```

DELETE /weather/<id>: Delete a specific weather record by its ID.
http://127.0.0.1:5000/weather/<id>


### 2. Youtube endpoints 

GET /youtube: Fetch YouTube videos related to a specific location.

Example request:

GET http://127.0.0.1:5000/youtube?location=New York

### 3. Nearby Places Endpoint
GET /places: Fetch nearby places from OpenStreetMap for a given location.

Example request:

GET http://127.0.0.1:5000/places?location=New York


### 4. Activity Suggestions
GET /activities: Suggest activities based on weather data for a specific location.

Example request:

GET http://127.0.0.1:5000/activities?location=New%20York

### 5. Travel Suggestions
GET /travel_suggestions: Get travel suggestions based on weather and activity preferences.

Example request:

GET http://127.0.0.1:5000/travel_suggestions?weather=sunny&activity=beach

### 6. Data Export
GET /export/csv: Export weather data from the database as a CSV file.

http://127.0.0.1:5000/export/csv

