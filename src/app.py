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
                password TEXT,
                id_code TEXT UNIQUE
            )
        ''')
        conn.commit()

init_db()

# Version 1: Username and Password
@app.route('/login', methods=['POST'])
def login_v1():
    username = request.json.get('username')
    password = request.json.get('password')
    
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        user = cursor.fetchone()
        
    if user:
        return jsonify({'success': True, 'message': 'Login successful!'})
    return jsonify({'success': False, 'message': 'Invalid credentials.'})

@app.route('/signup', methods=['POST'])
def signup_v1():
    username = request.json.get('username')
    password = request.json.get('password')
    
    try:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
        return jsonify({'success': True, 'message': 'Signup successful!'})
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'message': 'Username already exists.'})

# Version 2: ID Code
@app.route('/login/idcode', methods=['POST'])
def login_v2():
    id_code = request.json.get('idcode')
    
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id_code=?', (id_code,))
        user = cursor.fetchone()
        
    if user:
        return jsonify({'success': True, 'message': 'Login successful!'})
    return jsonify({'success': False, 'message': 'Invalid ID code.'})

@app.route('/signup/idcode', methods=['POST'])
def signup_v2():
    id_code = request.json.get('idcode')
    username = request.json.get('username')
    
    try:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, id_code) VALUES (?, ?)', (username, id_code))
            conn.commit()
        return jsonify({'success': True, 'message': 'Signup successful!'})
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'message': 'ID code or username already exists.'})

if __name__ == '__main__':
    app.run(debug=True, port=6969, host="0.0.0.0")
