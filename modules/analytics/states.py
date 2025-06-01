from aiogram.fsm.state import StatesGroup, State


class AnalyticsStatesGroup(StatesGroup):
    STATS_MENU = State()
    STATS_CATEGORY_PIE = State()
    STATS_INCOME_EXPENSE_LINE = State()
    STATS_SUMMARY = State()

    HISTORY = State()

