from aiogram import types, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from database.db import Database
from services.steam import create_steam_account
from utils.rate_limiter import RateLimiter
from utils.i18n import get_translation

db = Database()
limiter = RateLimiter(max_requests=5, time_window=60)

class RegistrationStates(StatesGroup):
    SELECT_PROXY = State()
    CREATE_ACCOUNT = State()

async def create_account_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT language, created_accounts, is_blocked FROM users WHERE telegram_id = ?", (user_id,))
        user = cursor.fetchone()
        if not user:
            await message.reply("Пожалуйста, начните с команды /start")
            return
        lang, created_accounts, is_blocked = user

        if is_blocked:
            await message.reply("Ваш аккаунт заблокирован.")
            return

        if created_accounts <= 0:
            await message.reply(get_translation(lang, "no_accounts_left"))
            return

        if not limiter.allow(user_id):
            await message.reply(get_translation(lang, "rate_limit_exceeded"))
            return

    # Запрос на использование прокси
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time=True)
    keyboard.add(get_translation(lang, "yes"), get_translation(lang, "no"))
    await message.reply(get_translation(lang, "use_proxy"), reply_markup=keyboard)
    await RegistrationStates.SELECT_PROXY.set()

async def select_proxy(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT language FROM users WHERE telegram_id = ?", (user_id,))
        lang = cursor.fetchone()[0] or "ru"

    use_proxy = message.text == get_translation(lang, "yes")
    await state.update_data(use_proxy=use_proxy)

    try:
        await limiter.random_delay()
        account_data = await create_steam_account(region="Turkey", use_proxy=use_proxy)
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO accounts (login, password, email, region, user_id) VALUES (?, ?, ?, ?, ?)",
                (account_data["login"], account_data["password"], account_data["email"], account_data["region"], user_id)
            )
            cursor.execute("UPDATE users SET created_accounts = created_accounts - 1 WHERE telegram_id = ?", (user_id,))
            conn.commit()
        await message.reply(
            f"{get_translation(lang, 'account_created')}:\n"
            f"Login: {account_data['login']}\nPassword: {account_data['password']}\nEmail: {account_data['email']}",
            reply_markup=types.ReplyKeyboardRemove()
        )
    except Exception as e:
        await message.reply(f"Ошибка: {str(e)}", reply_markup=types.ReplyKeyboardRemove())
    finally:
        await state.finish()

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(create_account_start, regexp="Создать аккаунты 🛠|Create accounts 🛠|Hesap oluştur 🛠")
    dp.register_message_handler(select_proxy, state=RegistrationStates.SELECT_PROXY)