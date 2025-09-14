from typing import Union

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.callbacks import Callbacks
from .states import AddIncome
from . import services


router = Router()

@router.callback_query(AddIncome.create_category, F.data == Callbacks.BACK)
@router.callback_query(F.data == Callbacks.INCOME.SELECT_CATEGORY)
async def select_category_handler(cb: CallbackQuery, state: FSMContext) -> None:
    await services.handle_select_category(cb, state)


@router.callback_query(AddIncome.select_category, F.data == Callbacks.INCOME.CREATE_CATEGORY)
async def create_category_handler(cb: CallbackQuery, state: FSMContext) -> None:
    await services.handle_create_category(cb, state)


@router.message(AddIncome.create_category)
async def input_new_category_handler(message: Message, state: FSMContext) -> None:
    await services.handle_input_new_category(message, state)


@router.callback_query(AddIncome.select_category, F.data == Callbacks.INCOME.DELETE_CATEGORY)
async def select_deleting_category_handler(cb: CallbackQuery, state: FSMContext) -> None:
    await services.handle_select_deleting_category(cb, state)


@router.callback_query(AddIncome.delete_category, F.data.startswith(Callbacks.INCOME.ADD_AMOUNT))
async def delete_category_handler(cb: CallbackQuery, state: FSMContext) -> None:
    await services.handle_delete_category(cb, state)


@router.callback_query(AddIncome.select_category, F.data.startswith(Callbacks.INCOME.ADD_AMOUNT))
async def input_amount_handler(cb: CallbackQuery, state: FSMContext) -> None:
    await services.handle_input_amount(cb, state)


@router.message(AddIncome.input_amount)
async def input_comment_handler(message: Message, state: FSMContext) -> None:
    await services.handle_input_comment(message, state)


@router.callback_query(AddIncome.input_comment, F.data == Callbacks.SKIP)
@router.message(AddIncome.input_comment)
async def addition_income_handler(event: Union[Message, CallbackQuery], state: FSMContext) -> None:
    await services.handle_addition_income(event, state)
