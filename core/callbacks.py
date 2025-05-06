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


class Callbacks:
    """Централизованное хранилище всех callback-действий бота"""

    # ===== COMMON =====
    MAIN_MENU = f"{CallbackNamespace.MAIN.value}:menu"
    BACK = f"{CallbackNamespace.MAIN.value}:back"
    SKIP = f"{CallbackNamespace.MAIN.value}:skip"

    # ===== EXPENSE =====
    class EXPENSE:
        SELECT_CATEGORY = f"{CallbackNamespace.EXPENSE.value}:select_category"
        CREATE_CATEGORY = f"{CallbackNamespace.EXPENSE.value}:create_category"
        ADD_AMOUNT = f"{CallbackNamespace.EXPENSE.value}:add_amount"
        ADD_COMMENT = f"{CallbackNamespace.EXPENSE.value}:add_comment"

    # ===== INCOME =====
    class INCOME:
        SELECT_CATEGORY = f"{CallbackNamespace.INCOME.value}:SELECT_category"
        CREATE_CATEGORY = f"{CallbackNamespace.INCOME.value}:create_category"
        ADD_AMOUNT = f"{CallbackNamespace.INCOME.value}:add_amount"
        ADD_COMMENT = f"{CallbackNamespace.INCOME.value}:add_comment"
        ADD_DATE = f"{CallbackNamespace.INCOME.value}:add_date"

    # ===== ANALYTICS =====
    class ANALYTICS:
        MENU = f"{CallbackNamespace.ANALYTICS.value}:menu"
        DAY_STATS = f"{CallbackNamespace.ANALYTICS.value}:day"
        WEEK_STATS = f"{CallbackNamespace.ANALYTICS.value}:week"
        MONTH_STATS = f"{CallbackNamespace.ANALYTICS.value}:month"
        CUSTOM_PERIOD = f"{CallbackNamespace.ANALYTICS.value}:custom"
        CATEGORY_STATS = f"{CallbackNamespace.ANALYTICS.value}:by_category"
        COMPARE = f"{CallbackNamespace.ANALYTICS.value}:compare"

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
