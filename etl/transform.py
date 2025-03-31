import json
import os
import pandas as pd
from datetime import datetime, timezone

CSV_FILE_PATH = "data/clean_weather.csv"

def transform_data():
    # Load raw data
    with open("data/raw_weather.json", "r") as file:
        data = json.load(file)

    transformed_data = []
    for city_data in data:
        transformed_data.append({
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            "city": city_data["name"],
            "country": city_data["sys"]["country"],
            "latitude": city_data["coord"]["lat"],
            "longitude": city_data["coord"]["lon"],
            "temperature_C": city_data["main"]["temp"],
            "feels_like_C": city_data["main"]["feels_like"],
            "min_temp_C": city_data["main"]["temp_min"],
            "max_temp_C": city_data["main"]["temp_max"],
            "pressure_hPa": city_data["main"]["pressure"],
            "humidity_%": city_data["main"]["humidity"],
            "wind_speed_m/s": city_data["wind"]["speed"],
            "wind_direction_deg": city_data["wind"]["deg"],
            "wind_gust_m/s": city_data["wind"].get("gust", None),  # Handle missing gust values
            "cloud_coverage_%": city_data["clouds"]["all"],
            "weather_main": city_data["weather"][0]["main"],
            "weather_description": city_data["weather"][0]["description"],
            "visibility_m": city_data["visibility"],
            "sunrise_utc": datetime.fromtimestamp(city_data["sys"]["sunrise"]).strftime('%Y-%m-%d %H:%M:%S'),
            "sunset_utc": datetime.fromtimestamp(city_data["sys"]["sunset"]).strftime('%Y-%m-%d %H:%M:%S'),
        })

    # Convert to DataFrame
    df = pd.DataFrame(transformed_data)

    if not os.path.exists(CSV_FILE_PATH):
        df.to_csv(CSV_FILE_PATH, index=False, mode="w", header=True)
    else:
        df.to_csv(CSV_FILE_PATH, index=False, mode="a", header=False)

    print(f"✅ Transformed data saved to {CSV_FILE_PATH}")

if __name__ == "__main__":
    transform_data()
