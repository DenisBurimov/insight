# ruff: noqa: F402
import pytest
from dotenv import load_dotenv
from flask import Flask

from app import create_app, spanner_service
from app.spanner.test_db import (
    delete_database,
    delete_instance,
    create_database,
    create_instance,
)
from tests.utils import register, login
from config import config


load_dotenv("tests/test.env")
CFG = config("testing")


@pytest.fixture()
def app():
    app = create_app("testing")
    app.config.update(
        {
            "TESTING": True,
        }
    )
    from app import commands

    commands.init(app)

    yield app


@pytest.fixture()
def client(app: Flask):
    with app.test_client() as client:
        app_ctx = app.app_context()
        app_ctx.push()

        if not spanner_service.instance.exists():
            create_instance(CFG.SPANNER_INSTANCE_ID)
        if spanner_service.database.exists():
            delete_database(spanner_service.database)
        create_database(CFG.SPANNER_INSTANCE_ID, CFG.SPANNER_DATABASE_ID)

        username, password = register("Quantum Tech Engineering")
        login(client, username, password)

        yield client

        delete_database(spanner_service.database)
        delete_instance(spanner_service.instance)
        app_ctx.pop()


@pytest.fixture()
def runner(app, client):

    yield app.test_cli_runner()
