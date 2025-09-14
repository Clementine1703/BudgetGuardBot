from core.stage import Stage
from core.keyboards import MAIN_MENU_BUTTON, CONFIRM_BUTTON
from core.utils import create_inline_kb


DATE_CONFIRM = Stage(
    msg='',
    kb=create_inline_kb([
        [CONFIRM_BUTTON],
        [MAIN_MENU_BUTTON]
    ]),
)
