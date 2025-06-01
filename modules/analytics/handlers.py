from typing import Union

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.callbacks import Callbacks
from . import services, states


router = Router()

@router.callback_query(states.AnalyticsStatesGroup.STATS_MENU, F.data == Callbacks.BACK)
@router.callback_query(F.data == Callbacks.ANALYTICS.MENU)
async def analytics_menu_handler(cb: CallbackQuery, state: FSMContext) -> None:
    await services.analytics_menu_handler(cb, state)


@router.callback_query(F.data == Callbacks.ANALYTICS.STATS.MENU)
async def analytics_stats_handler(cb: CallbackQuery, state: FSMContext) -> None:
    await services.analytics_stats_handler(cb, state)


@router.callback_query(F.data == Callbacks.ANALYTICS.STATS.CATEGORY_PIE)
async def analytics_stats_category_pie_period_start_handler(cb: CallbackQuery, state: FSMContext) -> None:
    await services.analytics_stats_category_pie_start_picker_handler(cb, state)


@router.callback_query(states.AnalyticsStatesGroup.STATS_CATEGORY_PIE, F.data == Callbacks.CONFIRM)
async def analytics_stats_category_pie_period_confirm_handler(cb: CallbackQuery, state: FSMContext) -> None:
    await services.analytics_stats_category_pie_period_confirm_handler(cb, state)


@router.callback_query(F.data == Callbacks.ANALYTICS.STATS.INCOME_EXPENSE_LINE)
async def analytics_stats_income_expense_line_period_start_handler(cb: CallbackQuery, state: FSMContext) -> None:
    """
    Хендлер начала выбора периода для графика доходов и расходов.
    """
    await services.analytics_stats_income_expense_line_start_picker_handler(cb, state)


@router.callback_query(states.AnalyticsStatesGroup.STATS_INCOME_EXPENSE_LINE, F.data == Callbacks.CONFIRM)
async def analytics_stats_income_expense_line_period_confirm_handler(cb: CallbackQuery, state: FSMContext) -> None:
    """
    Хендлер подтверждения периода и отправки графика доходов и расходов.
    """
    await services.analytics_stats_income_expense_line_period_confirm_handler(cb, state)


@router.callback_query(F.data == Callbacks.ANALYTICS.STATS.SUMMARY)
async def summary_period_start_handler(cb: CallbackQuery, state: FSMContext) -> None:
    """
    Начало выбора периода для показа итогов.
    """
    await services.summary_period_start_picker_handler(cb, state)


@router.callback_query(states.AnalyticsStatesGroup.STATS_SUMMARY, F.data == Callbacks.CONFIRM)
async def summary_period_confirm_handler(cb: CallbackQuery, state: FSMContext) -> None:
    """
    Подтверждение периода и отправка итогов за период.
    """
    await services.summary_period_confirm_handler(cb, state)
