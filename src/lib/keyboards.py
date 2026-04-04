from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("ℹ️ Информация о боте", callback_data="info")],
        [InlineKeyboardButton("📚 Решать задачи", callback_data="tasks")],
        [InlineKeyboardButton("💰 Монетизация", callback_data="monetization")],
        [InlineKeyboardButton("➕ Добавить задачу", callback_data="add_task")]
    ]
    return InlineKeyboardMarkup(keyboard)

def back_to_main_keyboard():
    keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="main_menu")]]
    return InlineKeyboardMarkup(keyboard)

def tasks_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("📝 Решать задачи 1 части", callback_data="solve_part1")],
        [InlineKeyboardButton("📝 Решать задачи 2 части", callback_data="solve_part2")],
        [InlineKeyboardButton("🔢 Решать задачу с конкретным номером", callback_data="solve_specific")],
        [InlineKeyboardButton("🗑 Очистить черный список", callback_data="clear_blacklist")],
        [InlineKeyboardButton("🔙 В главное меню", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def back_to_tasks_menu_keyboard():
    keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="back_to_tasks_menu")]]
    return InlineKeyboardMarkup(keyboard)

def solve_part_keyboard():
    keyboard = [
        [InlineKeyboardButton("❌ Перестать решать и вернуться", callback_data="stop_solving")]
    ]
    return InlineKeyboardMarkup(keyboard)

def solve_part2_keyboard():
    keyboard = [
        [InlineKeyboardButton("📤 Отправить ответ", callback_data="send_answer")],
        [InlineKeyboardButton("❌ Перестать решать и вернуться", callback_data="stop_solving")]
    ]
    return InlineKeyboardMarkup(keyboard)

def feedback_keyboard():
    keyboard = [
        [InlineKeyboardButton("🔄 Вернуться к решению задачи", callback_data="back_to_task")],
        [InlineKeyboardButton("📋 Вернуться в меню решения задач", callback_data="back_to_tasks_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def rating_keyboard():
    keyboard = [
        [InlineKeyboardButton("1", callback_data="rate_1"), InlineKeyboardButton("2", callback_data="rate_2"), InlineKeyboardButton("3", callback_data="rate_3")],
        [InlineKeyboardButton("4", callback_data="rate_4"), InlineKeyboardButton("5", callback_data="rate_5")]
    ]
    return InlineKeyboardMarkup(keyboard)

def add_to_blacklist_keyboard():
    keyboard = [
        [InlineKeyboardButton("✅ Да", callback_data="add_to_blacklist_yes")],
        [InlineKeyboardButton("❌ Нет", callback_data="add_to_blacklist_no")]
    ]
    return InlineKeyboardMarkup(keyboard)