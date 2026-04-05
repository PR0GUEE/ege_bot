import time
import requests
from ..config import load_config

def check_task_with_deepseek(problem_text, criteria, user_answer, retries=3, delay=2):
    """
    Отправляет запрос к DeepSeek API с повторными попытками при ошибках.
    Возвращает словарь {'score': int, 'comment': str} или None при окончательной ошибке.
    """
    config = load_config()
    api_key = config['deepseek']['api_key']
    model = config['deepseek']['model']
    
    prompt = f"""Ты — эксперт ЕГЭ по обществознанию. Проверь решение задачи второй части.

Условие задачи:
{problem_text}

Критерии оценки (если есть):
{criteria if criteria else "Критерии не предоставлены, оцени по стандартным критериям ЕГЭ ."}

Ответ ученика:
{user_answer}

Требуется:
1. Выставить оценку (целое число баллов) согласно критериям.
2. Написать краткий комментарий (2-3 предложения) с объяснением, за что поставлены баллы.

Формат ответа (строго):
Оценка: <число>
Комментарий: <текст>
"""
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 500
    }
    
    url = "https://api.deepseek.com/v1/chat/completions"
    
    for attempt in range(retries):
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # Парсим ответ
            score_line = [line for line in content.split('\n') if line.startswith('Оценка:')]
            comment_line = [line for line in content.split('\n') if line.startswith('Комментарий:')]
            score = int(score_line[0].replace('Оценка:', '').strip()) if score_line else 0
            comment = comment_line[0].replace('Комментарий:', '').strip() if comment_line else "Нет комментария"
            return {"score": score, "comment": comment}
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(delay)
                continue
            else:
                # Последняя попытка провалилась
                return None
    return None