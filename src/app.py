#copyright jensen https://github.com/Jensenleung2465/tcsauth app.py
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT NOT NULL,
                id_code TEXT UNIQUE
            )
        ''')
        conn.commit()

init_db()

# Version 1: Username and Password
@app.route('/login', methods=['GET'])
def login_v1():
    username = request.args.get('username')  # Use request.args for GET
    password = request.args.get('password')
    
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        user = cursor.fetchone()
        
    return "true" if user else "false"

@app.route('/signup', methods=['GET'])
def signup_v1():
    username = request.args.get('username')  # Use request.args for GET
    password = request.args.get('password')
    
    if username is None or password is None:
        return "false"

    try:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
        return "true"
    except sqlite3.IntegrityError:
        return "false"

# Version 2: ID Code (using GET)
@app.route('/login/idcode', methods=['GET'])
def login_v2():
    id_code = request.args.get('idcode')  # Use request.args for GET
    
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id_code=?', (id_code,))
        user = cursor.fetchone()
        
    return "true" if user else "false"

@app.route('/signup/idcode', methods=['GET'])
def signup_v2():
    id_code = request.args.get('idcode')  # Use request.args for GET
    username = request.args.get('username')
    
    if username is None or id_code is None:
        return "false"

    try:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, id_code) VALUES (?, ?)', (username, id_code))
            conn.commit()
        return "true"
    except sqlite3.IntegrityError:
        return "false"

if __name__ == '__main__':
    app.run(debug=True, port=6969, host="0.0.0.0")
