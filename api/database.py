from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from config import config

_session_local = None


def _get_session_local():
    global _session_local
    if _session_local is None:
        CFG = config()
        _session_local = sessionmaker(bind=create_engine(CFG.SQLALCHEMY_DATABASE_URI))
    return _session_local


def get_db() -> Generator[Session, None, None]:
    db = _get_session_local()()
    try:
        yield db
    finally:
        db.close()
