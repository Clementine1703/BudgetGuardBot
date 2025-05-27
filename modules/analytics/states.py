from aiogram.fsm.state import StatesGroup, State


class AnalyticsStatesGroup(StatesGroup):
    STATS = State()
    STATS_CATEGORY_PIE = State()
    STATS_GRAPH = State()
    STATS_SUMMARY = State()
    STATS_AVERAGE = State()
    STATS_TOP_RECORDS = State()

    HISTORY = State()

    SELECT_PERIOD = State()
    PERIOD_INPUT_START = State()
    PERIOD_INPUT_END = State()
    PERIOD_RESULT = State()

    SELECT_CATEGORY = State()
    CATEGORY_RESULT = State()
