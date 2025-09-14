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


async def handle_fallback(event: Message | CallbackQuery, state: FSMContext) -> None:
    await state.set_state(states.MainMenu.main)

    text = stages.FALLBACK_MAIN_MENU.msg()
    keyboard = stages.FALLBACK_MAIN_MENU.kb()

    if isinstance(event, CallbackQuery):
        await event.message.edit_text(text, reply_markup=keyboard)
        await event.answer()
    else:
        await event.answer(text, reply_markup=keyboard)
