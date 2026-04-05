import sqlite3
import os

def init_users_db():
    conn = sqlite3.connect('data/users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            blacklist TEXT,
            current_task_id INTEGER,
            subscription_status INTEGER
        )
    ''')
    conn.commit()
    conn.close()
    print("users.db ready")

def init_tasks_db():
    conn = sqlite3.connect('data/tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            num INTEGER,
            condition TEXT,
            response_evaluation TEXT,
            user_id INTEGER,
            grade REAL DEFAULT 0,
            num_grades INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()
    print("tasks.db ready")

def init_query_db():
    conn = sqlite3.connect('data/query.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS moderation_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            num INTEGER,
            condition TEXT,
            response_evaluation TEXT,
            user_id INTEGER
        )
    ''')
    conn.commit()
    conn.close()
    print("query.db ready")

if __name__ == "__main__":
    # Убедись, что папка data существует
    os.makedirs('data', exist_ok=True)
    init_users_db()
    init_tasks_db()
    init_query_db()
    print("All databases initialized.")