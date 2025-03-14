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
from fastapi.middleware.cors import CORSMiddleware

# Gemini client (from google.genai)
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if GEMINI_API_KEY is None:
    print("Gemini API key not found, please set up your .env correctly!")
    sys.exit(1)
elif TELEGRAM_BOT_TOKEN is None:
    print("Telegram API key not found, please set up your .env correctly!")
    sys.exit(1)

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

db_file = "links.db"

# ---------------------------
# Database Initialization
# ---------------------------
def init_db():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    # Add 'favorite' and 'created_at' columns for dynamic features
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
        """
    )
    conn.commit()
    conn.close()

# ---------------------------
# Categorization (Gemini)
# ---------------------------
def sync_categorize_link(url: str) -> tuple:
    """
    Blocking call to Gemini for categorization.
    Returns (broad_category, subcategory).
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
    text = response.text.strip()

    broad_category = "Unknown"
    subcategory = "Unknown"
    for line in text.split("\n"):
        if "Broad Category:" in line:
            broad_category = line.replace("Broad Category:", "").strip()
        elif "Subcategory:" in line:
            subcategory = line.replace("Subcategory:", "").strip()
    return broad_category, subcategory

async def categorize_link(url: str) -> tuple:
    """Async wrapper to run sync categorization in a thread pool."""
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        return await loop.run_in_executor(pool, sync_categorize_link, url)

# ---------------------------
# Telegram Bot Handlers
# ---------------------------
async def add_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles incoming links from Telegram.
    Categorizes the link, saves it, and replies with the category.
    """
    url = update.message.text.strip()
    category, subcategory = await categorize_link(url)

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO links (url, category, subcategory) VALUES (?, ?, ?)",
        (url, category, subcategory)
    )
    conn.commit()
    conn.close()

    await update.message.reply_text(
        f"Link saved under category: {category} -> {subcategory}"
    )

async def list_links(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lists all links stored in the database for Telegram users."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT url, category, subcategory FROM links")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        await update.message.reply_text("No links stored yet.")
        return

    message = "\n".join(
        [f"[{cat} -> {subcat}] {url}" for url, cat, subcat in rows]
    )
    await update.message.reply_text(message)

async def run_telegram_bot():
    """
    Builds and starts the Telegram bot.
    Runs indefinitely via an infinite Future.
    """
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, add_link))
    application.add_handler(CommandHandler("list", list_links))

    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    # Keep the bot running
    await asyncio.Future()  # Wait forever

# ---------------------------
# FastAPI Setup & Endpoints
# ---------------------------
async def lifespan(app: FastAPI):
    init_db()  # Initialize database on startup
    yield
    # Cleanup code on shutdown if needed

api_app = FastAPI(lifespan=lifespan)

# Add CORS middleware to allow front-end requests
api_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # In production, specify your front-end origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@api_app.get("/links")
async def get_links(sort: str = "recent"):
    """
    Fetch all links.
    Optional query param 'sort' can be 'recent', 'alphabetical', etc.
    """
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Default sort: by created_at descending (most recent first)
    if sort == "recent":
        cursor.execute("SELECT id, url, category, subcategory, favorite, created_at FROM links ORDER BY created_at DESC")
    elif sort == "alphabetical":
        cursor.execute("SELECT id, url, category, subcategory, favorite, created_at FROM links ORDER BY url ASC")
    else:
        cursor.execute("SELECT id, url, category, subcategory, favorite, created_at FROM links")

    rows = cursor.fetchall()
    conn.close()

    results = []
    for row in rows:
        link_id, url, category, subcategory, favorite, created_at = row
        results.append({
            "id": link_id,
            "url": url,
            "category": category,
            "subcategory": subcategory,
            "favorite": bool(favorite),
            "created_at": created_at
        })
    return results

@api_app.post("/links")
async def create_link(payload: dict):
    """
    Add a new link.
    Body must contain {"url": "..."}.
    """
    url = payload.get("url")
    if not url:
        raise HTTPException(status_code=400, detail="Missing link URL")

    # Categorize
    category, subcategory = await categorize_link(url)

    # Insert
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO links (url, category, subcategory)
        VALUES (?, ?, ?)
        """,
        (url, category, subcategory)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return {"message": "Link saved", "id": new_id, "category": category, "subcategory": subcategory}

@api_app.patch("/links/{link_id}/favorite")
async def toggle_favorite(link_id: int):
    """
    Toggle the 'favorite' status of a link.
    Returns the new favorite value.
    """
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Check if link exists
    cursor.execute("SELECT favorite FROM links WHERE id = ?", (link_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Link not found")

    current_fav = row[0]
    new_fav = 0 if current_fav == 1 else 1  # Flip 0→1 or 1→0

    cursor.execute(
        "UPDATE links SET favorite = ? WHERE id = ?",
        (new_fav, link_id)
    )
    conn.commit()
    conn.close()

    return {"link_id": link_id, "favorite": bool(new_fav)}

async def start_api():
    """Start the FastAPI server using uvicorn."""
    config = uvicorn.Config(api_app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

# ---------------------------
# Main entry point
# ---------------------------
async def main():
    init_db()
    # Run both the Telegram bot and API concurrently
    await asyncio.gather(
        run_telegram_bot(),
        start_api()
    )

if __name__ == "__main__":
    asyncio.run(main())
