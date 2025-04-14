from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from database import Base


class User(Base):
    __tablename__ = 'tg_user'

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, unique=True)
