import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from config import load_config
from lib import command_handlers, message_handlers

def main():
    config = load_config()

    logging.basicConfig(level=logging.INFO)

    app = Application.builder().token(config['telegram']['token']).build()

    app.add_handler(CommandHandler("start", command_handlers.start))
    app.add_handler(CallbackQueryHandler(message_handlers.button_handler))

    app.run_polling()

if __name__ == "__main__":
    main()