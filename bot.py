import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import settings
from logger import setup_logger

from handlers.start import router as router_start


dp = Dispatcher()
dp.include_router(router_start)


async def main() -> None:
    setup_logger()
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
