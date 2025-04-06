import azure.functions as func
import datetime
import json
import os
import subprocess
from dotenv import load_dotenv
import logging

app = func.FunctionApp()

@app.timer_trigger(schedule="0 */5 * * * *", arg_name="myTimer", run_on_startup=True, use_monitor=False) 
def etl_trigger(myTimer: func.TimerRequest) -> None:
    logging.info('🔁 Starting automated ETL...')

    try:
        # Load environment variables from the .env file in the current root directory
        env_path = os.path.join(os.path.dirname(__file__), '.env')
        if os.path.exists(env_path):
            load_dotenv(env_path)

        # Define the path to your ETL scripts (etl is now a subfolder here)
        base_etl_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'etl'))

        # Run ETL scripts
        subprocess.run(['python', os.path.join(base_etl_dir, 'extract.py')], check=True)
        subprocess.run(['python', os.path.join(base_etl_dir, 'transform.py')], check=True)
        subprocess.run(['python', os.path.join(base_etl_dir, 'load.py')], check=True)

        logging.info("✅ ETL pipeline ran successfully!")

    except Exception as e:
        logging.error(f"❌ ETL pipeline failed: {e}")