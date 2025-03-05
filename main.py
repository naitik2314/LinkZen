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

# Configuring the database (local)
db_file = "links.db"

def init_db():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(
        '''
            CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            category TEXT)
        ''')
    conn.commit()
    conn.close()