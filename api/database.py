import asyncio
import os
from collections.abc import AsyncGenerator
from urllib.parse import urlparse

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import config

_async_session_local = None
_cloud_sql_connector = None
_connector_lock = asyncio.Lock()


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
        url = _make_async_url(CFG.SQLALCHEMY_DATABASE_URI)
        instance = getattr(CFG, "CLOUD_SQL_INSTANCE", "")
        pgbouncer_host = os.environ.get("PGBOUNCER_HOST", "")

        if pgbouncer_host and url.startswith("postgresql"):
            # Route through PgBouncer; skip the Cloud SQL connector.
            # PgBouncer + Cloud SQL Proxy handle auth and real connection pooling.
            parsed = urlparse(CFG.SQLALCHEMY_DATABASE_URI)
            bouncer_url = parsed._replace(
                scheme="postgresql+asyncpg",
                netloc=f"{parsed.username}:{parsed.password}@{pgbouncer_host}:5432",
            ).geturl()
            engine = create_async_engine(
                bouncer_url,
                pool_size=5,
                max_overflow=10,
                pool_timeout=30,
                pool_pre_ping=True,
            )
        elif instance and url.startswith("postgresql"):
            parsed = urlparse(CFG.SQLALCHEMY_DATABASE_URI)
            user, password, db = parsed.username, parsed.password, parsed.path.lstrip("/")

            async def _getconn():
                global _cloud_sql_connector
                if _cloud_sql_connector is None:
                    async with _connector_lock:
                        if _cloud_sql_connector is None:
                            from google.cloud.sql.connector import create_async_connector
                            _cloud_sql_connector = await create_async_connector()
                return await _cloud_sql_connector.connect_async(
                    instance, "asyncpg", user=user, password=password, db=db
                )

            engine = create_async_engine(
                "postgresql+asyncpg://",
                async_creator=_getconn,
                pool_size=5,
                max_overflow=10,
                pool_timeout=30,
                pool_pre_ping=True,
                pool_recycle=1800,
            )
        elif url.startswith("postgresql"):
            engine = create_async_engine(
                url,
                pool_size=5,
                max_overflow=10,
                pool_timeout=30,
                pool_pre_ping=True,
                pool_recycle=1800,
            )
        else:
            engine = create_async_engine(url)

        _async_session_local = async_sessionmaker(engine, expire_on_commit=False)
    return _async_session_local


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with _get_session_local()() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
