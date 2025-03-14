import os
import sys
import asyncio
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # <-- Import CORS middleware

# Gemini client (from google.genai)
from google import genai

load_dotenv()

# Environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if GEMINI_API_KEY is None:
    print("Gemini API key not found, please refer to the GitHub repo documentation to set up your .env correctly!")
    sys.exit(1)
elif TELEGRAM_BOT_TOKEN is None:
    print("Telegram API key not found, please refer to the GitHub repo documentation to set up your .env correctly!")
    sys.exit(1)

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

# SQLite database file
db_file = "links.db"

def init_db():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            category TEXT,
            subcategory TEXT
        )
        '''
    )
    conn.commit()
    conn.close()

def sync_categorize_link(url: str) -> tuple:
    """
    Blocking call to Gemini for categorization.
    Returns a tuple: (broad_category, subcategory)
    """
    prompt = f"""
    Classify this link into:
    1. A broad category (News, Technology, Entertainment, Education, Self Help, Health & Nutrition, etc.).
    2. A refined subcategory that describes the link in more detail.

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
    broad_category = "Unknown"
    subcategory = "Unknown"
    for line in response_text.split("\n"):
        if "Broad Category:" in line:
            broad_category = line.replace("Broad Category:", "").strip()
        elif "Subcategory:" in line:
            subcategory = line.replace("Subcategory:", "").strip()
    return broad_category, subcategory

async def categorize_link(url: str) -> tuple:
    """Async wrapper to run the synchronous Gemini categorization in a thread pool."""
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        return await loop.run_in_executor(pool, sync_categorize_link, url)

# ----------------------------
# Telegram Bot Handlers
# ----------------------------
async def add_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = update.message.text.strip()
    category, subcategory = await categorize_link(url)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO links (url, category, subcategory) VALUES (?, ?, ?)", (url, category, subcategory))
    conn.commit()
    conn.close()
    await update.message.reply_text(f"Link saved under category: {category} -> {subcategory}")

async def list_links(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT url, category, subcategory FROM links")
    rows = cursor.fetchall()
    conn.close()
    message = "\n".join([f"[{cat} -> {subcat}] {url}" for url, cat, subcat in rows]) or "No links stored yet."
    await update.message.reply_text(message)

async def run_telegram_bot():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, add_link))
    application.add_handler(CommandHandler("list", list_links))
    
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    # Keep the bot running indefinitely
    await asyncio.Future()  # Wait forever

# ----------------------------
# FastAPI REST API with Lifespan Events and CORS
# ----------------------------
async def lifespan(app: FastAPI):
    init_db()  # Initialize database on startup
    yield
    # Add any shutdown or cleanup code if necessary

api_app = FastAPI(lifespan=lifespan)

# Add CORS middleware to allow requests from your front end
api_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development purposes; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@api_app.get("/links")
async def get_links():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT url, category, subcategory FROM links")
    rows = cursor.fetchall()
    conn.close()
    return [
        {"url": url, "category": category, "subcategory": subcategory}
        for url, category, subcategory in rows
    ]

@api_app.post("/links")
async def create_link(link: dict):
    url = link.get("url")
    if not url:
        raise HTTPException(status_code=400, detail="Missing link URL")
    category, subcategory = await categorize_link(url)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO links (url, category, subcategory) VALUES (?, ?, ?)", (url, category, subcategory))
    conn.commit()
    conn.close()
    return {"message": "Link saved", "category": category, "subcategory": subcategory}

async def start_api():
    config = uvicorn.Config(api_app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

# ----------------------------
# Main Entry Point: Run Both Concurrently
# ----------------------------
async def main():
    init_db()  # Ensure database is initialized before starting tasks
    await asyncio.gather(
        run_telegram_bot(),
        start_api()
    )

if __name__ == "__main__":
    asyncio.run(main())
