import os
import requests
import json 
from dotenv import load_dotenv

load_dotenv(override=True)

API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITIES = ["London", "Chennai", "New York", "Kandy", "Colombo"]
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric"

# Get absolute path to the data directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = "/tmp"
os.makedirs(DATA_DIR, exist_ok=True)
FILE_PATH = os.path.join(DATA_DIR, "raw_weather.json")

def fetch_weather_data():
    weather_data = []

    for city in CITIES:
        apiUrl = BASE_URL.format(city, API_KEY)
        response = requests.get(apiUrl)
        if response.status_code == 200:
            weather_data.append(response.json())
        else:
            print(f"Failed to fetch data for {city}: {response.status_code}")
            print(response.text)

    with open(FILE_PATH, "w") as file:
        json.dump(weather_data, file, indent=4)

    print(f"Weather data saved to {FILE_PATH}")

def run_extract():
    fetch_weather_data()
