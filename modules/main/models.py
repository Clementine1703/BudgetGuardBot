from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from core.database import Base


class User(Base):
    __tablename__ = 'tg_user'

    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger(), unique=True)
