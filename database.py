import sqlite3
from passlib.hash import bcrypt

def add_user(username, password, role):
    try:
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT, role TEXT)''')
            hashed = bcrypt.hash(password)
            cursor.execute("INSERT OR REPLACE INTO users VALUES (?, ?, ?)", (username, hashed, role))
            conn.commit()
        return True
    except Exception as e:
        print(f"Error adding user: {e}")
        return False

def authenticate(username, password):
    try:
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT password, role FROM users WHERE username=?", (username,))
            result = cursor.fetchone()
            if result and bcrypt.verify(password, result[0]):
                return result[1]
            return None
    except Exception as e:
        print(f"Authentication error: {e}")
        return None

# Добавьте дефолтных пользователей при первом запуске
if not add_user("admin", "admin123", "admin"):
    print("Failed to add default admin")
if not add_user("support1", "pass1", "support1"):
    print("Failed to add default support1")
if not add_user("support2", "pass2", "support2"):
    print("Failed to add default support2")
if not add_user("support3", "pass3", "support3"):
    print("Failed to add default support3")