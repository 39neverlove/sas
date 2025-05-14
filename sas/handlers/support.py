from aiogram import types, Dispatcher
from config.settings import SUPPORT_TAG, ADMIN_ID
from utils.i18n import get_translation

async def support_menu(message: types.Message):
    user_id = message.from_user.id
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT language FROM users WHERE telegram_id = ?", (user_id,))
        lang = cursor.fetchone()[0] or "ru"

    await message.reply(get_translation(lang, "support_msg"))
    # Уведомление админа
    await message.bot.send_message(
        ADMIN_ID,
        f"Пользователь @{message.from_user.username or 'unknown'} запросил поддержку (ID: {user_id})"
    )

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(support_menu, regexp="Поддержка 🆘|Support 🆘|Destek 🆘")