from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from database.db import Database
from utils.i18n import get_translation
from utils.stats import generate_stats_graph
from config.settings import ADMIN_ID

db = Database()

async def admin_panel(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.reply("Доступ запрещен!")
        return

    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT language FROM users WHERE telegram_id = ?", (message.from_user.id,))
        lang = cursor.fetchone()[0] or "ru"

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Статистика", "Управление пользователями", "Рассылка"]
    keyboard.add(*buttons)
    await message.reply(get_translation(lang, "admin_menu"), reply_markup=keyboard)

async def admin_stats(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM accounts")
        total_accounts = cursor.fetchone()[0]
        cursor.execute("SELECT region, COUNT(*) FROM accounts GROUP BY region")
        regions = cursor.fetchall()

    stats_text = f"Пользователи: {total_users}\nАккаунты: {total_accounts}\nПо регионам:\n"
    for region, count in regions:
        stats_text += f"{region}: {count}\n"

    await message.reply(stats_text)
    # Отправка графика
    graph = generate_stats_graph()
    await message.bot.send_photo(message.chat.id, photo=graph)

async def admin_users(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT telegram_id, username, is_blocked FROM users LIMIT 5")
        users = cursor.fetchall()

    response = "Пользователи:\n"
    for user in users:
        status = "Заблокирован" if user[2] else "Активен"
        response += f"ID: {user[0]}, @{user[1]} - {status}\n"
    response += "\nДля блокировки/разблокировки: /block <telegram_id> или /unblock <telegram_id>"

    await message.reply(response)

async def admin_broadcast(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    await message.reply("Введите сообщение для рассылки:")
    # Здесь можно добавить FSM для обработки ввода сообщения

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(admin_panel, commands=["admin"])
    dp.register_message_handler(admin_stats, regexp="Статистика")
    dp.register_message_handler(admin_users, regexp="Управление пользователями")
    dp.register_message_handler(admin_broadcast, regexp="Рассылка")