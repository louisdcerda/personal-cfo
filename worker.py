import os, time, datetime as dt
from sqlalchemy.orm import Session
from backend.app import database, models  # container context includes repo root

def run_job():
    utc_now = dt.datetime.utcnow().isoformat()
    print(f"[{utc_now}] worker heartbeat")


if __name__ == "__main__":
    while True:
        run_job()
        time.sleep(60)   # every 60 s for demo
