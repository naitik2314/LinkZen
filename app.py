from flask import Flask, render_template, request, jsonify
from database import get_links, add_link

app = Flask(__name__)

@app.route('/')
def index():
    """Serve the main UI with categorized links."""
    categories = get_links()
    return render_template("index.html", categories=categories)

@app.route('/add_link', methods=['POST'])
def add_new_link():
    """Receive a new link via HTMX request and categorize it."""
    url = request.form.get('url')
    category = request.form.get('category')
    subcategory = request.form.get('subcategory')

    add_link(url, category, subcategory)

    return jsonify({"status": "success", "message": "Link added!"})

if __name__ == '__main__':
    app.run(debug=True)
