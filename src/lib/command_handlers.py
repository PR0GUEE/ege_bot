from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
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