import os
from flask import Flask, render_template
from flask_cors import CORS
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

app = Flask(__name__)
CORS(app)

@app.route('/')
def get_items():
    items = []
    connection = None  # <-- додаємо це
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id, name FROM items")
        items = cursor.fetchall()
    except mysql.connector.Error:
        return "Помилка сервера при отриманні даних", 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
    return render_template('items.html', items=items)


if __name__ == '__main__':
    app.run(debug=True)
