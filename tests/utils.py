# ruff: noqa: F601
import json
from datetime import datetime
from uuid import uuid4
from io import BytesIO
from flask.testing import FlaskClient
from werkzeug.datastructures import MultiDict, FileStorage
from werkzeug.security import generate_password_hash
from app import spanner_service
from config import config


CFG = config("testing")

TEST_USER_NAME = "bob"
TEST_USER_EMAIL = "bob@test.com"
TEST_USER_PASSWORD = "password"
TEST_USER_ROLE = "manager"
TEST_USER_EDRPOUS = ""


def gen_uuid() -> str:
    return str(uuid4())


def register(
    name=TEST_USER_NAME,
    emails=TEST_USER_EMAIL,
    password=TEST_USER_PASSWORD,
    role=TEST_USER_ROLE,
    edrpous=TEST_USER_EDRPOUS,
):
    password_hash = generate_password_hash(password)
    spanner_service.insert_data(
        "users",
        (
            "id",
            "name",
            "emails",
            "password_hash",
            "role",
            "created_at",
            "is_deleted",
            "is_active",
            "is_2fa_activated",
            "secret",
            "edrpous",
        ),
        (
            gen_uuid(),
            name,
            emails,
            password_hash,
            role,
            datetime.now().strftime("%Y-%m-%d"),
            False,
            True,
            False,
            "some-secret",
            edrpous,
        ),
    )
    return name, password


def login(client: FlaskClient, username=TEST_USER_NAME, password=TEST_USER_PASSWORD):
    response = client.post(
        "/login",
        data=dict(user_id=username, password=password),
        follow_redirects=True,
    )
    return response


def logout(client: FlaskClient):
    return client.get("/logout", follow_redirects=True)
