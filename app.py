import os
import time
import uuid
from flask import Flask, render_template, jsonify, request, g
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv

load_dotenv()

from api.product_routes import register_product_routes
from api.auth_routes import register_auth_routes
from api.order_routes import register_order_routes

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-please-change-in-prod')
bcrypt = Bcrypt(app)


rate_limit_store = {}
RATE_LIMIT_WINDOW = 10
MAX_REQUESTS = 8


@app.before_request
def before_request_func():

    request_id = request.headers.get('X-Request-Id')
    if not request_id:
        request_id = uuid.uuid4().hex
    g.request_id = request_id

    client_ip = request.remote_addr
    current_time = time.time()

    client_data = rate_limit_store.get(client_ip, {'count': 0, 'start_time': current_time})

    if current_time - client_data['start_time'] > RATE_LIMIT_WINDOW:
        client_data = {'count': 1, 'start_time': current_time}
    else:
        client_data['count'] += 1

    rate_limit_store[client_ip] = client_data

    if client_data['count'] > MAX_REQUESTS:
        retry_after = RATE_LIMIT_WINDOW - (current_time - client_data['start_time'])
        response = jsonify({
            "error": "Too Many Requests",
            "details": "Rate limit exceeded. Try again later.",
            "requestId": g.request_id
        })
        response.status_code = 429
        response.headers['Retry-After'] = int(retry_after)
        return response


@app.after_request
def after_request_func(response):
    if hasattr(g, 'request_id'):
        response.headers['X-Request-Id'] = g.request_id
    return response


@app.errorhandler(Exception)
def handle_exception(e):
    code = 500
    if hasattr(e, 'code'):
        code = e.code

    return jsonify({
        "error": "Internal Server Error" if code == 500 else str(e),
        "code": getattr(e, 'name', 'UnknownError'),
        "details": str(e),
        "requestId": getattr(g, 'request_id', 'unknown')
    }), code


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


register_product_routes(app)
register_auth_routes(app, bcrypt)
register_order_routes(app)


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)