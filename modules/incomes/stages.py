from core.stage import Stage
from core.keyboards import MAIN_MENU_BUTTON, BACK_BUTTON, SKIP_BUTTON
from core.utils import create_inline_kb


CATEGORY_SELECTION = Stage(
    msg=(
        "<b>📂 Выберите категорию дохода:</b>\n\n"
        "Нажмите на нужную категорию ниже."
    ),
    kb=create_inline_kb
)

DELETE_CATEGORY_SELECTION = Stage(
    msg=(
        "🗑 <b>Выберите категорию дохода, которую нужно удалить:</b>\n\n"
        "Внимание: это действие необратимо!"
    ),
    kb=create_inline_kb
)

CATEGORY_CREATION = Stage(
    msg=(
        "✏️ <b>Введите название новой категории дохода:</b>\n\n"
        "После ввода название будет сохранено."
    ),
    kb=create_inline_kb([
        [MAIN_MENU_BUTTON],
        [BACK_BUTTON],
    ])
)

AMOUNT_INPUT = Stage(
    msg=(
        "💰 <b>Введите размер дохода:</b>\n\n"
    ),
    kb=create_inline_kb([
        [MAIN_MENU_BUTTON],
        [BACK_BUTTON],
    ])
)

COMMENT_INPUT = Stage(
    msg=(
        "📝 <b>Введите описание дохода (опционально):</b>\n\n"
        "Можно оставить пустым, нажав 'Пропустить'."
    ),
    kb=create_inline_kb([
        [MAIN_MENU_BUTTON],
        [BACK_BUTTON],
        [SKIP_BUTTON],
    ])
)
