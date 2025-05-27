from enum import Enum


class CallbackNamespace(Enum):
    MAIN = "main"
    EXPENSE = "expense"
    INCOME = "income"
    ANALYTICS = "analytics"
    BUDGET = "budget"
    CATEGORY = "category"
    REMINDER = "reminder"
    SETTINGS = "settings"
    EXPORT = "export"

    PICKER = "picker"


class Callbacks:
    """Централизованное хранилище всех callback-действий бота"""

    # ===== COMMON =====
    MAIN_MENU = f"{CallbackNamespace.MAIN.value}:menu"
    BACK = f"{CallbackNamespace.MAIN.value}:back"
    SKIP = f"{CallbackNamespace.MAIN.value}:skip"

    # ===== EXPENSE =====
    class EXPENSE:
        PREFIX = CallbackNamespace.EXPENSE.value
        SELECT_CATEGORY = f"{PREFIX}:select_category"
        CREATE_CATEGORY = f"{PREFIX}:create_category"
        ADD_AMOUNT = f"{PREFIX}:add_amount"
        ADD_COMMENT = f"{PREFIX}:add_comment"

    # ===== INCOME =====
    class INCOME:
        PREFIX = CallbackNamespace.EXPENSE.value
        SELECT_CATEGORY = f"{PREFIX}:select_category"
        CREATE_CATEGORY = f"{PREFIX}:create_category"
        ADD_AMOUNT = f"{PREFIX}:add_amount"
        ADD_COMMENT = f"{PREFIX}:add_comment"
        ADD_DATE = f"{PREFIX}:add_date"

    # ===== ANALYTICS =====
    class ANALYTICS:
        PREFIX = CallbackNamespace.ANALYTICS.value
        MENU = f"{PREFIX}:menu"
        class STATS:
            PREFIX = f"{CallbackNamespace.ANALYTICS.value}:stats"
            MENU = PREFIX
            CATEGORY_PIE = f"{PREFIX}:category_pie"
            GRAPH = f"{PREFIX}:graph"
            SUMMARY = f"{PREFIX}:summary"
            AVERAGE = f"{PREFIX}:average"
            TOP_RECORDS = f"{PREFIX}:top_records"

        HISTORY = f"{PREFIX}:history"
        PERIOD = f"{PREFIX}:period"
        CATEGORY = f"{PREFIX}:category"

    # ===== BUDGET =====
    class BUDGET:
        MENU = f"{CallbackNamespace.BUDGET.value}:menu"
        ADD_LIMIT = f"{CallbackNamespace.BUDGET.value}:add_limit"
        EDIT_LIMIT = f"{CallbackNamespace.BUDGET.value}:edit_limit"
        SHOW_LIMITS = f"{CallbackNamespace.BUDGET.value}:show_limits"

    # ===== CATEGORY MANAGEMENT =====
    class CATEGORY:
        MENU = f"{CallbackNamespace.CATEGORY.value}:menu"
        MANAGE_EXPENSE = f"{CallbackNamespace.CATEGORY.value}:manage_exp"
        MANAGE_INCOME = f"{CallbackNamespace.CATEGORY.value}:manage_inc"
        AUTO_TAGS = f"{CallbackNamespace.CATEGORY.value}:auto_tags"
        CURRENCY = f"{CallbackNamespace.CATEGORY.value}:currency"

    # ===== REMINDERS =====
    class REMINDER:
        MENU = f"{CallbackNamespace.REMINDER.value}:menu"
        CREATE = f"{CallbackNamespace.REMINDER.value}:create"
        LIST = f"{CallbackNamespace.REMINDER.value}:list"
        EDIT_SCHEDULE = f"{CallbackNamespace.REMINDER.value}:edit_schedule"
        DISABLE_ALL = f"{CallbackNamespace.REMINDER.value}:disable_all"

    # ===== SETTINGS =====
    class SETTINGS:
        MENU = f"{CallbackNamespace.SETTINGS.value}:menu"
        LANGUAGE = f"{CallbackNamespace.SETTINGS.value}:language"
        CURRENCY = f"{CallbackNamespace.SETTINGS.value}:currency"
        TIMEZONE = f"{CallbackNamespace.SETTINGS.value}:timezone"
        SECURITY = f"{CallbackNamespace.SETTINGS.value}:security"
        WIPE_DATA = f"{CallbackNamespace.SETTINGS.value}:wipe_data"

    # ===== EXPORT/IMPORT =====
    class EXPORT:
        MENU = f"{CallbackNamespace.EXPORT.value}:menu"
        DATA = f"{CallbackNamespace.EXPORT.value}:data"
        SEND_EMAIL = f"{CallbackNamespace.EXPORT.value}:send_email"
        CSV_EXCEL = f"{CallbackNamespace.EXPORT.value}:csv_excel"
        IMPORT_DATA = f"{CallbackNamespace.EXPORT.value}:import"

    # ===== PERIOD_PICKER =====
    class PERIOD_PICKER:
        PREFIX = f"{CallbackNamespace.PICKER.value}:period_picker"
        NAV = f"{PREFIX}:nav"
        SELECT = f"{PREFIX}:select"
        RESET = f"{PREFIX}:reset"
        CONFIRM = f"{PREFIX}:confirm"
        PICK_MONTH_YEAR = f"{PREFIX}:pick_month_year"
        YEAR = f"{PREFIX}:year"
        MONTH = f"{PREFIX}:month"
        BACK_TO_CALENDAR = f"{PREFIX}:back_to_calendar"
