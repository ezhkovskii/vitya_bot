import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import settings
from log import logger
from handlers import router

async def main():
    bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    logger.info("Бот запущен!")
    dp.include_router(router=router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())