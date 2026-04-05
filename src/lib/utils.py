from config import load_config
from lib.database import get_user
from lib.keyboards import back_to_main_keyboard

async def require_subscription(user_id, update_obj, context, callback_query=None):
    """
    Проверяет, имеет ли пользователь доступ к платным функциям.
    Возвращает True, если доступ разрешён, иначе отправляет сообщение и возвращает False.
    """
    config = load_config()
    if not config['monetization']['enabled']:
        return True
    
    user = get_user(user_id)
    if user['subscription_status']:
        return True
    
    # Нет подписки
    msg = "💰 Эта функция доступна только по подписке. Пожалуйста, оформите подписку в меню «Монетизация»."
    if callback_query:
        await callback_query.answer()
        await callback_query.edit_message_text(msg, reply_markup=back_to_main_keyboard())
    else:
        await update_obj.message.reply_text(msg, reply_markup=back_to_main_keyboard())
    return False