import asyncio
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from loadotenv import load_env

from handlers.start import router as router_start


load_env()
TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()
dp.include_router(router_start)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
