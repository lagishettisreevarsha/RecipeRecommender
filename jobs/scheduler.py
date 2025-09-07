import schedule
import time
import subprocess
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]


def job():
    # Run the pipeline
    subprocess.run(["py", "-m", "src.app", "--run-all"], check=False)

# Every day at 09:00
schedule.every().day.at("09:00").do(job)

print("Scheduler started. Press Ctrl+C to stop.")
while True:
    schedule.run_pending()
    time.sleep(1)
