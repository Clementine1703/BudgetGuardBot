from typing import List, Type, TypeVar, Union

from pydantic import ValidationError
from sqlalchemy import select
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, Message

from .database import db_session
from .keyboards import MAIN_MENU_BUTTON


T = TypeVar('T')


@db_session
async def get_or_create(session, model, **search_params):
    stmt = select(model).filter_by(**search_params)
    s = await session.scalars(stmt)
    instance = s.first()

    if instance:
        return instance, False

    instance = model(**search_params)
    session.add(instance)
    await session.commit()
    return instance, True


def create_inline_kb(
    buttons: list[list[Union[InlineKeyboardButton, tuple[str, str]]]]
) -> InlineKeyboardMarkup:
    keyboard = [
        [
            btn if isinstance(btn, InlineKeyboardButton)
            else InlineKeyboardButton(text=btn[0], callback_data=btn[1])
            for btn in row
        ]
        for row in buttons
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def create_reply_kb(buttons: list[list[Union[InlineKeyboardButton, str]]]) -> ReplyKeyboardMarkup:
    keyboard = [
        [
            btn if isinstance(btn, KeyboardButton)
            else KeyboardButton(text=btn)
            for btn in row
        ]
        for row in buttons
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard)


def extract_objects_of_class(data: List, target_class: Type[T]) -> List[T]:
    results = []
    for el in data:
        if isinstance(el, target_class):
            results.append(el)
        elif isinstance(el, list):
            results.extend(extract_objects_of_class(el, target_class))
    return results


async def send_validation_error_report(message: Message, e: ValidationError):
    error_messages = "Возникли следующие ошибки валидации:\n\n"

    for error in e.errors():
        field = error['loc'][-1]
        msg = error['msg']

        error_messages += f"🔴 Ошибка в поле: *{field}*\n"
        error_messages += f"💬 Сообщение: *{msg}*\n\n"

    await message.answer(
        error_messages,
        parse_mode="Markdown",
        reply_markup=create_inline_kb([[
            MAIN_MENU_BUTTON,
        ]])
    )
