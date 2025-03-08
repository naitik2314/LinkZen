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

if GEMINI_API_KEY is None or TELEGRAM_BOT_TOKEN is None:
    print("❌ API keys not found! Please set them in `.env`")
    sys.exit(1)

client = genai.Client(api_key=GEMINI_API_KEY)

DB_FILE = "links.db"

def init_db():
    """Initialize the SQLite database if not exists"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            category TEXT,
            subcategory TEXT
        )
        ''')
    conn.commit()
    conn.close()

def sync_categorize_link(url: str) -> tuple:
    """Blocking call to Gemini for refined categorization."""
    prompt = f"""
    Classify this link into:
    1. A broad category (News, Technology, Entertainment, Education, Self Help, etc.).
    2. A refined subcategory (like Looksmaxing, Procrastination, etc.).

    Link: {url}

    Return:
    Broad Category: <broad_category>
    Subcategory: <subcategory>
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt]
    )

    response_text = response.text.strip()
    broad_category, subcategory = "Unknown", "Unknown"

    for line in response_text.split("\n"):
        if "Broad Category:" in line:
            broad_category = line.replace("Broad Category:", "").strip()
        elif "Subcategory:" in line:
            subcategory = line.replace("Subcategory:", "").strip()

    return broad_category, subcategory

async def categorize_link(url: str) -> tuple:
    """Async wrapper to run sync Gemini categorization in thread pool."""
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        return await loop.run_in_executor(pool, sync_categorize_link, url)

async def add_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles incoming links"""
    url = update.message.text.strip()
    category, subcategory = await categorize_link(url)

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO links (url, category, subcategory) VALUES (?, ?, ?)", (url, category, subcategory))
    conn.commit()
    conn.close()

    await update.message.reply_text(f"✅ Link saved: {category} -> {subcategory}")

async def list_links(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lists stored links"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT url, category, subcategory FROM links")
    rows = cursor.fetchall()
    conn.close()

    message = "\n".join([f"[{cat} -> {subcat}] {url}" for url, cat, subcat in rows]) or "No links stored yet."
    await update.message.reply_text(message)

def main():
    """Start the bot"""
    init_db()

    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, add_link))
    application.add_handler(CommandHandler("list", list_links))

    print("🚀 Telegram Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
