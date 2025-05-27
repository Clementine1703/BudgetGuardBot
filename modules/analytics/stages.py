from core.stage import Stage
from core.callbacks import Callbacks
from core.keyboards import MAIN_MENU_BUTTON, BACK_BUTTON, SKIP_BUTTON
from core.utils import create_inline_kb


MENU = Stage(
    msg='BudgetGuard – это бот для планирования бюджета и отслеживания расходов...',
    kb=create_inline_kb([
        [('📈 Статистика и графики', Callbacks.ANALYTICS.STATS.MENU)],
        [('🧾 История операций', Callbacks.ANALYTICS.HISTORY)],
        [('📆 За период', Callbacks.ANALYTICS.PERIOD)],
        [('🔎 По категории', Callbacks.ANALYTICS.CATEGORY)],
        [MAIN_MENU_BUTTON]
    ]),
)

STATS = Stage(
    msg='Статистика и графики',
    kb=create_inline_kb([
        # [('📊 Диаграмма по категориям', Callbacks.ANALYTICS.STATS.CATEGORY_PIE)],
        [('📊 Пикер пока что', Callbacks.PERIOD_PICKER.SELECT)],
        [('📈 График трат и доходов', Callbacks.ANALYTICS.STATS.GRAPH)],
        [('📅 Итоги за месяц', Callbacks.ANALYTICS.STATS.SUMMARY)],
        [('📉 Средние значения', Callbacks.ANALYTICS.STATS.AVERAGE)],
        [('🔝 Рекорды и топ категории', Callbacks.ANALYTICS.STATS.TOP_RECORDS)],
        [MAIN_MENU_BUTTON],
        [BACK_BUTTON]
    ]),
)
#
# STATS_CATEGORY_PIE = Stage(
#     msg='Выберите период:',
#     kb=create_inline_kb([
#         [('День', Callbacks.ANALYTICS.STATS.CATEGORY_PIE)],
#         [('Неделя', Callbacks.ANALYTICS.STATS.BY_DAY_CHART)],
#         [('Месяц', Callbacks.ANALYTICS.STATS.MONTH_SUMMARY)],
#         [('Свой период', Callbacks.ANALYTICS.STATS.DAILY_AVG)],
#         [MAIN_MENU_BUTTON],
#         [BACK_BUTTON]
#     ]),
# )

