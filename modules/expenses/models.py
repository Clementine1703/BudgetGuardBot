from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from core.database import Base


class ExpenseCategory(Base):
    __tablename__ = 'expense_category'

    id = Column(Integer, primary_key=True)

    name = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey("tg_user.id"), nullable=False)


class Expense(Base):
    __tablename__ = 'expense'

    id = Column(Integer, primary_key=True)

    category_id = Column(Integer, ForeignKey("expense_category.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    comment = Column(String, nullable=True)
    date = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
