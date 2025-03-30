from aiogram import Router, html
from aiogram.filters import CommandStart
from aiogram.types import Message

from middlewares import chat_logger


router = Router()
router.message.middleware(chat_logger.ChatLoggerMiddleware())


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # raise ValueError("Ошибочка вышла")
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")
