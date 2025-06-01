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
        log_payload = {}

        if isinstance(event, Message):
            log_payload = {
                "type": "message",
                "user_id": event.from_user.id,
                "chat_id": event.chat.id,
                "message_id": event.message_id,
                "content_type": event.content_type,
                "text": event.text or event.caption,
            }

        elif isinstance(event, CallbackQuery):
            log_payload = {
                "type": "callback_query",
                "user_id": event.from_user.id,
                "chat_id": event.message.chat.id if event.message else None,
                "message_id": event.message.message_id if event.message else None,
                "callback_data": event.data,
                "message_text": event.message.text if event.message else None,
            }

        if log_payload.get("chat_id") is not None:
            logger = get_current_chat_logger(log_payload["chat_id"])
            logger.info(f'Событие от пользователя: {log_payload}')

        return await handler(event, data)
