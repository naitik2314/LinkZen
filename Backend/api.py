import sqlite3
import os
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

db_file = "links.db"
app = FastAPI(title="Link API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/links")
async def get_links():
    loop = asyncio.get_running_loop()
    def fetch_links():
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT id, url, category, subcategory, favorite, created_at, short_description, description FROM links")
        rows = cursor.fetchall()
        conn.close()
        return rows
    try:
        rows = await loop.run_in_executor(None, fetch_links)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Map rows to list of dictionaries
    links = []
    for row in rows:
        links.append({
            "id": row[0],
            "url": row[1],
            "category": row[2],
            "subcategory": row[3],
            "isFavorite": bool(row[4]),
            "createdAt": row[5],
            "short_description": row[6],
            "description": row[7]
        })
    return links

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)