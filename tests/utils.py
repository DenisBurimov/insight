from uuid import uuid4
from flask.testing import FlaskClient
from werkzeug.security import generate_password_hash
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
    password=TEST_USER_PASSWORD,
):
    password_hash = generate_password_hash(password)
    return name, password_hash


def login(client: FlaskClient, username=TEST_USER_NAME, password=TEST_USER_PASSWORD):
    response = client.post(
        "/login",
        data=dict(user_id=username, password=password),
        follow_redirects=True,
    )
    return response


def logout(client: FlaskClient):
    return client.get("/logout", follow_redirects=True)
