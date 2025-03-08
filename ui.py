# Streamlit UI
import streamlit as st
import sqlite3

# DB connection
def get_db_connection():
    conn = sqlite3.connect("links.db")
    conn.row_factory = sqlite3.Row
    return conn

# Fetch categories
def get_categories():
    conn = get_db_connection()
    categories = conn.execute("SELECT DISTINCT category FROM links").fetchall()
    conn.close()
    return ["All"] + [c["category"] for c in categories if c["category"]]

# Fetch links by category
def get_links(category=None):
    conn = get_db_connection()
    query = "SELECT * FROM links" if category == "All" else "SELECT * FROM links WHERE category = ?"
    links = conn.execute(query, () if category == "All" else (category,)).fetchall()
    conn.close()
    return links

st.set_page_config(page_title="LinkZen", layout="wide")
st.title("🔗 LinkZen - Organized Bookmarks")

categories = get_categories()
selected_category = st.sidebar.selectbox("Select Category", categories)

data = get_links(selected_category)

if data:
    for link in data:
        with st.expander(f"{link['category']} → {link['subcategory']}"):
            st.markdown(f"**🔗 [Visit]({link['url']})**")
else:
    st.write("No links found.")
