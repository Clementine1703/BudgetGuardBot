from aiogram.fsm.state import StatesGroup, State


class AddIncome(StatesGroup):
    select_category = State()
    create_category = State()
    input_new_category = State()
    input_amount = State()
    input_comment = State()
