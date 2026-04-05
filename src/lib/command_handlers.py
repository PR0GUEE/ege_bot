from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from lib.database import get_user, update_user_current_task, clear_user_current_task, get_task_to_solve, add_task_to_blacklist, clear_blacklist, get_task_by_id
from lib.keyboards import tasks_menu_keyboard, back_to_main_keyboard, solve_part_keyboard, back_to_tasks_menu_keyboard, solve_part2_keyboard

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
            task = get_task_to_solve([num], blacklist)
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
