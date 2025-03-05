from google import genai
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

client = genai.Client(api_key=GEMINI_API_KEY)

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

def categorize_link(url: str) -> str:
    """Uses Gemini 2.0 Flash API to categorize the link."""
    # Prompt to ask Gemini to categorize the link
    prompt = f"Categorize this link into a broad category like 'News', 'Technology', 'Entertainment', 'Education', 'E-commerce', etc.: {url}\nCategory:"
    # Generate the response from Gemini
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt]
    )
    # Extract the response text (simple, since response.text works directly in Gemini 2.0)
    return response.text.strip()

