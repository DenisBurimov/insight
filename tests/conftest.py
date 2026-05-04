import pytest
from flask import Flask

from app import create_app
from database import db as _db
import models as m  # noqa: F401 - registers tables in db.metadata


@pytest.fixture(scope="function")
def app():
    app = create_app("testing")
    app.config["WTF_CSRF_ENABLED"] = False
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture(scope="function")
def client(app: Flask):
    with app.test_client() as client:
        yield client


@pytest.fixture(scope="function")
def runner(app: Flask):
    yield app.test_cli_runner()
