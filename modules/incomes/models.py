from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from core.database import Base


class IncomeCategory(Base):
    __tablename__ = 'income_category'

    id = Column(Integer, primary_key=True)

    name = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey("tg_user.id"), nullable=False)

    incomes = relationship("Income", back_populates="category")


class Income(Base):
    __tablename__ = 'income'

    id = Column(Integer, primary_key=True)

    category_id = Column(Integer, ForeignKey("income_category.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    comment = Column(String, nullable=True)
    date = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    category = relationship("IncomeCategory", back_populates="incomes")
