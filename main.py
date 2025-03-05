import google.generativeai as genai
import sqlite3
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
from dotenv import load_dotenv
import sys

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if GEMINI_API_KEY is None:
    print("Gemini API key not found, please refer to the GitHub repo documentation to set up your .env correctly!")
    sys.exit(1)
elif TELEGRAM_BOT_TOKEN is None:
    print("Telegram API key not found, please refer to the GitHub repo documentation to set up your .env correctly!")
    sys.exit(1)
else:
    None

# Configure the API key (this is correct for google-generativeai package)
genai.configure(api_key=GEMINI_API_KEY)

# Initialize model
model = genai.GenerativeModel("gemini-1.5-flash")

# Make a simple request
response = model.generate_content(["How does AI work?"])

# Output the response
print(response.text)