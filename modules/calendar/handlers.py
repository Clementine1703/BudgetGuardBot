from aiogram.types import CallbackQuery
from aiogram.fsm.state import State
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from datetime import datetime
from core.callbacks import Callbacks

from modules.calendar.picker import DatePeriodPicker, DatePeriodStates
from modules.calendar.stages import DATE_CONFIRM


router = Router()
picker = DatePeriodPicker()

async def start_period_picker(
    callback: CallbackQuery,
    state: FSMContext,
    *,
    target_state: State,
    target_key: str = "date_period"
):
    today = datetime.today()
    await state.set_state(DatePeriodStates.SELECTING)
    await state.update_data(
        year=today.year,
        month=today.month,
        start=None,
        end=None,
        target_state=target_state.state,
        target_key=target_key
    )
    await callback.message.edit_text(
        "Выберите период:",
        reply_markup=picker.get_keyboard(today.year, today.month)
    )


@router.callback_query(F.data.startswith(Callbacks.PERIOD_PICKER.NAV))
async def nav_month(callback: CallbackQuery, state: FSMContext):
    # Пример: "picker:period_picker:nav:2025:6"
    parts = callback.data.split(":")
    year, month = int(parts[3]), int(parts[4])

    data = await state.get_data()
    selected_start = data.get("start")
    selected_end = data.get("end")

    await state.update_data(year=year, month=month)

    await callback.message.edit_reply_markup(
        reply_markup=picker.get_keyboard(year, month, selected_start, selected_end)
    )
    await callback.answer()


@router.callback_query(F.data.startswith(Callbacks.PERIOD_PICKER.SELECT + ":"))
async def select_day(callback: CallbackQuery, state: FSMContext):
    # Пример: "picker:period_picker:select:2024-05-01"
    parts = callback.data.split(":")
    date_str = parts[-1]
    date = datetime.fromisoformat(date_str).date()
    data = await state.get_data()

    start = data.get("start")
    end = data.get("end")

    if start is None or (start and end):
        await state.update_data(start=date, end=None)
    elif start and date < start:
        await state.update_data(start=date, end=None)
    else:
        await state.update_data(end=date)

    new_data = await state.get_data()
    await state.update_data(year=date.year, month=date.month)
    await callback.message.edit_reply_markup(
        reply_markup=picker.get_keyboard(date.year, date.month, new_data.get("start"), new_data.get("end"))
    )
    await callback.answer()


@router.callback_query(F.data == Callbacks.PERIOD_PICKER.RESET)
async def reset_selection(callback: CallbackQuery, state: FSMContext):
    today = datetime.today()
    await state.update_data(start=None, end=None, year=today.year, month=today.month)
    await callback.message.edit_reply_markup(
        reply_markup=picker.get_keyboard(today.year, today.month)
    )
    await callback.answer("Сброшено")


@router.callback_query(F.data == Callbacks.PERIOD_PICKER.CONFIRM)
async def confirm_selection(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    start = data.get("start")
    end = data.get("end") or start

    if not start:
        await callback.answer("Выберите хотя бы одну дату", show_alert=True)
        return

    target_state = data.get("target_state")
    target_key = data.get("target_key", "period")

    if target_state:
        await state.set_state(target_state)

    await state.update_data(**{target_key: {"start": start, "end": end}})
    await callback.message.edit_text(
        text=f"Выбранный период: с {start.strftime('%d.%m.%Y')} по {end.strftime('%d.%m.%Y')}",
        reply_markup=DATE_CONFIRM.kb()
    )
    await callback.answer()


@router.callback_query(F.data == Callbacks.PERIOD_PICKER.PICK_MONTH_YEAR)
async def pick_month_year(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    year = data.get("year", datetime.today().year)
    await callback.message.edit_reply_markup(reply_markup=picker.get_year_month_selector(year))
    await callback.answer()


@router.callback_query(F.data.startswith(Callbacks.PERIOD_PICKER.YEAR))
async def select_year(callback: CallbackQuery, state: FSMContext):
    # Пример: "picker:period_picker:year:2025"
    parts = callback.data.split(":")
    year = int(parts[-1])
    await state.update_data(year=year)
    await callback.message.edit_reply_markup(reply_markup=picker.get_year_month_selector(year))
    await callback.answer()


@router.callback_query(F.data.startswith(Callbacks.PERIOD_PICKER.MONTH))
async def select_month(callback: CallbackQuery, state: FSMContext):
    # Пример: "picker:period_picker:month:5"
    parts = callback.data.split(":")
    month = int(parts[-1])
    data = await state.get_data()
    year = data.get("year", datetime.today().year)
    await state.update_data(year=year, month=month)

    selected_start = data.get("start")
    selected_end = data.get("end")

    await callback.message.edit_text("Выберите период:")
    await callback.message.edit_reply_markup(
        reply_markup=picker.get_keyboard(year, month, selected_start, selected_end)
    )
    await callback.answer()


@router.callback_query(F.data == Callbacks.PERIOD_PICKER.BACK_TO_CALENDAR)
async def back_to_calendar(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    year = data.get("year", datetime.today().year)
    month = data.get("month", datetime.today().month)
    selected_start = data.get("start")
    selected_end = data.get("end")

    await callback.message.edit_text("Выберите период:")
    await callback.message.edit_reply_markup(
        reply_markup=picker.get_keyboard(year, month, selected_start, selected_end)
    )
    await callback.answer()
