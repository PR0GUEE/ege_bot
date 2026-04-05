from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from lib.database import get_user, update_user_current_task, clear_user_current_task, get_task_to_solve, add_task_to_blacklist, clear_blacklist, get_task_by_id
from lib.keyboards import tasks_menu_keyboard, back_to_main_keyboard, solve_part_keyboard, back_to_tasks_menu_keyboard, solve_part2_keyboard
from lib.keyboards import add_task_menu_keyboard, submit_cancel_keyboard
from lib.database import add_task, add_task_for_moderation


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    keyboard = [
        [InlineKeyboardButton("ℹ️ Информация о боте", callback_data="info")],
        [InlineKeyboardButton("📚 Решать задачи", callback_data="tasks")],
        [InlineKeyboardButton("💰 Монетизация", callback_data="monetization")],
        [InlineKeyboardButton("➕ Добавить задачу", callback_data="add_task")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Добро пожаловать в бот для подготовки к ЕГЭ по обществознанию!\n\n"
        "Выберите действие:",
        reply_markup=reply_markup
    )

async def handle_task_number_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get('awaiting_task_number'):
        return
    
    user_id = update.effective_user.id
    text = update.message.text.strip()
    
    if text.isdigit():
        num = int(text)
        if 1 <= num <= 25:
            user_data = get_user(user_id)
            blacklist = user_data.get('blacklist', [])
            task = get_task_to_solve([num], blacklist, user_id=user_id)
            if task:
                update_user_current_task(user_id, task['id'])
                context.user_data['current_task'] = task
                context.user_data['current_task_id'] = task['id']
                context.user_data['awaiting_task_number'] = False
                context.user_data['solving_part'] = 2  # конкретный номер = 2 часть (открытый ответ)
                
                message = f"*Задача №{task['num']}*\n\n{task['condition']}"
                message += "\n\n*Ответ:* задача с открытым ответом — введите текст"
                
                await update.message.reply_text(
                    message,
                    parse_mode="Markdown",
                    reply_markup=solve_part2_keyboard()
                )
            else:
                await update.message.reply_text(
                    "❌ Задача с таким номером не найдена.",
                    reply_markup=back_to_tasks_menu_keyboard()
                )
            return
        else:
            await update.message.reply_text(
                "❌ Некорректный ввод. Введите число от 1 до 25:",
                reply_markup=back_to_tasks_menu_keyboard()
            )
            return
    else:
        await update.message.reply_text(
            "❌ Некорректный ввод. Введите число от 1 до 25:",
            reply_markup=back_to_tasks_menu_keyboard()
        )
        return

async def add_task_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("🌍 Добавить задачу для всех", callback_data="add_task_global")],
        [InlineKeyboardButton("👤 Добавить задачу для себя", callback_data="add_task_private")],
        [InlineKeyboardButton("🔙 Назад", callback_data="main_menu")]
    ]
    await query.edit_message_text(
        "➕ *Добавление задачи*\n\n"
        "Куда хотите добавить задачу?",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def start_task_wizard(update: Update, context: ContextTypes.DEFAULT_TYPE, task_type: str):
    query = update.callback_query
    await query.answer()
    context.user_data['task_wizard'] = {'type': task_type, 'step': 'num'}
    await query.edit_message_text(
        "🔢 Введите номер задачи (от 1 до 25):\n\n"
        "Или нажмите кнопку «Отмена» для выхода.",
        reply_markup=submit_cancel_keyboard()
    )

async def handle_task_wizard_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'task_wizard' not in context.user_data:
        return
    wizard = context.user_data['task_wizard']
    text = update.message.text.strip()
    step = wizard['step']
    
    if step == 'num':
        if text.isdigit() and 1 <= int(text) <= 25:
            wizard['num'] = int(text)
            wizard['step'] = 'condition'
            wizard['condition_parts'] = []
            await update.message.reply_text(
                "📝 Введите условие задачи (можно несколькими сообщениями).\n"
                "Когда закончите, нажмите кнопку «✅ Готово».",
                reply_markup=submit_cancel_keyboard()
            )
        else:
            await update.message.reply_text(
                "❌ Некорректный номер. Введите число от 1 до 25:",
                reply_markup=submit_cancel_keyboard()
            )
    elif step == 'condition':
        # Собираем части условия
        if 'condition_parts' not in wizard:
            wizard['condition_parts'] = []
        wizard['condition_parts'].append(text)
        await update.message.reply_text("Условие добавлено. Продолжайте или нажмите «✅ Готово».")
    elif step == 'response':
        if 'response_parts' not in wizard:
            wizard['response_parts'] = []
        wizard['response_parts'].append(text)
        await update.message.reply_text("Ответ/критерии добавлены. Продолжайте или нажмите «✅ Готово».")

async def submit_task_wizard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    wizard = context.user_data.get('task_wizard')
    if not wizard:
        return
    
    step = wizard['step']
    if step == 'condition':
        # Сохраняем полное условие
        wizard['condition'] = '\n'.join(wizard.get('condition_parts', []))
        wizard['step'] = 'response'
        wizard['response_parts'] = []
        # Определяем подсказку в зависимости от номера
        num = wizard['num']
        if 1 <= num <= 16:
            if num in [6,13,15]:
                hint = "Введите ответ (соответствие) — последовательность цифр без пробелов:"
            else:
                hint = "Введите ответ (набор вариантов) — подряд без пробелов:"
        else:  # 17-25
            hint = "Введите критерии оценивания для задачи второй части (произвольный текст):"
        await query.edit_message_text(
            f"{hint}\n\nМожно вводить несколькими сообщениями. Когда закончите, нажмите «✅ Готово».",
            reply_markup=submit_cancel_keyboard()
        )
    elif step == 'response':
        # Сохраняем ответ/критерии
        response_text = '\n'.join(wizard.get('response_parts', []))
        num = wizard['num']
        condition = wizard['condition']
        user_id = update.effective_user.id
        task_type = wizard['type']  # 'global' или 'private'
        
        if task_type == 'private':
            add_task(num, condition, response_text, user_id=user_id)
            msg = "✅ Задача добавлена в ваш личный список. Она будет попадаться только вам."
        else:
            add_task_for_moderation(num, condition, response_text, user_id)
            msg = "📋 Задача отправлена на модерацию. После проверки она появится в общем доступе."
        
        await query.edit_message_text(msg, reply_markup=back_to_main_keyboard())
        # Очищаем wizard
        context.user_data.pop('task_wizard', None)
