import json
import os
import pandas as pd
from datetime import datetime, timezone
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

CSV_FILE_PATH = os.path.join(DATA_DIR, "clean_weather.csv")
JSON_FILE_PATH = os.path.join(DATA_DIR, "raw_weather.json")

def transform_data():
    # Load raw data
    with open(JSON_FILE_PATH, "r") as file:
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
            "wind_gust_m/s": city_data["wind"].get("gust", None),
            "cloud_coverage_%": city_data["clouds"]["all"],
            "weather_main": city_data["weather"][0]["main"],
            "weather_description": city_data["weather"][0]["description"],
            "visibility_m": city_data["visibility"],
            "sunrise_utc": datetime.fromtimestamp(city_data["sys"]["sunrise"]).strftime('%Y-%m-%d %H:%M:%S'),
            "sunset_utc": datetime.fromtimestamp(city_data["sys"]["sunset"]).strftime('%Y-%m-%d %H:%M:%S'),
        })

    df = pd.DataFrame(transformed_data)
    df.to_csv(CSV_FILE_PATH, index=False, mode="w", header=True)
    print(f"Transformed data saved to {CSV_FILE_PATH}")

    upload_to_blob()

def upload_to_blob():
    try:
        connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        container_name = os.getenv("AZURE_CONTAINER_NAME")

        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob="clean_weather.csv")

        with open(CSV_FILE_PATH, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

        print("Uploaded clean_weather.csv to Azure Blob Storage!")

    except Exception as e:
        print(f"Failed to upload to Azure Blob: {e}")

if __name__ == "__main__":
    transform_data()