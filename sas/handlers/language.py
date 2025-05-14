from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db import Database
from utils.i18n import get_translation

db = Database()

async def cmd_lang(message: types.Message):
    user_id = message.from_user.id
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT language FROM users WHERE telegram_id = ?", (user_id,))
        lang = cursor.fetchone()[0] or "ru"

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("Русский", callback_data="lang_ru"),
        InlineKeyboardButton("English", callback_data="lang_en"),
        InlineKeyboardButton("Türkçe", callback_data="lang_tr")
    )
    await message.reply(get_translation(lang, "lang_select"), reply_markup=keyboard)

async def set_language(callback: types.CallbackQuery):
    lang = callback.data.split("_")[1]
    user_id = callback.from_user.id
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET language = ? WHERE telegram_id = ?", (lang, user_id))
        conn.commit()
    await callback.message.edit_text(get_translation(lang, "lang_select") + f"\nSelected: {lang}")
    await callback.answer()

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_lang, commands=["lang"])
    dp.register_callback_query_handler(set_language, regexp="lang_")