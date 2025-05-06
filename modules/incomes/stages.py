from core.stage import Stage
from core.keyboards import MAIN_MENU_BUTTON, BACK_BUTTON, SKIP_BUTTON
from core.utils import create_inline_kb


CATEGORY_SELECTION = Stage(
    msg='Выберите категорию дохода: ',
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
    msg='Введите размер дохода: ',
    kb=create_inline_kb([
        [MAIN_MENU_BUTTON],
        [BACK_BUTTON]
    ]),
)


COMMENT_INPUT = Stage(
    msg='Введите описание дохода (опционально): ',
    kb=create_inline_kb([
        [MAIN_MENU_BUTTON],
        [BACK_BUTTON],
        [SKIP_BUTTON]
    ]),
)


