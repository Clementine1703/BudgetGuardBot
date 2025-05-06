from core.stage import Stage
from core.callbacks import Callbacks
from core.utils import create_inline_kb


MAIN_MENU = Stage(
    msg='BudgetGuard – это бот для планирования бюджета и отслеживания расходов...',
    kb=create_inline_kb([
        [('💸 Внести трату', Callbacks.EXPENSE.SELECT_CATEGORY), ('💰 Внести доход', Callbacks.INCOME.SELECT_CATEGORY)],
        [('📊 Анализ и отчеты', Callbacks.ANALYTICS.MENU), ('📅 План бюджета', Callbacks.BUDGET.MENU)],
        [('📁 Категории и параметры', Callbacks.CATEGORY.MENU), ('🔔 Напоминания', Callbacks.REMINDER.MENU)],
        [('⚙️ Настройки', Callbacks.SETTINGS.MENU), ('📤 Экспорт / Импорт', Callbacks.EXPORT.MENU)]
    ]),
)
