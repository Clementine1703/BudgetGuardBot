from aiogram.types import CallbackQuery
from datetime import date
from typing import Callable, Awaitable, Dict

PeriodCallback = Callable[[CallbackQuery, date, date], Awaitable[None]]
PERIOD_CALLBACKS: Dict[str, PeriodCallback] = {}

def register_period_callback(name: str):
    def wrapper(func: PeriodCallback):
        PERIOD_CALLBACKS[name] = func
        return func
    return wrapper
