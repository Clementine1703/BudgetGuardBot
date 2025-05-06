from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from . import states, stages


async def handle_comand_start(message: Message, state: FSMContext) -> None:
    await state.set_state(states.MainMenu.main)
    await message.answer(stages.MAIN_MENU.msg(), reply_markup=stages.MAIN_MENU.kb())


async def handle_main_menu(cb: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(states.MainMenu.main)
    await cb.message.edit_text(
        stages.MAIN_MENU.msg(),
        reply_markup=stages.MAIN_MENU.kb(),
    )
