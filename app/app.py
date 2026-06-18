from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB = "users.db"

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    conn.execute("INSERT OR IGNORE INTO users (id, username, password) VALUES (1, 'admin', 'admin123')")
    conn.commit()
    conn.close()

@app.route("/login", methods=["GET"])
def login():
    username = request.args.get("username", "")
    password = request.args.get("password", "")
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    # CORREGIDO: consulta parametrizada, previene SQL Injection
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    conn.close()
    if user:
        return jsonify({"status": "ok", "message": f"Bienvenido {username}"}), 200
    return jsonify({"status": "error", "message": "Credenciales inválidas"}), 401

@app.route("/health")
def health():
    return jsonify({"status": "up"}), 200

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
