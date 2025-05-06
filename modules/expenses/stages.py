from core.stage import Stage
from core.callbacks import Callbacks
from core.keyboards import MAIN_MENU_BUTTON, BACK_BUTTON, SKIP_BUTTON
from core.utils import create_inline_kb


CATEGORY_SELECTION = Stage(
    msg='Выберите категорию расхода: ',
    kb=create_inline_kb
)


CATEGORY_CREATION = Stage(
    msg='Введите название категории: ',
    kb=create_inline_kb([
        [MAIN_MENU_BUTTON],
        [BACK_BUTTON]
    ]),
)


AMOUNT_INPUT = Stage(
    msg='Введите размер траты: ',
    kb=create_inline_kb([
        [MAIN_MENU_BUTTON],
        [BACK_BUTTON]
    ]),
)


COMMENT_INPUT = Stage(
    msg='Введите описание траты (опционально): ',
    kb=create_inline_kb([
        [MAIN_MENU_BUTTON],
        [BACK_BUTTON],
        [SKIP_BUTTON]
    ]),
)


