#!/usr/bin/python3.10
import os
import csv
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import date
import time
import telegram
import asyncio
from collections import defaultdict

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
telegramToken = os.getenv("TELEGRAM-TOKEN")
telegramRecipient = os.getenv("RECIPIENT-ID")
folderPath = os.getenv("FOLDER-PATH")
loginURL = os.getenv("LOGIN-URL")
targetSortURL = os.getenv("TARGET-SORT-URL")

# Open Chrome
driver = webdriver.Chrome()

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

# Go to the login page
driver.get(loginURL)
driver.implicitly_wait(10.0)
time.sleep(10)

# Find the username and password fields
email_field = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Email"].form-control')
password_field = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Password"].form-control')

# Enter login credentials
email_field.send_keys(email)
driver.implicitly_wait(5.0)
password_field.send_keys(password)
driver.implicitly_wait(5.0)

# Submit the form
password_field.send_keys(Keys.RETURN)
time.sleep(10)

# Store today's date formatted in a variable
today = date.today()
formatted_date = today.strftime("%Y-%m-%d")

# Sort Orders page by today's date
driver.get(targetSortURL+formatted_date+'T00:00:00%22%7D,%22____timestamp%22:%222023311143230%22%7D')

# Download Orders CSV for today's date
CSV_element = driver.find_element(By.CLASS_NAME, "export-to-csv")
driver.implicitly_wait(5.0)
CSV_element.click()

time.sleep(10)

# Finds most recent file in Downloads Directory
todays_CSV = max([os.path.join(folderPath, f) for f in os.listdir(folderPath)], key=os.path.getctime)

# Parsing CSV
with open(todays_CSV, 'r') as file:
    reader = csv.reader(file)

    # Skip header
    next(reader)

    # Count the number of samples for each pharmacy
    counts = defaultdict(int)
    for row in reader:
        if row[1] is not None:
            counts[row[1]] += 1

    # Create message string
    message_string = ""
    for pharmacy, count in counts.items():
        if count == 1:
            message_string += f"{pharmacy} {row[8]},\n"
        else:
            message_string += f"{pharmacy} ({count} samples) ,\n"

    # Add message if pharmacies have no samples
    if not message_string:
        message_string = "No samples yet for today"

# Initialize telegram credentials
bot = telegram.Bot(token = telegramToken)

# It breaks if you don't use async so don't remove it
async def send_telegram_message(bot, telegramRecipient, message_string):
    await bot.send_message(chat_id=telegramRecipient, text=message_string)
asyncio.run(send_telegram_message(bot, telegramRecipient, message_string))

time.sleep(30)

driver.quit()