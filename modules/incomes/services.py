from typing import Union

from aiogram.types import Message, CallbackQuery, KeyboardButton
from aiogram.fsm.context import FSMContext
from pydantic import ValidationError

from core.callbacks import Callbacks
from core.keyboards import MAIN_MENU_BUTTON, BACK_BUTTON
from core.utils import send_validation_error_report
from . import states, stages, repositories, schemas
from .schemas import IncomeValidator


async def handle_select_category(cb: CallbackQuery, state: FSMContext) -> None:
    categories = await repositories.get_all_categories(cb.from_user.id)
    buttons = [[(c.name, f'{Callbacks.INCOME.ADD_AMOUNT}:{str(c.id)}')] for c in categories]
    buttons.extend([
        [("➕ Создать категорию доходов", Callbacks.INCOME.CREATE_CATEGORY)],
        [MAIN_MENU_BUTTON]
    ]),

    await cb.message.edit_text(
        stages.CATEGORY_SELECTION.msg(),
        reply_markup=stages.CATEGORY_SELECTION.kb(buttons)
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
        validated = IncomeValidator(category=message.text)
    except ValidationError as e:
        await send_validation_error_report(message, e)
        return

    await repositories.create_category(message.from_user.id, message.text)

    categories = await repositories.get_all_categories(message.from_user.id)
    buttons = [[(c.name, f'{Callbacks.INCOME.ADD_AMOUNT}:{str(c.id)}')] for c in categories]
    buttons.extend([
        [("➕ Создать категорию доходов", Callbacks.INCOME.CREATE_CATEGORY)],
        [MAIN_MENU_BUTTON]
    ]),

    await message.answer(
        stages.CATEGORY_SELECTION.msg(),
        reply_markup=stages.CATEGORY_SELECTION.kb(buttons)
    )
    await state.set_state(states.AddIncome.select_category)


async def handle_input_amount(cb: CallbackQuery, state: FSMContext) -> None:
    category_id = cb.data.split(':')[-1]
    await state.update_data(category_id=int(category_id))

    await cb.message.edit_text(
        stages.AMOUNT_INPUT.msg(),
        reply_markup=stages.AMOUNT_INPUT.kb()
    )
    await state.set_state(states.AddIncome.input_amount)


async def handle_input_comment(message: Message, state: FSMContext) -> None:
    try:
        validated = IncomeValidator(amount=message.text)
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
            validated = IncomeValidator(comment=event.text)
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

    categories = await repositories.get_all_categories(event.from_user.id)
    buttons = [[(c.name, f'{Callbacks.INCOME.ADD_AMOUNT}:{str(c.id)}')] for c in categories]
    buttons.extend([
        [("➕ Создать категорию доходов", Callbacks.INCOME.CREATE_CATEGORY)],
        [MAIN_MENU_BUTTON]
    ]),

    await message.answer(
        f'Доход успешно добавлен\n\n{stages.CATEGORY_SELECTION.msg()}',
        reply_markup=stages.CATEGORY_SELECTION.kb(buttons)
    )
    await state.set_state(states.AddIncome.select_category)
