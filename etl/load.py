import os
import snowflake.connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Snowflake Connection
def get_snowflake_connection():
    """Establish a connection to Snowflake"""
    try:
        conn = snowflake.connector.connect(
            user=os.getenv("SNOWFLAKE_USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
            database=os.getenv("SNOWFLAKE_DATABASE"),
            schema=os.getenv("SNOWFLAKE_SCHEMA"),
        )
        print("Connected to Snowflake!")
        return conn
    except Exception as e:
        print(f"Failed to connect to Snowflake: {e}")
        return None

# Load Data from Azure Blob to Snowflake
def load_data_to_snowflake():
    conn = get_snowflake_connection()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        
        # Copy data into the Snowflake table
        copy_sql = """
        COPY INTO weather_data (TIMESTAMP, CITY, COUNTRY, LATITUDE, LONGITUDE, TEMPERATURE_C, 
                        FEELS_LIKE_C, MIN_TEMP_C, MAX_TEMP_C, PRESSURE_HPA, HUMIDITY, 
                        WIND_SPEED_M_S, WIND_DIRECTION_DEG, WIND_GUST_M_S, CLOUD_COVERAGE_PERCENT, 
                        WEATHER_MAIN, WEATHER_DESCRIPTION, VISIBILITY_M, SUNRISE_UTC, SUNSET_UTC)
        FROM @azure_weather_stage/clean_weather.csv
        FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY='"' SKIP_HEADER = 1);
        """
        
        cursor.execute(copy_sql)
        print("Data successfully loaded into Snowflake!")
    
    except Exception as e:
        print(f"Error loading data: {e}")
    
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    load_data_to_snowflake()
