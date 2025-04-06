import azure.functions as func
import os
import logging
from dotenv import load_dotenv

from etl.extract import run_extract
from etl.transform import run_transform
from etl.load import run_load

app = func.FunctionApp()

@app.timer_trigger(schedule="0 */30 * * * *", arg_name="myTimer", run_on_startup=True, use_monitor=False) 
def etl_trigger(myTimer: func.TimerRequest) -> None:
    logging.info('🔁 Starting automated ETL...')

    try:
        # Load environment variables from the .env file in the current root directory
        env_path = os.path.join(os.path.dirname(__file__), '.env')
        if os.path.exists(env_path):
            load_dotenv(env_path)

        # Run ETL directly
        run_extract()
        run_transform()
        run_load()

        logging.info("✅ ETL pipeline ran successfully!")

    except Exception as e:
        logging.error(f"❌ ETL pipeline failed: {e}")
