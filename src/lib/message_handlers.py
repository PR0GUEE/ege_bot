from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "info":
        await query.edit_message_text(
            "📖 *Информация о боте*\n\n"
            "Бот для подготовки к ЕГЭ по обществознанию.\n"
            "Версия: 1.0.0\n\n"
            "Здесь будут появляться задачи и тесты для подготовки.",
            parse_mode="Markdown",
            reply_markup=back_to_main_keyboard()
        )
    
    elif query.data == "tasks":
        await query.edit_message_text(
            "📚 *Решение задач*\n\n"
            "Раздел в разработке.",
            parse_mode="Markdown",
            reply_markup=back_to_main_keyboard()
        )
    
    elif query.data == "monetization":
        await query.edit_message_text(
            "💰 *Монетизация*\n\n"
            "Раздел в разработке.",
            parse_mode="Markdown",
            reply_markup=back_to_main_keyboard()
        )
    
    elif query.data == "add_task":
        await query.edit_message_text(
            "➕ *Добавление задачи*\n\n"
            "Раздел в разработке.",
            parse_mode="Markdown",
            reply_markup=back_to_main_keyboard()
        )
    
    elif query.data == "main_menu":
        await query.edit_message_text(
            "Добро пожаловать в бот для подготовки к ЕГЭ по обществознанию!\n\n"
            "Выберите действие:",
            reply_markup=main_menu_keyboard()
        )

def back_to_main_keyboard():
    keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="main_menu")]]
    return InlineKeyboardMarkup(keyboard)

def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("ℹ️ Информация о боте", callback_data="info")],
        [InlineKeyboardButton("📚 Решать задачи", callback_data="tasks")],
        [InlineKeyboardButton("💰 Монетизация", callback_data="monetization")],
        [InlineKeyboardButton("➕ Добавить задачу", callback_data="add_task")]
    ]
    return InlineKeyboardMarkup(keyboard)