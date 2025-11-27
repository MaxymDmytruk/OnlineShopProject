from flask import request, jsonify
import service.user_service as user_service


def register_auth_routes(app, bcrypt):
    @app.route('/register', methods=['POST'])
    def register():
        data = request.json
        result, status_code = user_service.register_user(data, bcrypt)
        return jsonify(result), status_code

    @app.route('/login', methods=['POST'])
    def login():
        data = request.json
        result, status_code = user_service.login_user(data, bcrypt, app.config)
        return jsonify(result), status_code

    print("Маршрути для /register та /login зареєстровано.")