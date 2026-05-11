import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker, Session

from api.main import app
from api.database import get_db
from database import db
import models as m  # noqa: F401 - registers tables in db.metadata

# Shared-cache URI lets both the sync setup session and the async app session
# see the same in-memory database within the same process.
_SYNC_URL = "sqlite:///file::memory:?cache=shared&uri=true"
_ASYNC_URL = "sqlite+aiosqlite:///file::memory:?cache=shared&uri=true"


@pytest.fixture(scope="function")
def db_session():
    engine = create_engine(_SYNC_URL, connect_args={"check_same_thread": False})
    db.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    try:
        yield session
    finally:
        session.close()
        db.metadata.drop_all(engine)
        engine.dispose()


@pytest.fixture(scope="function")
def client(db_session: Session):
    async_engine = create_async_engine(
        _ASYNC_URL, connect_args={"check_same_thread": False}
    )
    factory = async_sessionmaker(async_engine, expire_on_commit=False)

    async def override_get_db():
        async with factory() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
