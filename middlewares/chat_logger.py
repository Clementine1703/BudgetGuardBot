from typing import Callable, Dict, Any, Awaitable, Union
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from core.logger import get_current_chat_logger


class ChatLoggerMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Union[Message, CallbackQuery], Dict[str, Any]], Awaitable[Any]],
            event: Union[Message, CallbackQuery],
            data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, Message):
            chat_id = event.chat.id
        elif isinstance(event, CallbackQuery):
            chat_id = event.message.chat.id if event.message else None
        else:
            return await handler(event, data)

        if chat_id is not None:
            logger = get_current_chat_logger(chat_id)
            logger.info(f'Событие от пользователя: {event}')

        return await handler(event, data)