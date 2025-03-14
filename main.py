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
        """
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            category TEXT,
            subcategory TEXT,
            favorite INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
    conn.commit()
    conn.close()

def sync_categorize_link(url: str) -> tuple:
    """Blocking call to Gemini for super refined categorization."""
    prompt = f"""
    Classify this link into:
    1. A broad category (News, Technology, Entertainment, Education, Self Help, Health & Nutrition, etc.).
    2. A refined subcategory that describes the link in more detail (for example, if Self Help, is it about Procrastination, Looksmaxing, or Book Recommendations?)

    Link: {url}

    Return the result as:
    Broad Category: <broad_category>
    Subcategory: <subcategory>
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt]
    )

    response_text = response.text.strip()

    # Parse the response into category and subcategory
    broad_category = "Unknown"
    subcategory = "Unknown"

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

    # Fetch broad and subcategory
    category, subcategory = await categorize_link(url)

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO links (url, category, subcategory) VALUES (?, ?, ?)", (url, category, subcategory))
    conn.commit()
    conn.close()

    await update.message.reply_text(f"Link saved under category: {category} -> {subcategory}")

async def list_links(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lists stored links"""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT url, category, subcategory FROM links")
    rows = cursor.fetchall()
    conn.close()

    message = "\n".join([f"[{cat} -> {subcat}] {url}" for url, cat, subcat in rows]) or "No links stored yet."
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
