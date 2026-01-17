from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)  # allow all origins

# ---------------- Database ----------------


def get_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        port=8889,
        user="root",
        password="root",
        database="spotify_churn"
    )

# ---------------- Register ----------------


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data["username"]
    password = generate_password_hash(data["password"])
    subscription_type = data.get("subscription_type", "Free")
    age = data.get("age", 20)
    country = data.get("country", "India")

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("""
            INSERT INTO users 
            (username,password,subscription_type,age,country,
             avg_listening_hours_per_week,login_frequency_per_week,
             songs_skipped_per_week,playlists_created,days_since_last_login,churn)
            VALUES (%s,%s,%s,%s,%s,0,0,0,0,0,0)
        """, (username, password, subscription_type, age, country))
        db.commit()
    except mysql.connector.Error as e:
        db.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        cursor.close()
        db.close()

    role = "admin" if username.lower() == "admin" else "user"
    return jsonify({"success": True, "username": username, "role": role})

# ---------------- Login ----------------


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()
    cursor.close()
    db.close()

    if not user:
        return jsonify({"success": False, "message": "User not found"}), 400
    if not check_password_hash(user["password"], password):
        return jsonify({"success": False, "message": "Incorrect password"}), 400

    role = "admin" if username.lower() == "admin" else "user"
    return jsonify({"success": True, "username": username, "role": role, "user_id": user["user_id"]})

# ---------------- Update User Activity ----------------


@app.route("/update-user", methods=["POST", "OPTIONS"])
def update_user():
    if request.method == "OPTIONS":
        return jsonify({"success": True})
    data = request.get_json()
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        UPDATE users
        SET avg_listening_hours_per_week = avg_listening_hours_per_week + %s/60,
            login_frequency_per_week = login_frequency_per_week + 1,
            songs_skipped_per_week = songs_skipped_per_week + %s,
            playlists_created = playlists_created + %s,
            days_since_last_login = 0
        WHERE user_id=%s
    """, (data.get("minutes_listened", 0), data.get("songs_skipped", 0), data.get("playlists_created", 0), data["user_id"]))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"success": True})

# ---------------- Admin Stats ----------------


@app.route("/stats")
def stats():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    db.close()
    total_users = len(users)
    churn_rate = sum(u["churn"] for u in users) / \
        total_users if total_users > 0 else 0
    return jsonify({"total_users": total_users, "churn_rate": churn_rate})


@app.route("/chart-data")
def chart_data():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT subscription_type,churn FROM users")
    users = cursor.fetchall()
    cursor.close()
    db.close()
    chart = {"Free": 0, "Premium": 0}
    counts = {"Free": 0, "Premium": 0}
    for u in users:
        stype = u["subscription_type"].strip()
        chart[stype] += u["churn"]
        counts[stype] += 1
    for k in chart:
        chart[k] = chart[k]/counts[k] if counts[k] > 0 else 0
    return jsonify(chart)


if __name__ == "__main__":
    app.run(debug=True)
