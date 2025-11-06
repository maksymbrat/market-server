from flask import Flask, request, jsonify
import json, os

app = Flask(__name__)
DATA_FILE = "market_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"users": [], "listings": []}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

db = load_data()

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    if any(u["login"] == data["login"] for u in db["users"]):
        return jsonify({"error": "Користувач вже існує"}), 400
    db["users"].append(data)
    save_data(db)
    return jsonify({"status": "ok"})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    for u in db["users"]:
        if u["login"] == data["login"] and u["password"] == data["password"]:
            return jsonify({"status": "ok"})
    return jsonify({"error": "Невірний логін або пароль"}), 401

@app.route("/listings", methods=["GET", "POST"])
def listings():
    if request.method == "GET":
        return jsonify(db["listings"])
    data = request.json
    db["listings"].append(data)
    save_data(db)
    return jsonify({"status": "added"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
