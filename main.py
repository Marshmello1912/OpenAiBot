import asyncio

from aiogram import Dispatcher, Bot
from handlers import register_handlers
from aiogram.contrib.fsm_storage.memory import MemoryStorage


async def main():
    bot = Bot("")
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    register_handlers(dp)

    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
