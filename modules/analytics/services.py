import io
import time
from datetime import datetime, timedelta

from aiogram.types import CallbackQuery, BufferedInputFile
from aiogram.fsm.context import FSMContext

import plotly.graph_objects as go

from core.callbacks import Callbacks
from core.stage import Stage
from . import states, stages, repositories
from modules.calendar.handlers import start_period_picker
from ..expenses.models import Expense
from ..incomes.models import Income


MAX_MSG_LEN = 3500


async def analytics_menu_handler(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.message.edit_text(
        stages.MENU.msg(),
        reply_markup=stages.MENU.kb(),
    )


async def analytics_stats_handler(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.message.edit_text(
        stages.STATS_MENU.msg(),
        reply_markup=stages.STATS_MENU.kb(),
    )
    await state.set_state(states.AnalyticsStatesGroup.STATS_MENU)


async def analytics_stats_category_pie_start_picker_handler(cb: CallbackQuery, state: FSMContext) -> None:
    await start_period_picker(cb, state, target_state=states.AnalyticsStatesGroup.STATS_CATEGORY_PIE)


async def analytics_stats_category_pie_period_confirm_handler(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    await send_pie_chart_callback(cb, data['date_period']['start'], data['date_period']['end'])
    await cb.message.answer(
        stages.STATS_MENU.msg(),
        reply_markup=stages.STATS_MENU.kb(),
    )
    await state.set_state(states.AnalyticsStatesGroup.STATS_MENU)


async def analytics_stats_income_expense_line_start_picker_handler(cb: CallbackQuery, state: FSMContext) -> None:
    await start_period_picker(cb, state, target_state=states.AnalyticsStatesGroup.STATS_INCOME_EXPENSE_LINE)


async def analytics_stats_income_expense_line_period_confirm_handler(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    await send_income_expense_line_chart_callback(cb, data['date_period']['start'], data['date_period']['end'])
    await cb.message.answer(
        stages.STATS_MENU.msg(),
        reply_markup=stages.STATS_MENU.kb(),
    )
    await state.set_state(states.AnalyticsStatesGroup.STATS_MENU)


async def analytics_stats_summary_period_start_picker_handler(cb: CallbackQuery, state: FSMContext) -> None:
    """
    Запускает процесс выбора периода (дата-репикер).
    """
    await start_period_picker(cb, state, target_state=states.AnalyticsStatesGroup.STATS_SUMMARY)


async def analytics_stats_summary_period_confirm_handler(cb: CallbackQuery, state: FSMContext) -> None:
    """
    Получает выбранный период из состояния и отправляет итоговую информацию.
    """
    data = await state.get_data()
    await state.clear()

    start_date: datetime.date = data.get("date_period", {}).get("start")
    end_date: datetime.date = data.get("date_period", {}).get("end")

    if not start_date or not end_date:
        await cb.message.answer("Пожалуйста, выберите период заново.")
        await cb.answer()
        return

    user_id = cb.from_user.id
    income_total, expense_total = await repositories.get_total_summary(user_id, start_date, end_date)

    balance = income_total - expense_total
    balance_sign = "➕" if balance >= 0 else "➖"
    balance_color = "🟢" if balance >= 0 else "🔴"

    caption = (
        f"<b>📆 Итоги за период</b>\n"
        f"<i>{start_date.strftime('%d.%m.%Y')} – {end_date.strftime('%d.%m.%Y')}</i>\n\n"
        f"🟢 <b>Доходы:</b> {int(income_total)} ₽\n"
        f"🔴 <b>Расходы:</b> {int(expense_total)} ₽\n"
        f"{balance_color} <b>Баланс:</b> {balance_sign} {abs(int(balance))} ₽"
    )

    await cb.message.answer(caption)
    await cb.message.answer(
        stages.STATS_MENU.msg(),
        reply_markup=stages.STATS_MENU.kb(),
    )
    await state.set_state(states.AnalyticsStatesGroup.STATS_MENU)


async def send_pie_chart_callback(
    cb: CallbackQuery,
    start_date,
    end_date
) -> None:
    """
    Получает данные о расходах и доходах пользователя за указанный период,
    генерирует круговые диаграммы и отправляет их по отдельности.
    """
    def create_pie_chart(categories: list[str], amounts: list[float], title: str) -> go.Figure:
        fig = go.Figure(data=[go.Pie(labels=categories, values=amounts, hole=0)])
        fig.update_traces(textinfo='percent+label')
        fig.update_layout(title_text=title)
        return fig

    async def gen_caption(
        category_sums: list[tuple[str, float]],
        total_sum: float,
        start_date: datetime.date,
        end_date: datetime.date,
        is_income: bool
    ) -> str:
        label = "Доходы" if is_income else "Расходы"
        emoji = "🟢" if is_income else "🔴"
        total_emoji = "💰" if is_income else "💸"

        caption = (
            f"<b>📊 {label} по категориям</b>\n"
            f"<i>с {start_date.strftime('%d.%m.%Y')} по {end_date.strftime('%d.%m.%Y')}</i>\n\n"
        )
        for name, amount in category_sums:
            caption += f"• <b>{name}</b>: {int(amount)} ₽\n"
        caption += f"\n<b>{total_emoji} Общая сумма:</b> {int(total_sum)} ₽"
        return caption

    for is_income in (False, True):  # Сначала расходы, потом доходы
        category_sums, total_sum = await repositories.get_category_summary(
            cb.from_user.id, start_date, end_date, is_income=is_income
        )

        if not category_sums:
            await cb.message.answer(
                "Доходов не найдено." if is_income else "Расходов не найдено."
            )
            continue

        categories, amounts = zip(*category_sums)
        fig = create_pie_chart(
            list(categories), list(amounts),
            title="Доходы по категориям" if is_income else "Расходы по категориям"
        )

        buf = io.BytesIO(fig.to_image(format='png'))
        buf.seek(0)
        filename = f"chart_{'income' if is_income else 'expense'}_{int(time.time())}.png"
        photo = BufferedInputFile(buf.read(), filename=filename)
        caption = await gen_caption(category_sums, total_sum, start_date, end_date, is_income)

        await cb.message.answer_photo(photo=photo, caption=caption)

    await cb.answer()


async def send_income_expense_line_chart_callback(
    cb: CallbackQuery,
    start_date,
    end_date
) -> None:
    """
    Получает доходы и расходы пользователя за период, генерирует линейный график и отправляет его.

    Args:
        cb (CallbackQuery): callback-запрос от пользователя Telegram.
        start_date (datetime.date): дата начала периода.
        end_date (datetime.date): дата конца периода.

    Returns:
        None
    """
    def create_income_expense_line_chart(dates: list[str], incomes: list[float], expenses: list[float]) -> go.Figure:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=incomes, mode='lines+markers', name='Доходы', line=dict(color='green')))
        fig.add_trace(go.Scatter(x=dates, y=expenses, mode='lines+markers', name='Расходы', line=dict(color='red')))
        fig.update_layout(title='Доходы и расходы по дням', xaxis_title='Дата', yaxis_title='Сумма, ₽')
        return fig

    income_data, expense_data = await repositories.get_income_and_expense_by_day(cb.from_user.id, start_date, end_date)

    if not income_data and not expense_data:
        await cb.message.answer("За выбранный период данных о доходах и расходах не найдено.")
        await cb.answer()
        return

    # Список всех дат в периоде (чтобы график был ровный)
    all_dates = sorted(set(income_data.keys()) | set(expense_data.keys()))
    dates_str = [d.strftime('%d.%m.%Y') for d in all_dates]
    incomes = [income_data.get(d, 0) for d in all_dates]
    expenses = [expense_data.get(d, 0) for d in all_dates]

    fig = create_income_expense_line_chart(dates_str, incomes, expenses)
    buf = io.BytesIO(fig.to_image(format='png'))
    buf.seek(0)
    filename = f"income_expense_{int(time.time())}.png"
    photo = BufferedInputFile(buf.read(), filename=filename)

    caption = (
        f"<b>📈 Доходы и расходы</b>\n"
        f"<i>с {start_date.strftime('%d.%m.%Y')} по {end_date.strftime('%d.%m.%Y')}</i>"
    )

    await cb.message.answer_photo(photo=photo, caption=caption)
    await cb.answer()


async def analytics_history_handler(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.message.edit_text(
        stages.HISTORY_MENU.msg(),
        reply_markup=stages.HISTORY_MENU.kb(),
    )
    await state.set_state(states.AnalyticsStatesGroup.HISTORY_MENU)


async def analytics_history_period_handler(cb: CallbackQuery, state: FSMContext) -> None:
    if cb.data == Callbacks.ANALYTICS.HISTORY.PERIOD:
        await start_period_picker(cb, state, target_state=states.AnalyticsStatesGroup.HISTORY_PERIOD)
    else:
        start_date = datetime.now() - timedelta(
            days=1) if cb.data == Callbacks.ANALYTICS.HISTORY.LAST_DAY else datetime.now() - timedelta(days=7)
        end_date = datetime.now()
        await show_operations_history(cb, cb.from_user.id, start_date, end_date)
        await state.set_state(states.AnalyticsStatesGroup.HISTORY_MENU)


async def analytics_history_period_confirm_handler(cb: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    await state.clear()

    start_date: datetime = data.get("date_period", {}).get("start")
    end_date: datetime = data.get("date_period", {}).get("end")

    await show_operations_history(cb, cb.from_user.id, start_date, end_date)
    await state.set_state(states.AnalyticsStatesGroup.HISTORY_MENU)


async def show_operations_history(
    cb: CallbackQuery,
    user_id: int,
    start_date: datetime,
    end_date: datetime
) -> None:
    operations = await repositories.get_incomes_expenses_for_period(
        user_id,
        start_date,
        end_date
    )

    history_messages = await format_operations_history(operations, start_date, end_date)
    for idx, msg in enumerate(history_messages):
        if idx == 0:
            await cb.message.answer(msg, parse_mode="HTML")
        else:
            await cb.message.answer(msg, parse_mode="HTML")

    await cb.message.answer(
        "Укажите период:",
        reply_markup=stages.HISTORY_MENU.kb()
    )


async def format_operations_history(
    operations: tuple[list[Income], list[Expense]],
    start_date: datetime,
    end_date: datetime
) -> list[str]:
    incomes, expenses = operations

    all_ops = sorted([*incomes, *expenses], key=lambda x: x.date, reverse=True)
    actual_start = min((op.date for op in all_ops), default=start_date)
    actual_end = max((op.date for op in all_ops), default=end_date)

    def format_income(income: Income) -> str:
        category = getattr(getattr(income, 'category', None), 'name', 'Без категории')
        date_str = income.date.strftime('%d.%m.%Y %H:%M')
        comment = f"\n<i>📝 {income.comment}</i>" if income.comment else ""

        return (
            f"<b>💰 +{income.amount} ₽</b>  <u>{category}</u>\n"
            f"<b>📅</b> <code>{date_str}</code>{comment}\n"
        )

    def format_expense(expense: Expense) -> str:
        category = getattr(getattr(expense, 'category', None), 'name', 'Без категории')
        date_str = expense.date.strftime('%d.%m.%Y %H:%M')
        comment = f"\n<i>📝 {expense.comment}</i>" if expense.comment else ""

        return (
            f"<b>🔻 -{expense.amount} ₽</b>  <u>{category}</u>\n"
            f"<b>📅</b> <code>{date_str}</code>{comment}\n"
        )

    total_income = sum(income.amount for income in incomes)
    total_expense = sum(exp.amount for exp in expenses)
    balance = total_income - total_expense

    header = [
        "📊 <b>История операций</b>",
        f"📅 Период: <code>{actual_start.strftime('%d.%m.%Y')}</code> — <code>{actual_end.strftime('%d.%m.%Y')}</code>",
        "━━━━━━━━━━━━━━━━━━",
    ]

    # Начинаем с заголовка и доходов
    message_chunks: list[str] = []
    current_message = "\n".join(header)

    # Добавляем блок доходов
    income_header = f"📈 <b>Доходы ({len(incomes)})</b>" if incomes else "📈 <b>Доходов нет</b>"
    income_lines = [income_header]
    if incomes:
        for income in incomes:
            income_lines.append(format_income(income))

    # Добавляем доходы построчно
    for line in income_lines + ["─────────────"]:
        if len(current_message) + len(line) + 1 > MAX_MSG_LEN:
            message_chunks.append(current_message)
            current_message = ""
        current_message += f"\n{line}"

    # Расходы
    expense_header = f"📉 <b>Расходы ({len(expenses)})</b>" if expenses else "📉 <b>Расходов нет</b>"
    expense_lines = [expense_header]
    if expenses:
        for expense in expenses:
            expense_lines.append(format_expense(expense))

    for line in expense_lines + ["─────────────"]:
        if len(current_message) + len(line) + 1 > MAX_MSG_LEN:
            message_chunks.append(current_message)
            current_message = ""
        current_message += f"\n{line}"

    # Итоговый блок
    footer_lines = [
        f"💵 <b>Итого доходы:</b> <b>+{total_income} ₽</b>" if incomes else "",
        f"💸 <b>Итого расходы:</b> <b>-{total_expense} ₽</b>" if expenses else "",
        f"🧮 <b>Баланс:</b> <b>{'+' if balance >= 0 else ''}{balance} ₽</b>",
        f"📌 <b>Всего операций:</b> <b>{len(incomes) + len(expenses)}</b>",
    ]

    for line in filter(None, footer_lines):
        if len(current_message) + len(line) + 1 > MAX_MSG_LEN:
            message_chunks.append(current_message)
            current_message = ""
        current_message += f"\n{line}"

    if current_message.strip():
        message_chunks.append(current_message)

    return message_chunks
