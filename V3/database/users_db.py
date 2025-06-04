import sqlite3
import hashlib
import os

DB_PATH = "database/users.db"

def init_users_db():
    """Initialize users database with default users"""
    os.makedirs("database", exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Default users
    default_users = [
        ("admin", "admin@company.com", "admin123", "DBAM"),
        ("itadmin", "itadmin@company.com", "itpass123", "DBAIT"),
        ("hradmin", "hradmin@company.com", "hrpass123", "DBAHR"),
        ("ituser", "ituser@company.com", "ituser123", "DBUIT"),
        ("hruser", "hruser@company.com", "hruser123", "DBUHR"),
    ]
    
    for username, email, password, role in default_users:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute('''
            INSERT OR IGNORE INTO users (username, email, password, role)
            VALUES (?, ?, ?, ?)
        ''', (username, email, hashed_password, role))
    
    conn.commit()
    conn.close()

def authenticate_user(username, password):
    """Authenticate user credentials"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    cursor.execute('''
        SELECT role FROM users WHERE username = ? AND password = ?
    ''', (username, hashed_password))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return True, result[0]
    return False, None

# Initialize database on import
init_users_db()
