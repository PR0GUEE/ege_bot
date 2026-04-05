import sqlite3

def get_pending_task():
    conn = sqlite3.connect('data/query.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, num, condition, response_evaluation, user_id FROM moderation_tasks LIMIT 1')
    row = cursor.fetchone()
    conn.close()
    return row

def delete_task(task_id):
    conn = sqlite3.connect('data/query.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM moderation_tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    print(f"Задача {task_id} удалена.")

def accept_task(task):
    task_id, num, condition, response_eval, user_id = task
    # Переносим в tasks.db
    conn_tasks = sqlite3.connect('data/tasks.db')
    cursor_tasks = conn_tasks.cursor()
    cursor_tasks.execute('''
        INSERT INTO tasks (num, condition, response_evaluation, user_id, grade, num_grades)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (num, condition, response_eval, None, 0.0, 0))
    conn_tasks.commit()
    conn_tasks.close()
    # Удаляем из очереди
    delete_task(task_id)
    print(f"Задача {task_id} перенесена в tasks.db (общая).")

def main():
    print("=== Модератор задач ===")
    while True:
        task = get_pending_task()
        if not task:
            print("Нет задач на проверку.")
            break
        
        task_id, num, condition, response_eval, user_id = task
        print("\n" + "="*50)
        print(f"ID задачи: {task_id}")
        print(f"Номер в экзамене (num): {num}")
        print(f"Пользователь (user_id): {user_id}")
        print(f"Условие:\n{condition}")
        print(f"Ответ/Критерии:\n{response_eval}")
        print("-"*50)
        print("Команды: accept (принять), reject (отклонить), exit (выйти)")
        
        choice = input("> ").strip().lower()
        if choice == 'accept':
            accept_task(task)
        elif choice == 'reject':
            delete_task(task_id)
        elif choice == 'exit':
            print("Выход из модерации.")
            break
        else:
            print("Неизвестная команда. Попробуйте снова.")
            continue

if __name__ == "__main__":
    main()