from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from lib.database import get_user, update_user_current_task, clear_user_current_task, get_task_by_id, get_task_by_num, add_task_to_blacklist, clear_blacklist
from lib.keyboards import back_to_main_keyboard, main_menu_keyboard, tasks_menu_keyboard, back_to_tasks_menu_keyboard, solve_part_keyboard, solve_part2_keyboard, feedback_keyboard, rating_keyboard, add_to_blacklist_keyboard

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    
    if data == "info":
        await query.edit_message_text(
            "📖 *Информация о боте*\n\n"
            "Бот для подготовки к ЕГЭ по обществознанию.\n"
            "Версия: 1.0.0\n\n"
            "Здесь будут появляться задачи и тесты для подготовки.",
            parse_mode="Markdown",
            reply_markup=back_to_main_keyboard()
        )
    elif data == "tasks":
        await show_tasks_menu(query)
    elif data == "monetization":
        await query.edit_message_text(
            "💰 *Монетизация*\n\n"
            "Раздел в разработке.",
            parse_mode="Markdown",
            reply_markup=back_to_main_keyboard()
        )
    elif data == "add_task":
        await query.edit_message_text(
            "➕ *Добавление задачи*\n\n"
            "Раздел в разработке.",
            parse_mode="Markdown",
            reply_markup=back_to_main_keyboard()
        )
    elif data == "main_menu":
        await query.edit_message_text(
            "Добро пожаловать в бот для подготовки к ЕГЭ по обществознанию!\n\n"
            "Выберите действие:",
            reply_markup=main_menu_keyboard()
        )
    elif data == "back_to_tasks_menu":
        await show_tasks_menu(query)
    elif data == "solve_part1":
        await start_solve(update, context, part=1)
    elif data == "solve_part2":
        await start_solve(update, context, part=2)
    elif data == "solve_specific":
        context.user_data['awaiting_task_number'] = True
        await query.edit_message_text(
            "🔢 Введите номер задачи (от 1 до 25):\n\n"
            "Или нажмите кнопку ниже для возврата.",
            reply_markup=back_to_tasks_menu_keyboard()
        )
    elif data == "clear_blacklist":
        user_id = query.from_user.id
        clear_blacklist(user_id)
        await query.edit_message_text(
            "✅ Черный список задач очищен!",
            reply_markup=back_to_tasks_menu_keyboard()
        )
    elif data == "stop_solving":
        user_id = query.from_user.id
        clear_user_current_task(user_id)
        context.user_data.pop('current_task', None)
        context.user_data.pop('current_task_id', None)
        context.user_data.pop('solving_part', None)
        context.user_data.pop('collected_answer', None)
        await query.edit_message_text(
            "Вы вернулись в меню решения задач.",
            reply_markup=tasks_menu_keyboard()
        )
    elif data == "back_to_task":
        user_id = query.from_user.id
        user_data = get_user(user_id)
        current_task_id = user_data.get('current_task_id')
        if current_task_id:
            task = get_task_by_id(current_task_id)
            if task:
                context.user_data['current_task'] = task
                context.user_data['current_task_id'] = task['id']
                solving_part = context.user_data.get('solving_part', 1)
                message = f"*Задача №{task['num']}*\n\n{task['condition']}"
                if solving_part == 1 and task['num'] not in [6,13,15]:
                    message += "\n\n*Ответ:* набор вариантов — введите подряд без пробелов"
                elif solving_part == 1 and task['num'] in [6,13,15]:
                    message += "\n\n*Ответ:* соответствие — введите последовательность цифр без пробелов"
                else:  # part 2
                    message += "\n\n*Ответ:* задача с открытым ответом — введите текст"
                
                keyboard = solve_part2_keyboard() if solving_part == 2 else solve_part_keyboard()
                await query.edit_message_text(message, parse_mode="Markdown", reply_markup=keyboard)
                return
        await query.edit_message_text("Ошибка: задача не найдена.", reply_markup=tasks_menu_keyboard())
    elif data == "submit_feedback":
        # Показываем меню оценки
        context.user_data['awaiting_rating'] = True
        await query.edit_message_text(
            "⭐ *Оцените задачу от 1 до 5:*\n\n"
            "1 - ужасно\n2 - плохо\n3 - нормально\n4 - хорошо\n5 - отлично",
            parse_mode="Markdown",
            reply_markup=rating_keyboard()
        )
    elif data.startswith("rate_"):
        # Обработка нажатия кнопок 1-5
        rating = int(data.split("_")[1])
        task_id = context.user_data.get('current_task_id')
        if task_id:
            from lib.database import update_task_rating
            update_task_rating(task_id, rating)
        await query.edit_message_text(
            "Спасибо за оценку! Добавить эту задачу в черный список?",
            reply_markup=add_to_blacklist_keyboard()
        )
    elif data == "add_to_blacklist_yes":
        user_id = query.from_user.id
        task_id = context.user_data.get('current_task_id')
        if task_id:
            add_task_to_blacklist(user_id, task_id)
        await query.edit_message_text(
            "✅ Задача добавлена в черный список.",
            reply_markup=tasks_menu_keyboard()
        )
        clear_user_current_task(user_id)
        context.user_data.pop('current_task', None)
        context.user_data.pop('current_task_id', None)
        context.user_data.pop('solving_part', None)
    elif data == "add_to_blacklist_no":
        await query.edit_message_text(
            "✅ Хорошо, задача не добавлена в черный список.",
            reply_markup=tasks_menu_keyboard()
        )
        clear_user_current_task(user_id)
        context.user_data.pop('current_task', None)
        context.user_data.pop('current_task_id', None)
        context.user_data.pop('solving_part', None)
    elif data == "send_answer":
        # Отправка собранного ответа для 2 части
        user_id = query.from_user.id
        collected = context.user_data.get('collected_answer', '')
        if not collected.strip():
            await query.answer("Вы ещё не ввели ответ!", show_alert=True)
            return
        task = context.user_data.get('current_task')
        if not task:
            await query.edit_message_text("Ошибка: задача не найдена.", reply_markup=tasks_menu_keyboard())
            return
        
        # Заглушка проверки через нейросеть (позже заменим)
        verdict = f"✅ Ваш ответ: {collected}\n(проверка через нейросеть будет добавлена позже)"
        
        await query.edit_message_text(
            f"{verdict}\n\nПереходим к оценке задачи.",
            reply_markup=feedback_keyboard()
        )
        context.user_data.pop('collected_answer', None)
        # Показываем меню обратной связи (кнопки "вернуться к задаче" и "в меню")
        # Оценка будет после нажатия "submit_feedback" (или сразу предложить?)
        # По ТЗ: после вердикта сразу меню обратной связи с просьбой оценить.
        # Сделаем так: после вердикта отправляем сообщение с кнопкой "Оценить задачу"
        await query.message.reply_text(
            "Пожалуйста, оцените задачу от 1 до 5, нажав на кнопку ниже.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⭐ Оценить", callback_data="submit_feedback")]])
        )

