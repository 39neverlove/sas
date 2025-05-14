import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config.settings import TELEGRAM_TOKEN
from handlers import start, registration, referral, language, support, admin

async def main():
    bot = Bot(token=TELEGRAM_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    # Регистрация обработчиков
    start.register_handlers(dp)
    registration.register_handlers(dp)
    referral.register_handlers(dp)
    language.register_handlers(dp)
    support.register_handlers(dp)
    admin.register_handlers(dp)

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())