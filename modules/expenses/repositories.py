from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db_session
from modules.main.models import User
from .models import ExpenseCategory, Expense


@db_session
async def create_category(session: AsyncSession, user_tg_id: int, name: str) -> None:
    result = await session.execute(
        select(User.id).where(User.tg_id == user_tg_id)
    )
    user_id = result.scalar_one_or_none()

    if user_id is None:
        raise ValueError("Пользователь с таким tg_id не найден")

    session.add(ExpenseCategory(user_id=user_id, name=name))
    await session.commit()


@db_session
async def get_all_categories(session: AsyncSession, user_tg_id: int) -> List[ExpenseCategory]:
    stmt = select(ExpenseCategory).join(User, ExpenseCategory.user_id == User.id).where(User.tg_id == user_tg_id)
    result = await session.execute(stmt)
    return list(result.scalars().all())


@db_session
async def create_expense(session: AsyncSession, data: dict) -> None:
   session.add(Expense(**data))
   await session.commit()
