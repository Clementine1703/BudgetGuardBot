from typing import Union

from aiogram.types import Message, CallbackQuery, KeyboardButton
from aiogram.fsm.context import FSMContext
from pydantic import ValidationError

from core.callbacks import Callbacks
from core.keyboards import MAIN_MENU_BUTTON, BACK_BUTTON
from core.utils import send_validation_error_report
from . import states, stages, repositories, schemas


async def analytics_menu_handler(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.message.edit_text(
        stages.MENU.msg(),
        reply_markup=stages.MENU.kb(),
    )


async def analytics_stats_handler(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.message.edit_text(
        stages.STATS.msg(),
        reply_markup=stages.STATS.kb(),
    )
    await state.set_state(states.AnalyticsStatesGroup.STATS)


async def analytics_stats_category_pie_handler(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.message.edit_text(
        stages.STATS.msg(),
        reply_markup=stages.STATS.kb(),
    )
    await state.set_state(states.AnalyticsStatesGroup.STATS)

