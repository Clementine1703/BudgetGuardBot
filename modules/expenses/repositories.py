from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db_session
from modules.main.models import User
from .models import ExpenseCategory, Expense


@db_session
async def create_category(session: AsyncSession, user_tg_id: int, name: str) -> None:
    """
    Создаёт новую категорию расходов для пользователя.

    Args:
        session (AsyncSession): асинхронная сессия базы данных.
        user_tg_id (int): Telegram ID пользователя.
        name (str): название новой категории расходов.

    Raises:
        ValueError: если пользователь с указанным Telegram ID не найден.

    Returns:
        None
    """
    result = await session.execute(
        select(User.id).where(User.tg_id == user_tg_id)
    )
    user_id = result.scalar_one_or_none()

    if user_id is None:
        raise ValueError("Пользователь с таким tg_id не найден")

    session.add(ExpenseCategory(user_id=user_id, name=name))
    await session.commit()


@db_session
async def delete_category(session: AsyncSession, user_tg_id: int, category_id: int) -> None:
    """
    Удаляет категорию расходов, если она принадлежит пользователю.

    Args:
        session (AsyncSession): асинхронная сессия базы данных.
        user_tg_id (int): Telegram ID пользователя.
        category_id (int): ID категории расходов.

    Raises:
        ValueError: если пользователь или категория не найдены.

    Returns:
        None
    """
    user = await session.execute(select(User).where(User.tg_id == user_tg_id))
    user = user.scalar_one_or_none()
    if user is None:
        raise ValueError("Пользователь с таким tg_id не найден")

    category = await session.get(ExpenseCategory, category_id)
    if category is None or category.user_id != user.id:
        raise ValueError("Категория не найдена или не принадлежит пользователю")

    await session.delete(category)
    await session.commit()


@db_session
async def get_all_categories(session: AsyncSession, user_tg_id: int) -> List[ExpenseCategory]:
    """
    Получает список всех категорий расходов пользователя.

    Args:
        session (AsyncSession): асинхронная сессия базы данных.
        user_tg_id (int): Telegram ID пользователя.

    Returns:
        List[ExpenseCategory]: список объектов категорий расходов пользователя.
    """
    stmt = select(ExpenseCategory).join(User, ExpenseCategory.user_id == User.id).where(User.tg_id == user_tg_id)
    result = await session.execute(stmt)
    return list(result.scalars().all())


@db_session
async def create_expense(session: AsyncSession, data: dict) -> None:
    """
    Создаёт запись о расходе с переданными данными.

    Args:
        session (AsyncSession): асинхронная сессия базы данных.
        data (dict): словарь с данными расхода, ключи соответствуют полям модели Expense.

    Returns:
        None
    """
    session.add(Expense(**data))
    await session.commit()
