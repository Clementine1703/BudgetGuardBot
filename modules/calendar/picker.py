from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import StatesGroup, State
from datetime import datetime, timedelta
from core.callbacks import Callbacks
import calendar


class DatePeriodStates(StatesGroup):
    SELECTING = State()


class DatePeriodPicker:
    def __init__(self):
        self.cb = Callbacks.PERIOD_PICKER.PREFIX

    def get_keyboard(self, year: int, month: int, selected_start=None, selected_end=None) -> InlineKeyboardMarkup:
        inline_keyboard = []

        month_name = calendar.month_name[month]
        inline_keyboard.append([
            InlineKeyboardButton(text=f"{month_name} {year}", callback_data="ignore")
        ])

        # Заголовок с днями недели
        inline_keyboard.append([
            InlineKeyboardButton(text=day, callback_data="ignore")
            for day in ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        ])

        # Календарь месяца
        month_days = calendar.monthcalendar(year, month)
        for week in month_days:
            row = []
            for day in week:
                if day == 0:
                    row.append(InlineKeyboardButton(text=" ", callback_data="ignore"))
                else:
                    date_obj = datetime(year, month, day).date()
                    if selected_start == date_obj:
                        text = f"🔹{day}"
                    elif selected_end == date_obj:
                        text = f"🔸{day}"
                    else:
                        text = str(day)

                    row.append(InlineKeyboardButton(
                        text=text,
                        callback_data=f"{Callbacks.PERIOD_PICKER.SELECT}:{date_obj.isoformat()}"
                    ))
            inline_keyboard.append(row)

        prev_month = datetime(year, month, 1) - timedelta(days=1)
        next_month = datetime(year, month, 28) + timedelta(days=4)
        next_month = datetime(next_month.year, next_month.month, 1)

        inline_keyboard.append([
            InlineKeyboardButton(text="⬅️", callback_data=f"{Callbacks.PERIOD_PICKER.NAV}:{prev_month.year}:{prev_month.month}"),
            InlineKeyboardButton(text="📅 месяц/год", callback_data=Callbacks.PERIOD_PICKER.PICK_MONTH_YEAR),
            InlineKeyboardButton(text="➡️", callback_data=f"{Callbacks.PERIOD_PICKER.NAV}:{next_month.year}:{next_month.month}")
        ])

        inline_keyboard.append([
            InlineKeyboardButton(text="🔄 Сброс", callback_data=Callbacks.PERIOD_PICKER.RESET),
            InlineKeyboardButton(text="✅ Готово", callback_data=Callbacks.PERIOD_PICKER.CONFIRM)
        ])

        return InlineKeyboardMarkup(inline_keyboard=inline_keyboard, row_width=7)

    def get_year_month_selector(self, current_year: int) -> InlineKeyboardMarkup:
        inline_keyboard = []

        # Годы (5 кнопок)
        years_range = range(current_year - 2, current_year + 3)
        year_buttons = [InlineKeyboardButton(
            text=str(y),
            callback_data=f"{Callbacks.PERIOD_PICKER.YEAR}:{y}"
        ) for y in years_range]
        for i in range(0, len(year_buttons), 3):
            inline_keyboard.append(year_buttons[i:i + 3])

        # Месяцы (по 4 в ряд)
        month_buttons = [
            InlineKeyboardButton(
                text=calendar.month_name[m],
                callback_data=f"{Callbacks.PERIOD_PICKER.MONTH}:{m}"
            ) for m in range(1, 13)
        ]
        for i in range(0, 12, 4):
            inline_keyboard.append(month_buttons[i:i + 4])

        inline_keyboard.append([
            InlineKeyboardButton(text="◀️ Назад к календарю", callback_data=Callbacks.PERIOD_PICKER.BACK_TO_CALENDAR)
        ])

        return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
