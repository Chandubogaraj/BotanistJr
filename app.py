import base64
import requests
import sqlite3
import os
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "super_secret_key"

# ---------------- SQLite Config ----------------
DATABASE = 'botanistjr.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# 🔑 Use environment variable instead of hardcoding
PLANTNET_API_KEY = os.getenv("PLANTNET_API_KEY")

# ---------------- Routes ----------------

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            conn.commit()
            conn.close()
            flash("Registration successful!")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Username already exists!")

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        conn.close()

        # ✅ Proper password validation
        if user and check_password_hash(user["password"], password):
            session['username'] = user["username"]
            return redirect(url_for('main'))
        else:
            flash("Invalid credentials!")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/main')
def main():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('main.html')

# ---------------- Plant Identification ----------------
@app.route('/predict', methods=['POST'])
def predict():
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    if not request.is_json:
        return jsonify(error='Invalid request format'), 400

    image_data = request.json.get('image')
    if not image_data:
        return jsonify(error='No image provided'), 400

    try:
        image_bytes = base64.b64decode(image_data.split(',', 1)[1])
    except Exception:
        return jsonify(error='Invalid image data'), 400

    files = {
        'images': ('plant.jpg', image_bytes, 'image/jpeg')
    }

    url = f"https://my-api.plantnet.org/v2/identify/all?api-key={PLANTNET_API_KEY}"

    try:
        response = requests.post(url, files=files, timeout=10)
        response.raise_for_status()
        result_json = response.json()
    except Exception as e:
        app.logger.error(f"PlantNet error: {e}")
        return jsonify(error='Identification service unavailable'), 503

    # ✅ Fixed logic here
    if "results" in result_json and len(result_json["results"]) > 0:
        best_match = result_json["results"][0]

        common_list = best_match["species"].get("commonNames", [])
        scientific_name = best_match["species"]["scientificNameWithoutAuthor"]

        if common_list:
            plant_name = common_list[0]
        else:
            plant_name = scientific_name

        confidence = best_match["score"] * 100

        return jsonify({
            "plant_name": plant_name,
            "common_names": common_list,
            "scientific_name": scientific_name,
            "confidence": round(confidence, 2)
        })

    return jsonify({
        "plant_name": "Not identified",
        "scientific_name": "Unknown",
        "confidence": 0
    })


if __name__ == '__main__':
    init_db()
    app.run(debug=True)