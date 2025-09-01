from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from app.config import settings
from sqlmodel import SQLModel

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True
)


async def init_db():
    async with engine.begin() as conn:
        from app.models.user_model import User,Transaction
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    async with async_session() as session:
        yield session