from typing import Union

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.callbacks import Callbacks
from .states import AnalyticsStatesGroup
from . import services, states


router = Router()

@router.callback_query(states.AnalyticsStatesGroup.STATS, F.data == Callbacks.BACK)
@router.callback_query(F.data == Callbacks.ANALYTICS.MENU)
async def analytics_menu_handler(cb: CallbackQuery, state: FSMContext) -> None:
    await services.analytics_menu_handler(cb, state)


@router.callback_query(F.data == Callbacks.ANALYTICS.STATS.MENU)
async def analytics_stats_handler(cb: CallbackQuery, state: FSMContext) -> None:
    await services.analytics_stats_handler(cb, state)


# @router.callback_query(F.data == Callbacks.ANALYTICS.STATS.CATEGORY_PIE)
# async def analytics_stats_category_pie(cb: CallbackQuery, state: FSMContext) -> None:
#     await services.analytics_stats_category_pie_handler(cb, state)


# @router.message(AddExpense.create_category)
# async def input_new_category_handler(message: Message, state: FSMContext) -> None:
#     await services.handle_input_new_category(message, state)
