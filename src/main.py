import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from config import load_config
from lib import command_handlers, message_handlers

def main():
    config = load_config()
    logging.basicConfig(level=logging.INFO)
    
    app = Application.builder().token(config['telegram']['token']).build()
    
    app.add_handler(CommandHandler("start", command_handlers.start))
    app.add_handler(CallbackQueryHandler(message_handlers.button_handler))
    
    # Обработчик для ввода номера задачи
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, command_handlers.handle_task_number_input), group=1)
    # Обработчик для ответов на задачи 1 части
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handlers.handle_part1_answer), group=2)
    # Обработчик для сбора ответов 2 части (но он не должен конфликтовать, фильтруем по наличию current_task_id и solving_part)
    # Сделаем в самом обработчике проверку, поэтому просто добавим его
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handlers.handle_part2_answer), group=3)
    
    app.run_polling()

if __name__ == "__main__":
    main()