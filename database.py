from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from utils import get_db_url


engine = create_async_engine(get_db_url(), echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def db_session(func):
        async def wrapper():
            async with async_session() as session:
                return await func(session)
        return wrapper

Base = declarative_base()