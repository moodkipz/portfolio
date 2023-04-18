import time
import os
import schedule
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
scriptPath = os.getenv("PATH-TO-SCRIPT")

def run_script():
    os.system(scriptPath)

# Define scheduled times
scheduled_times = ["12:00", "15:00", "17:00", "18:00", "19:00"]

# Schedule the script to run at the specified times
for times in scheduled_times:
    schedule.every().day.at(times).do(run_script)

while True:
    schedule.run_pending()
    time.sleep(10)