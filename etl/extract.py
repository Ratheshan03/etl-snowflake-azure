import os
import requests
import json 
from dotenv import load_dotenv

load_dotenv(override=True)

API_KEY = os.getenv("OPENWEATHER_API_KEY")

CITIES = ["London", "Chennai", "New York", "Kandy", "Colombo"]

BASE_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric"

def fetch_weather_data():
    weather_data = []

    for city in CITIES:
        apiUrl = BASE_URL.format(city, API_KEY)
        response = requests.get(apiUrl)
        if response.status_code == 200:
            response_data = response.json()
            weather_data.append(response_data)
        else:
            print(f"Failed to fetch data for {city}: {response.status_code}")
            print(response.text)


    # Get absolute path to the data directory
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))

    # Create the directory if it doesn't exist
    os.makedirs(data_dir, exist_ok=True)

    file_path = os.path.join(data_dir, "raw_weather.json")

    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            json.dump([], file) 
    

    with open(file_path, "w") as file:
        json.dump(weather_data, file, indent=4)

    print(f"Weather data saved to {file_path}")

if __name__ == "__main__":
    fetch_weather_data()
