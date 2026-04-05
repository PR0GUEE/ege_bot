# Заглушка для работы с БД
# Реальные функции будут реализованы позже

def get_user(user_id):
    # Возвращает словарь с данными пользователя
    return {
        'blacklist': [],
        'current_task_id': None
    }

def update_user_current_task(user_id, task_id):
    # Сохраняет id текущей задачи пользователя
    pass

def clear_user_current_task(user_id):
    # Очищает текущую задачу пользователя
    pass

def get_task_by_num(num):
    # Возвращает задачу по номеру
    # Временная заглушка
    tasks = {
        1: {'id': 1, 'num': 1, 'condition': 'Пример условия задачи 1', 'answer': 'ответ1'},
        2: {'id': 2, 'num': 2, 'condition': 'Пример условия задачи 2', 'answer': 'ответ2'},
    }
    return tasks.get(num)

def get_task_by_id(task_id):
    # Возвращает задачу по id
    return get_task_by_num(task_id)  # Временно

def add_task_to_blacklist(user_id, task_id):
    # Добавляет задачу в черный список пользователя
    pass

def clear_blacklist(user_id):
    # Очищает черный список пользователя
    pass

def update_task_rating(task_id, new_rating):
    import sqlite3
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