from core.stage import Stage
from core.callbacks import Callbacks
from core.utils import create_inline_kb


MAIN_MENU = Stage(
    msg=(
        "<b>🏠 Главное меню:</b>\n\n"
        "Выберите одно из действий ниже:"
    ),
    kb=create_inline_kb([
        [
            ('💸 Внести трату', Callbacks.EXPENSE.SELECT_CATEGORY),
            ('💰 Внести доход', Callbacks.INCOME.SELECT_CATEGORY)
        ],
        [
            ('📊 Анализ и отчеты', Callbacks.ANALYTICS.MENU)
        ],
    ]),
)


FALLBACK_MAIN_MENU = Stage(
    msg=(
        "⚠️ <b>Что-то пошло не так.</b>\n\n"
        "Вы были перемещены в главное меню. Выберите действие:"
    ),
    kb=create_inline_kb([
        [
            ('💸 Внести трату', Callbacks.EXPENSE.SELECT_CATEGORY),
            ('💰 Внести доход', Callbacks.INCOME.SELECT_CATEGORY)
        ],
        [
            ('📊 Анализ и отчеты', Callbacks.ANALYTICS.MENU)
        ],
    ]),
)
