from google import genai
import sqlite3
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv
import sys
import asyncio
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if GEMINI_API_KEY is None:
    print("Gemini API key not found, please refer to the GitHub repo documentation to set up your .env correctly!")
    sys.exit(1)
elif TELEGRAM_BOT_TOKEN is None:
    print("Telegram API key not found, please refer to the GitHub repo documentation to set up your .env correctly!")
    sys.exit(1)

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

def sync_categorize_link(url: str) -> str:
    """This is the sync function that calls Gemini API (blocking)."""
    prompt = f"Categorize this link into a broad category like 'News', 'Technology', 'Entertainment', 'Education', 'E-commerce', etc.: {url}\nCategory:"
    
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt]
    )
    return response.text.strip()

async def categorize_link(url: str) -> str:
    """Async wrapper around sync Gemini call - future proof for async Telegram bot."""
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        return await loop.run_in_executor(pool, sync_categorize_link, url)

async def add_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles incoming links"""
    url = update.message.text.strip()

    # Get category using async Gemini wrapper
    category = await categorize_link(url)

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO links (url, category) VALUES (?, ?)", (url, category))
    conn.commit()
    conn.close()

    await update.message.reply_text(f"Link saved under category: {category}")

async def list_links(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lists stored links"""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT url, category FROM links")
    rows = cursor.fetchall()
    conn.close()

    message = "\n".join([f"[{cat}] {url}" for url, cat in rows]) or "No links stored yet."
    await update.message.reply_text(message)

def main():
    """Main function to start the bot"""
    init_db()

    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, add_link))
    application.add_handler(CommandHandler("list", list_links))

    application.run_polling()

if __name__ == "__main__":
    main()
