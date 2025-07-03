from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.config import DB_URL

async_engine = create_async_engine(
    url=DB_URL,
    echo=True,
    pool_size=10,
    max_overflow=20,
)

session_factory = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


async def session_getter() -> AsyncSession:
    async with session_factory() as session:
        yield session


class Base(DeclarativeBase):
    metadata = MetaData()