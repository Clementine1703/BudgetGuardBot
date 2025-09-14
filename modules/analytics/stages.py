from core.stage import Stage
from core.callbacks import Callbacks
from core.keyboards import MAIN_MENU_BUTTON, BACK_BUTTON
from core.utils import create_inline_kb


MENU = Stage(
    msg=(
        "📊 <b>Меню аналитики:</b>\n\n"
        "Выберите один из разделов, чтобы просмотреть статистику или историю операций:"
    ),
    kb=create_inline_kb([
        [('📈 Статистика и графики', Callbacks.ANALYTICS.STATS.MENU)],
        [('🧾 История операций', Callbacks.ANALYTICS.HISTORY.MENU)],
        [MAIN_MENU_BUTTON]
    ]),
)

STATS_MENU = Stage(
    msg=(
        "📊 <b>Статистика и графики:</b>\n\n"
        "Выберите, какую информацию вы хотите просмотреть:"
    ),
    kb=create_inline_kb([
        [('📊 Диаграммы по категориям', Callbacks.ANALYTICS.STATS.CATEGORY_PIE)],
        [('📈 График трат и доходов', Callbacks.ANALYTICS.STATS.INCOME_EXPENSE_LINE)],
        [('📅 Итоги за период', Callbacks.ANALYTICS.STATS.SUMMARY)],
        [BACK_BUTTON],
        [MAIN_MENU_BUTTON],
    ]),
)

HISTORY_MENU = Stage(
    msg=(
        "🧾 <b>История операций:</b>\n\n"
        "Выберите период, за который хотите просмотреть операции:"
    ),
    kb=create_inline_kb([
        [('За 24 часа', Callbacks.ANALYTICS.HISTORY.LAST_DAY)],
        [('За неделю', Callbacks.ANALYTICS.HISTORY.LAST_WEEK)],
        [('📅 Свой период', Callbacks.ANALYTICS.HISTORY.PERIOD)],
        [BACK_BUTTON],
        [MAIN_MENU_BUTTON],
    ]),
)