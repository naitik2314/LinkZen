import sqlite3

DB_FILE = "links.db"

def get_links():
    """Fetch categorized links from the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT category, subcategory, url FROM links ORDER BY category")
    rows = cursor.fetchall()
    conn.close()

    categories = {}
    for category, subcategory, url in rows:
        if category not in categories:
            categories[category] = {}
        if subcategory not in categories[category]:
            categories[category][subcategory] = []
        categories[category][subcategory].append(url)

    return categories

def add_link(url, category, subcategory):
    """Add a new link to the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO links (url, category, subcategory) VALUES (?, ?, ?)", (url, category, subcategory))
    conn.commit()
    conn.close()
