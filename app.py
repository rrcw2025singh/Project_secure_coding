import os
import sqlite3
from flask import Flask, request, jsonify
from urllib.request import urlopen

app = Flask(__name__)
DB_NAME = "users.db"

# Hardcoded secrets (for vulnerability)
API_KEY = "super-secret-key"
ADMIN_EMAIL = "admin@example.com"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            bio TEXT
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return jsonify({"message": "App running"})


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")
    bio = data.get("bio")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # SQL Injection vulnerability
    query = f"INSERT INTO users (username, password, bio) VALUES ('{username}', '{password}', '{bio}')"
    cursor.execute(query)

    conn.commit()
    conn.close()

    return jsonify({"message": "User created"})


@app.route("/user")
def get_user():
    username = request.args.get("username")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # SQL Injection vulnerability
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)

    data = cursor.fetchall()
    conn.close()

    return jsonify({"data": data})


@app.route("/fetch")
def fetch():
    url = request.args.get("url")

    # SSRF vulnerability
    response = urlopen(url)
    content = response.read().decode()

    return jsonify({"content": content})


@app.route("/run", methods=["POST"])
def run():
    data = request.get_json()
    command = data.get("command")

    # Command injection
    os.system(command)

    return jsonify({"message": "Executed"})


if __name__ == "__main__":
    init_db()
    app.run(debug=True)