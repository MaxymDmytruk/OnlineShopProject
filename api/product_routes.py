from flask import request, jsonify
import service.product_service as product_service
from api.auth_middleware import admin_required


def register_product_routes(app):
    @app.route('/products', methods=['GET'])
    def get_products():
        products = product_service.get_all_products()
        return jsonify(products), 200

    @app.route('/products/<int:id>', methods=['GET'])
    def get_product(id):
        result, status_code = product_service.get_product_by_id(id)
        return jsonify(result), status_code

    @app.route('/products', methods=['POST'])
    @admin_required
    def create_product(current_user):
        print(f"Admin '{current_user['email']}' creating product.")

        data = request.json
        if not data:
            return jsonify({"error": "Bad Request"}), 400

        idem_key = request.headers.get('Idempotency-Key')

        result, status_code = product_service.create_product(data, idempotency_key=idem_key)

        return jsonify(result), status_code

    @app.route('/products/<int:id>', methods=['PUT'])
    @admin_required
    def update_product(current_user, id):
        data = request.json
        result, status_code = product_service.update_product(id, data)
        return jsonify(result), status_code

    @app.route('/products/<int:id>', methods=['DELETE'])
    @admin_required
    def delete_product(current_user, id):
        result, status_code = product_service.delete_product(id)
        if status_code == 204:
            return "", 204
        return jsonify(result), status_code

    print("Маршрути CRUD зареєстровано.")