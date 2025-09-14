from typing import Union

from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from pydantic import ValidationError

from core.callbacks import Callbacks
from core.keyboards import MAIN_MENU_BUTTON
from core.utils import send_validation_error_report
from . import states, stages, repositories
from .schemas import IncomeValidator


async def handle_select_category(cb: CallbackQuery, state: FSMContext) -> None:
    keyboard = await get_categories_kb(cb.from_user.id)
    await cb.message.edit_text(
        stages.CATEGORY_SELECTION.msg(),
        reply_markup=stages.CATEGORY_SELECTION.kb(keyboard)
    )
    await state.set_state(states.AddIncome.select_category)


async def handle_create_category(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.message.edit_text(
        stages.CATEGORY_CREATION.msg(),
        reply_markup=stages.CATEGORY_CREATION.kb()
    )
    await state.set_state(states.AddIncome.create_category)


async def handle_input_new_category(message: Message, state: FSMContext) -> None:
    try:
        IncomeValidator(category=message.text)
    except ValidationError as e:
        await send_validation_error_report(message, e)
        return

    await repositories.create_category(message.from_user.id, message.text)

    keyboard = await get_categories_kb(message.from_user.id)
    await message.answer(
        stages.CATEGORY_SELECTION.msg(),
        reply_markup=stages.CATEGORY_SELECTION.kb(keyboard)
    )
    await state.set_state(states.AddIncome.select_category)


async def handle_select_deleting_category(cb: CallbackQuery, state: FSMContext) -> None:
    """
    Обрабатывает запрос на выбор категории для удаления дохода.

    Args:
        cb (CallbackQuery): объект callback запроса из Telegram.
        state (FSMContext): контекст состояния FSM.
    """
    keyboard = await get_categories_kb(cb.from_user.id, simplified=True)
    await cb.message.edit_text(
        stages.DELETE_CATEGORY_SELECTION.msg(),
        reply_markup=stages.DELETE_CATEGORY_SELECTION.kb(keyboard)
    )
    await state.set_state(states.AddIncome.delete_category)


async def handle_delete_category(cb: CallbackQuery, state: FSMContext) -> None:
    """
    Удаляет категорию дохода.

    Args:
        cb (CallbackQuery): объект callback запроса из Telegram.
        state (FSMContext): контекст состояния FSM.
    """
    category_id = int(cb.data.split(':')[-1])
    await repositories.delete_category(cb.from_user.id, category_id)
    keyboard = await get_categories_kb(cb.from_user.id)
    await cb.message.edit_text(
        stages.CATEGORY_SELECTION.msg(),
        reply_markup=stages.CATEGORY_SELECTION.kb(keyboard)
    )
    await state.set_state(states.AddIncome.select_category)


async def handle_input_amount(cb: CallbackQuery, state: FSMContext) -> None:
    category_id = cb.data.split(':')[-1]
    await state.clear()
    await state.update_data(category_id=int(category_id))

    await cb.message.edit_text(
        stages.AMOUNT_INPUT.msg(),
        reply_markup=stages.AMOUNT_INPUT.kb()
    )
    await state.set_state(states.AddIncome.input_amount)


async def handle_input_comment(message: Message, state: FSMContext) -> None:
    try:
        IncomeValidator(amount=message.text)
    except ValidationError as e:
        await send_validation_error_report(message, e)
        return

    amount = message.text
    await state.update_data(amount=int(amount))
    await message.answer(
        stages.COMMENT_INPUT.msg(),
        reply_markup=stages.COMMENT_INPUT.kb()
    )
    await state.set_state(states.AddIncome.input_comment)


async def handle_addition_income(event: Union[Message, CallbackQuery], state: FSMContext) -> None:
    if isinstance(event, Message):
        try:
            IncomeValidator(comment=event.text)
        except ValidationError as e:
            await send_validation_error_report(event, e)
            return

        comment = event.text
        await state.update_data(comment=comment)
        message = event
    else:
        message = event.message


    income_data = await state.get_data()
    await repositories.create_income(income_data)

    keyboard = await get_categories_kb(event.from_user.id)

    await message.answer(
        f'Доход успешно добавлен\n\n{stages.CATEGORY_SELECTION.msg()}',
        reply_markup=stages.CATEGORY_SELECTION.kb(keyboard)
    )
    await state.set_state(states.AddIncome.select_category)


async def get_categories_kb(user_id: int, simplified: bool = False) -> list[list[tuple[str, str] | InlineKeyboardButton]]:
    categories = await repositories.get_all_categories(user_id)
    buttons = [[(c.name, f'{Callbacks.INCOME.ADD_AMOUNT}:{str(c.id)}')] for c in categories]
    buttons.extend([
            [MAIN_MENU_BUTTON]
        ] if simplified else [
            [("➕ Создать категорию доходов", Callbacks.INCOME.CREATE_CATEGORY)],
            [("❌ Удалить категорию доходов", Callbacks.INCOME.DELETE_CATEGORY)],
            [MAIN_MENU_BUTTON]
        ]
    )
    return buttons
