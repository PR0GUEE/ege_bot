import sqlite3
import json
import random

def get_user(user_id):
    """
    Возвращает словарь с полями: blacklist (list), current_task_id (int or None), subscription_status (bool).
    Если subscription_status в БД NULL, возвращает True.
    """
    conn = sqlite3.connect('data/users.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT blacklist, current_task_id, subscription_status 
        FROM users WHERE user_id = ?
    ''', (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        blacklist = json.loads(row[0]) if row[0] else []
        current_task_id = row[1]
        sub_status = row[2] if row[2] is not None else True
        return {'blacklist': blacklist, 'current_task_id': current_task_id, 'subscription_status': sub_status}
    else:
        # Создаём нового пользователя
        conn = sqlite3.connect('data/users.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (user_id, blacklist, current_task_id, subscription_status)
            VALUES (?, ?, ?, ?)
        ''', (user_id, json.dumps([]), None, True))
        conn.commit()
        conn.close()
        return {'blacklist': [], 'current_task_id': None, 'subscription_status': True}

def update_user_current_task(user_id, task_id):
    conn = sqlite3.connect('data/users.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET current_task_id = ? WHERE user_id = ?', (task_id, user_id))
    conn.commit()
    conn.close()

def clear_user_current_task(user_id):
    conn = sqlite3.connect('data/users.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET current_task_id = NULL WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

def get_task_by_id(task_id):
    """Возвращает все поля задачи из tasks.db по её id."""
    conn = sqlite3.connect('data/tasks.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_task_to_solve(task_pool: list[int], banned: list[int]):
    """
    Выбирает случайную задачу, у которой num в task_pool и id не в banned.
    Возвращает словарь задачи или None.
    """
    conn = sqlite3.connect('data/tasks.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    # Формируем запрос: num в заданном списке, id не в banned
    placeholders_num = ','.join('?' for _ in task_pool)
    if banned:
        placeholders_banned = ','.join('?' for _ in banned)
        query = f'''
            SELECT * FROM tasks 
            WHERE num IN ({placeholders_num}) AND id NOT IN ({placeholders_banned})
        '''
        params = task_pool + banned
    else:
        query = f'''
            SELECT * FROM tasks 
            WHERE num IN ({placeholders_num})
        '''
        params = task_pool
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    if rows:
        chosen = random.choice(rows)
        return dict(chosen)
    return None

def add_task_to_blacklist(user_id, task_id):
    """Добавляет task_id в черный список пользователя (JSON)."""
    conn = sqlite3.connect('data/users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT blacklist FROM users WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    blacklist = json.loads(row[0]) if row and row[0] else []
    if task_id not in blacklist:
        blacklist.append(task_id)
        cursor.execute('UPDATE users SET blacklist = ? WHERE user_id = ?', (json.dumps(blacklist), user_id))
    conn.commit()
    conn.close()

def clear_blacklist(user_id):
    """Очищает черный список пользователя."""
    conn = sqlite3.connect('data/users.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET blacklist = ? WHERE user_id = ?', (json.dumps([]), user_id))
    conn.commit()
    conn.close()

def update_task_rating(task_id, new_rating):
    conn = sqlite3.connect('data/tasks.db')
    cursor = conn.cursor()
    
    # Получаем текущие значения grade и num_grades
    cursor.execute("SELECT grade, num_grades FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    if row:
        current_grade, current_num = row
        new_num = current_num + 1
        # Формула среднего: (grade * num_grades + new_rating) / (num_grades + 1)
        # Но если num_grades было 0, то new_grade = new_rating
        if current_num == 0:
            new_grade = new_rating
        else:
            new_grade = (current_grade * current_num + new_rating) / new_num
        cursor.execute("UPDATE tasks SET grade = ?, num_grades = ? WHERE id = ?", (new_grade, new_num, task_id))
    else:
        # Если задачи нет — создать запись (но обычно она есть)
        cursor.execute("INSERT INTO tasks (id, grade, num_grades) VALUES (?, ?, ?)", (task_id, new_rating, 1))
    conn.commit()
    conn.close()

def get_task_criteria(task_id):
    import sqlite3
    conn = sqlite3.connect('data/tasks.db')
    cursor = conn.cursor()
    cursor.execute("SELECT criteria FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None