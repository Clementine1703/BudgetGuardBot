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
