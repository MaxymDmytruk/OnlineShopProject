from flask import request, jsonify
import sqlite3
from api.auth_middleware import login_required


def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def register_order_routes(app):
    @app.route('/orders', methods=['POST'])
    @login_required
    def create_order(current_user):
        data = request.json
        product_id = data.get('product_id')

        conn = get_db()
        product = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()

        if not product:
            conn.close()
            return jsonify({"error": "Not Found"}), 404

        try:
            conn.execute(
                "INSERT INTO orders (user_id, product_id, product_name, price) VALUES (?, ?, ?, ?)",
                (current_user['user_id'], product['id'], product['name'], product['price'])
            )
            conn.commit()
            conn.close()
            return jsonify({"message": f"Successfully bought {product['name']}"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @app.route('/orders', methods=['GET'])
    @login_required
    def get_my_orders(current_user):
        conn = get_db()
        rows = conn.execute(
            "SELECT * FROM orders WHERE user_id = ? ORDER BY order_date DESC",
            (current_user['user_id'],)
        ).fetchall()
        conn.close()

        orders = [dict(row) for row in rows]
        return jsonify(orders), 200