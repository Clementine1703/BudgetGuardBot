from core.stage import Stage
from core.callbacks import Callbacks
from core.keyboards import MAIN_MENU_BUTTON, BACK_BUTTON
from core.utils import create_inline_kb


MENU = Stage(
    msg='BudgetGuard – это бот для планирования бюджета и отслеживания расходов...',
    kb=create_inline_kb([
        [('📈 Статистика и графики', Callbacks.ANALYTICS.STATS.MENU)],
        [('🧾 История операций', Callbacks.ANALYTICS.HISTORY)],
        [MAIN_MENU_BUTTON]
    ]),
)

STATS_MENU = Stage(
    msg='Статистика и графики',
    kb=create_inline_kb([
        [('📊 Диаграммы по категориям', Callbacks.ANALYTICS.STATS.CATEGORY_PIE)],
        [('📈 График трат и доходов', Callbacks.ANALYTICS.STATS.INCOME_EXPENSE_LINE)],
        [('📅 Итоги за месяц', Callbacks.ANALYTICS.STATS.SUMMARY)],
        [MAIN_MENU_BUTTON],
        [BACK_BUTTON]
    ]),
)
