from aiogram.types import InlineKeyboardButton

from .callbacks import Callbacks


MAIN_MENU_BUTTON = InlineKeyboardButton(text='🏠 В главное меню', callback_data=Callbacks.MAIN_MENU)
BACK_BUTTON = InlineKeyboardButton(text='⬅️ Назад', callback_data=Callbacks.BACK)
SKIP_BUTTON = InlineKeyboardButton(text='➡️ Пропустить', callback_data=Callbacks.SKIP)