from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from database.db import Database
from utils.i18n import get_translation
from config.settings import SUPPORT_TAG

db = Database()

async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or "unknown"
    args = message.get_args()

    # Проверка реферала
    if args.startswith("ref_"):
        referrer_id = int(args.split("_")[1])
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO users (telegram_id, username, created_accounts) VALUES (?, ?, ?)", 
                         (user_id, username, 5))  # 5 аккаунтов для приглашенного
            cursor.execute("SELECT referrals FROM users WHERE telegram_id = ?", (referrer_id,))
            if cursor.fetchone():
                cursor.execute("INSERT INTO referrals (referrer_id, referred_id) VALUES (?, ?)", (referrer_id, user_id))
                cursor.execute("UPDATE users SET referrals = referrals + 1, created_accounts = created_accounts + 3 WHERE telegram_id = ?", 
                             (referrer_id,))
            conn.commit()

    # Создание пользователя, если не существует
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO users (telegram_id, username) VALUES (?, ?)", (user_id, username))
        cursor.execute("SELECT language FROM users WHERE telegram_id = ?", (user_id,))
        lang = cursor.fetchone()[0] or "ru"
        conn.commit()

    # Главное меню
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        get_translation(lang, "create_account"),
        get_translation(lang, "referral"),
        get_translation(lang, "support"),
        get_translation(lang, "stats")
    ]
    keyboard.add(*buttons)
    await message.reply(get_translation(lang, "welcome"), reply_markup=keyboard)

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=["start"])