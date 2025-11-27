import sqlite3
from datetime import datetime

idempotency_store = {}


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def _map_row_to_product_dict(row):
    if row is None: return None
    return {
        "id": row["id"],
        "name": row["name"],
        "description": row["description"],
        "price": row["price"],
        "category": row["category"],  # Читаємо категорію
        "image_url": row["image_url"],  # Читаємо картинку
        "createdAt": row["createdAt"],
        "updatedAt": row["updatedAt"]
    }


def get_all_products():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return [_map_row_to_product_dict(row) for row in rows]


def get_product_by_id(product_id):
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    conn.close()
    if row is None:
        return {"error": "NotFound", "details": f"Product {product_id} not found"}, 404
    return _map_row_to_product_dict(row), 200


def create_product(product_data, idempotency_key=None):
    if idempotency_key and idempotency_key in idempotency_store:
        return idempotency_store[idempotency_key], 201

    name = product_data.get('name')
    price = product_data.get('price')
    category = product_data.get('category', 'general')

    if not name or not price:
        return {"error": "ValidationError", "details": "name and price required"}, 400

    description = product_data.get('description', '')
    image_url = product_data.get('image_url', 'https://via.placeholder.com/400x300')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        now = datetime.utcnow().isoformat()

        sql = """
        INSERT INTO products (name, description, price, category, image_url, createdAt, updatedAt) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """

        cursor.execute(sql, (name, description, price, category, image_url, now, now))
        new_id = cursor.lastrowid
        conn.commit()

        new_row = conn.execute("SELECT * FROM products WHERE id = ?", (new_id,)).fetchone()
        conn.close()

        result = _map_row_to_product_dict(new_row)

        if idempotency_key:
            idempotency_store[idempotency_key] = result

        return result, 201

    except Exception as e:
        return {"error": "DatabaseError", "details": str(e)}, 500


def update_product(product_id, product_data):
    name = product_data.get('name')
    price = product_data.get('price')

    if not name or not price: return {"error": "Error", "details": "Invalid data"}, 400

    try:
        conn = get_db_connection()
        conn.execute("UPDATE products SET name=?, price=?, updatedAt=? WHERE id=?",
                     (name, price, datetime.utcnow().isoformat(), product_id))
        conn.commit()
        row = conn.execute("SELECT * FROM products WHERE id=?", (product_id,)).fetchone()
        conn.close()
        if not row: return {"error": "NotFound"}, 404
        return _map_row_to_product_dict(row), 200
    except Exception as e:
        return {"error": "Error"}, 500


def delete_product(product_id):
    try:
        conn = get_db_connection()
        existing = conn.execute("SELECT id FROM products WHERE id=?", (product_id,)).fetchone()
        if not existing:
            conn.close()
            return {"error": "NotFound"}, 404
        conn.execute("DELETE FROM products WHERE id=?", (product_id,))
        conn.commit()
        conn.close()
        return "", 204
    except Exception as e:
        return {"error": "Error"}, 500