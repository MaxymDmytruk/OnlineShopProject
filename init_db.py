import sqlite3
from flask import Flask
from flask_bcrypt import Bcrypt

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS orders")
cursor.execute("DROP TABLE IF EXISTS products")
cursor.execute("DROP TABLE IF EXISTS users")

cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'buyer',
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('''
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    category TEXT NOT NULL, 
    image_url TEXT,         
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('''
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    product_name TEXT NOT NULL,
    price REAL NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (product_id) REFERENCES products (id)
)
''')

products = [
    ("Python Mastery", "Complete guide to Python programming.", 29.99, "ebooks", "https://picsum.photos/id/24/400/300"),
    ("Clean Code Guide", "How to write better code instantly.", 19.99, "ebooks", "https://picsum.photos/id/3/400/300"),
    ("Startup Secrets", "From zero to hero in business.", 14.99, "ebooks", "https://picsum.photos/id/20/400/300"),
    ("Website Template Pro", "Responsive HTML/CSS template.", 49.99, "software", "https://picsum.photos/id/60/400/300"),
    ("SEO Analyzer Tool", "Check your website ranking.", 99.00, "software", "https://picsum.photos/id/119/400/300"),
    ("Mobile App UI Kit", "Figma kit for mobile apps.", 35.00, "software", "https://picsum.photos/id/48/400/300"),
    ("Abstract 4K Pack", "10 high-quality abstract wallpapers.", 5.00, "art", "https://picsum.photos/id/54/400/300"),
    ("Nature Icons Set", "Vector icons for your projects.", 12.50, "art", "https://picsum.photos/id/28/400/300"),
    ("Space Texture", "High resolution space background.", 8.00, "art", "https://picsum.photos/id/74/400/300")
]

cursor.executemany(
    "INSERT INTO products (name, description, price, category, image_url) VALUES (?, ?, ?, ?, ?)",
    products
)


fake_app = Flask(__name__)
bcrypt = Bcrypt(fake_app)


password_hash = bcrypt.generate_password_hash("admin123").decode('utf-8')

cursor.execute(
    "INSERT INTO users (email, password_hash, role) VALUES (?, ?, ?)",
    ("admin@shop.com", password_hash, "admin")
)
print("Auto-Admin created: admin@shop.com / admin123")


connection.commit()
connection.close()
print("Database initialized successfully!")