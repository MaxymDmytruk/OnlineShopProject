import sqlite3
import jwt
from datetime import datetime, timedelta


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def register_user(user_data, bcrypt_app):
    email = user_data.get('email')
    password = user_data.get('password')

    if not email or not password:
        return {"error": "ValidationError", "details": "email and password are required"}, 400

    conn = get_db_connection()
    existing_user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    if existing_user:
        conn.close()
        return {"error": "Conflict", "details": "Email already exists"}, 409  # 409 Conflict


    user_count = conn.execute("SELECT COUNT(id) as count FROM users").fetchone()
    role = 'admin' if user_count['count'] == 0 else 'buyer'

    password_hash = bcrypt_app.generate_password_hash(password).decode('utf-8')

    try:
        sql = "INSERT INTO users (email, password_hash, role) VALUES (?, ?, ?)"
        conn.execute(sql, (email, password_hash, role))
        conn.commit()
        conn.close()
        return {"message": f"User {email} registered successfully (Role: {role})"}, 201  # 201 Created

    except Exception as e:
        conn.close()
        return {"error": "DatabaseError", "details": str(e)}, 500



def login_user(login_data, bcrypt_app, app_config):
    email = login_data.get('email')
    password = login_data.get('password')

    if not email or not password:
        return {"error": "ValidationError", "details": "email and password are required"}, 400

    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()

    if not user:
        return {"error": "Unauthorized", "details": "Invalid credentials"}, 401

    if bcrypt_app.check_password_hash(user['password_hash'], password):

        token_payload = {
            'user_id': user['id'],
            'email': user['email'],
            'role': user['role'],
            'exp': datetime.utcnow() + timedelta(hours=24)
        }

        secret_key = app_config['SECRET_KEY']
        token = jwt.encode(token_payload, secret_key, algorithm="HS256")
        return {"token": token}, 200

    else:
        return {"error": "Unauthorized", "details": "Invalid credentials"}, 401

