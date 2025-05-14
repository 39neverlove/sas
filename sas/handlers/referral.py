from aiogram import types, Dispatcher
from database.db import Database
from utils.i18n import get_translation

db = Database()

async def referral_menu(message: types.Message):
    user_id = message.from_user.id
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT language, referrals FROM users WHERE telegram_id = ?", (user_id,))
        user = cursor.fetchone()
        if not user:
            await message.reply("Пожалуйста, начните с команды /start")
            return
        lang, referrals = user

    referral_link = f"https://t.me/{(await message.bot.me).username}?start=ref_{user_id}"
    await message.reply(
        get_translation(lang, "referral_link", link=referral_link) +
        f"\nПриглашено: {referrals} пользователей"
    )

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(referral_menu, regexp="Реферальная система 💎|Referral system 💎|Referans sistemi 💎")