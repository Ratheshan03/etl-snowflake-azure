import snowflake.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connect to Snowflake
try:
    conn = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
    )
    print("✅ Successfully connected to Snowflake!")
    conn.close()
    
except Exception as e:
    print(f"❌ Snowflake connection failed: {e}")
