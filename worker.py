import os
import time
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from backend.app import database, models  # container context includes repo root

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('worker.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def run_job():
    try:
        utc_now = datetime.utcnow().isoformat()
        logger.info(f"Worker heartbeat at {utc_now}")
        
        # Add your job logic here
        # For example, process pending transactions
        # update_account_balances()
        # process_scheduled_transfers()
        
    except Exception as e:
        logger.error(f"Error in worker job: {str(e)}", exc_info=True)

if __name__ == "__main__":
    logger.info("Starting worker process")
    while True:
        try:
            run_job()
        except Exception as e:
            logger.error(f"Worker loop error: {str(e)}", exc_info=True)
        finally:
            time.sleep(60)  # every 60 seconds
