from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db_session
from modules.main.models import User
from .models import IncomeCategory, Income


@db_session
async def create_category(session: AsyncSession, user_tg_id: int, name: str) -> None:
    result = await session.execute(
        select(User.id).where(User.tg_id == user_tg_id)
    )
    user_id = result.scalar_one_or_none()

    if user_id is None:
        raise ValueError("Пользователь с таким tg_id не найден")

    session.add(IncomeCategory(user_id=user_id, name=name))
    await session.commit()


@db_session
async def delete_category(session: AsyncSession, user_tg_id: int, category_id: int) -> None:
    """
    Удаляет категорию доходов, если она принадлежит пользователю.

    Args:
        session (AsyncSession): асинхронная сессия базы данных.
        user_tg_id (int): Telegram ID пользователя.
        category_id (int): ID категории доходов.

    Raises:
        ValueError: если пользователь или категория не найдены.

    Returns:
        None
    """
    user = await session.execute(select(User).where(User.tg_id == user_tg_id))
    user = user.scalar_one_or_none()
    if user is None:
        raise ValueError("Пользователь с таким tg_id не найден")

    category = await session.get(IncomeCategory, category_id)
    if category is None or category.user_id != user.id:
        raise ValueError("Категория не найдена или не принадлежит пользователю")

    await session.delete(category)
    await session.commit()


@db_session
async def get_all_categories(session: AsyncSession, user_tg_id: int) -> List[IncomeCategory]:
    stmt = select(IncomeCategory).join(User, IncomeCategory.user_id == User.id).where(User.tg_id == user_tg_id)
    result = await session.execute(stmt)
    return list(result.scalars().all())


@db_session
async def create_income(session: AsyncSession, data: dict) -> None:
   session.add(Income(**data))
   await session.commit()
