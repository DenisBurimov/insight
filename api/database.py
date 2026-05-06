from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import config

_async_session_local = None


def _make_async_url(url: str) -> str:
    if url.startswith("sqlite:///"):
        return url.replace("sqlite:///", "sqlite+aiosqlite:///", 1)
    if url.startswith("postgresql+psycopg2://"):
        return url.replace("postgresql+psycopg2://", "postgresql+asyncpg://", 1)
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    return url


def _get_session_local() -> async_sessionmaker[AsyncSession]:
    global _async_session_local
    if _async_session_local is None:
        CFG = config()
        engine = create_async_engine(_make_async_url(CFG.SQLALCHEMY_DATABASE_URI))
        _async_session_local = async_sessionmaker(engine, expire_on_commit=False)
    return _async_session_local


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with _get_session_local()() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
