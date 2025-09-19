import mysql.connector
from flask import Flask, jsonify, request
from flask_cors import CORS

# Налаштування з'єднання з базою даних MySQL
# Заміни 'root' та 'password' на свої облікові дані
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'MaxKatya13',
    'database': 'online_shop'
}

# Ініціалізація додатку Flask
app = Flask(__name__)
# Дозволяє крос-доменні запити з клієнтського боку
CORS(app)


@app.route('/items', methods=['GET'])
def get_items():
    """
    Ендпоінт, який отримує список товарів з БД і повертає їх у форматі JSON.
    """
    items = []
    connection = None
    try:
        # Встановлюємо з'єднання з БД
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Виконуємо SQL-запит
        cursor.execute("SELECT id, name FROM items")

        # Отримуємо всі результати
        results = cursor.fetchall()

        # Перетворюємо результати в список словників
        for row in results:
            items.append({'id': row[0], 'name': row[1]})

    except mysql.connector.Error as err:
        return jsonify({"error": f"Error: {err}"}), 500
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

    # Повертаємо список товарів у форматі JSON
    return jsonify(items)


if __name__ == '__main__':
    # Запускаємо сервер в режимі відладки
    app.run(debug=True)