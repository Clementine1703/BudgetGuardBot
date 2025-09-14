from aiogram.fsm.state import StatesGroup, State


class AddExpense(StatesGroup):
    category = State()
    amount = State()
    comment = State()
    date = State()


class AddIncome(StatesGroup):
    category = State()
    amount = State()
    comment = State()
    date = State()


class Analytics(StatesGroup):
    menu = State()
    day = State()
    week = State()
    month = State()
    custom_period = State()
    by_category = State()
    compare_income_expense = State()


class BudgetPlan(StatesGroup):
    menu = State()
    add_limit = State()
    edit_limit = State()
    view_limits = State()


class CategoryManager(StatesGroup):
    menu = State()

    # Расходы
    manage_expense = State()
    create_expense = State()
    rename_expense = State()
    delete_expense = State()

    # Доходы
    manage_income = State()
    create_income = State()
    rename_income = State()
    delete_income = State()

    # Прочее
    auto_tag_settings = State()
    currency_settings = State()


class Reminders(StatesGroup):
    menu = State()
    create = State()
    list_all = State()
    edit_schedule = State()
    disable_all = State()


class Settings(StatesGroup):
    menu = State()
    set_language = State()
    set_currency = State()
    set_timezone = State()
    security_settings = State()
    confirm_wipe = State()


class ExportImport(StatesGroup):
    menu = State()
    export_data = State()
    send_email = State()
    export_csv = State()
    import_data = State()