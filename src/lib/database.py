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

def update_task_rating(task_id, rating):
    # Обновляет рейтинг задачи
    pass