async def show_tasks_menu(query):
    await query.edit_message_text(
        "📚 *Меню решения задач*\n\nВыберите режим:",
        parse_mode="Markdown",
        reply_markup=tasks_menu_keyboard()
    )

async def start_solve(update: Update, context: ContextTypes.DEFAULT_TYPE, part: int):
    query = update.callback_query
    user_id = query.from_user.id
    blacklist = get_user(user_id).get('blacklist', [])
    
    if part == 1:
        num_range = range(1, 17)
    else:
        num_range = range(17, 26)
    
    task = None
    for num in num_range:
        if num not in blacklist:
            task = get_task_by_num(num)
            if task:
                break
    
    if task:
        update_user_current_task(user_id, task['id'])
        context.user_data['current_task'] = task
        context.user_data['current_task_id'] = task['id']
        context.user_data['solving_part'] = part
        context.user_data['collected_answer'] = ""  # для 2 части
        
        message = f"*Задача №{task['num']}*\n\n{task['condition']}"
        if part == 1:
            if task['num'] in [6,13,15]:
                message += "\n\n*Ответ:* соответствие — введите последовательность цифр без пробелов"
                keyboard = solve_part_keyboard()
            else:
                message += "\n\n*Ответ:* набор вариантов — введите подряд без пробелов"
                keyboard = solve_part_keyboard()
        else:
            message += "\n\n*Ответ:* задача с открытым ответом — введите текст (можно несколькими сообщениями, затем нажмите «Отправить ответ»)"
            keyboard = solve_part2_keyboard()
        
        await query.edit_message_text(message, parse_mode="Markdown", reply_markup=keyboard)
    else:
        await query.edit_message_text(
            "😔 К сожалению, задача не нашлась.\nВозможно, стоит очистить черный список или связаться с создателями бота.",
            reply_markup=back_to_tasks_menu_keyboard()
        )

# Обработчики текстовых сообщений (ответы на задачи)
async def handle_part1_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data = get_user(user_id)
    current_task_id = user_data.get('current_task_id')
    if not current_task_id:
        return  # не решает задачу
    task = get_task_by_id(current_task_id)
    if not task:
        return
    
    answer = update.message.text.strip().lower()
    correct_answer = task['answer'].lower()
    
    if task['num'] in [6,13,15]:
        # Точное сравнение
        is_correct = (answer == correct_answer)
    else:
        # Сравнение наборов символов (убираем пробелы, сортируем)
        def normalize(s):
            return ''.join(sorted(s.replace(' ', '')))
        is_correct = (normalize(answer) == normalize(correct_answer))
    
    verdict = "✅ Верно!" if is_correct else "❌ Неверно!"
    await update.message.reply_text(
        f"{verdict}\n\nПравильный ответ: {task['answer']}\n\nПереходим к оценке задачи.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⭐ Оценить", callback_data="submit_feedback")]])
    )
    # Очищаем флаг решения, но сохраняем current_task_id для оценки
    # Не очищаем, чтобы потом добавить в ЧС

async def handle_part2_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data = get_user(user_id)
    current_task_id = user_data.get('current_task_id')
    if not current_task_id:
        return
    # Собираем ответ
    if 'collected_answer' not in context.user_data:
        context.user_data['collected_answer'] = ""
    context.user_data['collected_answer'] += update.message.text + "\n"
    await update.message.reply_text("Ответ добавлен. Можете продолжить ввод или нажать кнопку «Отправить ответ».")