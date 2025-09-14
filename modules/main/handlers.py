from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from core.callbacks import Callbacks
from . import services


router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await services.handle_comand_start(message, state)


@router.callback_query(F.data == Callbacks.MAIN_MENU)
async def main_menu_handler(cb: CallbackQuery, state: FSMContext) -> None:
    await services.handle_main_menu(cb, state)


@router.callback_query()
async def fallback_callback_handler(cb: CallbackQuery, state: FSMContext) -> None:
    await services.handle_fallback(cb, state)


@router.message()
async def fallback_message_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        await services.handle_fallback(message, state)
