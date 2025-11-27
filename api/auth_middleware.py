from functools import wraps
from flask import request, jsonify, current_app
import jwt


def get_token_data():
    if 'Authorization' not in request.headers:
        return None

    token = request.headers['Authorization'].split(" ")[1]
    try:
        return jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
    except:
        return None


def login_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        data = get_token_data()
        if not data:
            return jsonify({'error': 'Unauthorized', 'details': 'Login required'}), 401
        return f(current_user=data, *args, **kwargs)

    return decorated


def admin_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        data = get_token_data()
        if not data:
            return jsonify({'error': 'Unauthorized'}), 401
        if data.get('role') != 'admin':
            return jsonify({'error': 'Forbidden', 'details': 'Admin access required'}), 403
        return f(current_user=data, *args, **kwargs)

    return decorated