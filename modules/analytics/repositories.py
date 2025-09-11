from datetime import date

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.database import db_session
from modules.expenses.models import Expense, ExpenseCategory
from modules.incomes.models import IncomeCategory, Income
from modules.main.models import User


@db_session
async def get_category_summary(
    session: AsyncSession,
    user_tg_id: int,
    start_date: date,
    end_date: date,
    is_income: bool,
) -> tuple[list[tuple[str, float]], float]:
    """
    Универсальный метод: возвращает суммы по категориям для доходов или расходов.
    """
    category_model = IncomeCategory if is_income else ExpenseCategory
    record_model = Income if is_income else Expense

    stmt = (
        select(category_model.name, func.sum(record_model.amount))
        .join(record_model, record_model.category_id == category_model.id)
        .join(User, category_model.user_id == User.id)
        .where(
            and_(
                User.tg_id == user_tg_id,
                record_model.date >= start_date,
                record_model.date <= end_date,
            )
        )
        .group_by(category_model.name)
    )

    result = await session.execute(stmt)
    category_sums = [(name, amount or 0.0) for name, amount in result.all()]

    total_stmt = (
        select(func.sum(record_model.amount))
        .join(category_model, record_model.category_id == category_model.id)
        .join(User, category_model.user_id == User.id)
        .where(
            and_(
                User.tg_id == user_tg_id,
                record_model.date >= start_date,
                record_model.date <= end_date,
            )
        )
    )
    total_result = await session.execute(total_stmt)
    total_sum = total_result.scalar() or 0.0

    return category_sums, total_sum


@db_session
async def get_income_and_expense_by_day(
    session: AsyncSession,
    user_tg_id: int,
    start_date: date,
    end_date: date
) -> tuple[dict[date, float], dict[date, float]]:
    """
    Получить доходы и расходы пользователя сгруппированные по дате за указанный период.

    Returns два словаря:
        - доходы: {дата: сумма}
        - расходы: {дата: сумма}
    """
    # Доходы по дням
    income_stmt = (
        select(
            func.date_trunc('day', Income.date).label('day'),
            func.sum(Income.amount).label('sum')
        )
        .join(IncomeCategory, Income.category_id == IncomeCategory.id)
        .join(User, IncomeCategory.user_id == User.id)
        .where(
            and_(
                User.tg_id == user_tg_id,
                Income.date >= start_date,
                Income.date <= end_date,
            )
        )
        .group_by('day')
        .order_by('day')
    )
    income_result = await session.execute(income_stmt)
    income_by_day = {row.day.date(): row.sum or 0 for row in income_result}

    # Расходы по дням
    expense_stmt = (
        select(
            func.date_trunc('day', Expense.date).label('day'),
            func.sum(Expense.amount).label('sum')
        )
        .join(ExpenseCategory, Expense.category_id == ExpenseCategory.id)
        .join(User, ExpenseCategory.user_id == User.id)
        .where(
            and_(
                User.tg_id == user_tg_id,
                Expense.date >= start_date,
                Expense.date <= end_date,
            )
        )
        .group_by('day')
        .order_by('day')
    )
    expense_result = await session.execute(expense_stmt)
    expense_by_day = {row.day.date(): row.sum or 0 for row in expense_result}

    return income_by_day, expense_by_day


@db_session
async def get_total_summary(
    session: AsyncSession,
    user_tg_id: int,
    start_date: date,
    end_date: date,
) -> tuple[float, float]:
    """
    Возвращает общие суммы доходов и расходов пользователя за указанный период.

    Связь с пользователем происходит через категорию, т.к. user_id есть только у категории.
    """

    income_stmt = (
        select(func.sum(Income.amount))
        .join(IncomeCategory, Income.category_id == IncomeCategory.id)
        .join(User, IncomeCategory.user_id == User.id)
        .where(
            and_(
                User.tg_id == user_tg_id,
                Income.date >= start_date,
                Income.date <= end_date,
            )
        )
    )
    income_result = await session.execute(income_stmt)
    income_total = income_result.scalar() or 0.0

    expense_stmt = (
        select(func.sum(Expense.amount))
        .join(ExpenseCategory, Expense.category_id == ExpenseCategory.id)
        .join(User, ExpenseCategory.user_id == User.id)
        .where(
            and_(
                User.tg_id == user_tg_id,
                Expense.date >= start_date,
                Expense.date <= end_date,
            )
        )
    )
    expense_result = await session.execute(expense_stmt)
    expense_total = expense_result.scalar() or 0.0

    return income_total, expense_total


@db_session
async def get_incomes_expenses_for_period(
        session: AsyncSession,
        user_tg_id: int,
        start_date:date,
        end_date:date
):
    income_stmt = (
        select(Income)
        .options(selectinload(Income.category))
        .join(IncomeCategory, Income.category_id == IncomeCategory.id)
        .join(User, IncomeCategory.user_id == User.id)
        .where(
            and_(
                User.tg_id == user_tg_id,
                Income.date >= start_date,
                Income.date <= end_date,
            )
        )
    )
    print("Income query:", income_stmt.compile(compile_kwargs={"literal_binds": True}))
    income_result = await session.execute(income_stmt)
    incomes = income_result.scalars().all()

    expense_stmt = (
        select(Expense)
        .options(selectinload(Expense.category))
        .join(ExpenseCategory, Expense.category_id == ExpenseCategory.id)
        .join(User, ExpenseCategory.user_id == User.id)
        .where(
            and_(
                User.tg_id == user_tg_id,
                Expense.date >= start_date,
                Expense.date <= end_date,
            )
        )
    )
    print("Expense query:", expense_stmt.compile(compile_kwargs={"literal_binds": True}))
    expense_result = await session.execute(expense_stmt)
    expenses = expense_result.scalars().all()

    return incomes, expenses
