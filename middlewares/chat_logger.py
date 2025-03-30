from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from logger import get_current_chat_logger


class ChatLoggerMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        logger = get_current_chat_logger(event.chat.id)
        logger.info(f'Событие от пользователя: {event}')
        return await handler(event, data)
