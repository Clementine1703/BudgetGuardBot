import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from core.config import settings
from core.logger import setup_logger
from middlewares import UserMiddleware, ChatLoggerMiddleware

from modules.main.handlers import router as router_main
from modules.expenses.handlers import router as router_expense
from modules.incomes.handlers import router as router_incomes


dp = Dispatcher()

middlewares = [UserMiddleware(), ChatLoggerMiddleware()]
for m in middlewares:
    dp.message.middleware(m)
    dp.callback_query.middleware(m)

dp.include_router(router_main)
dp.include_router(router_expense)
dp.include_router(router_incomes)


async def main() -> None:
    setup_logger()
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
