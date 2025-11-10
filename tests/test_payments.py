# ruff: noqa: F841
import pytest
from flask.testing import FlaskClient
from config import config
from app import models as m
from app.logger import log


CFG = config("testing")


# @pytest.mark.skipif(True, reason="Local test")
def test_api_transactions(client: FlaskClient):
    response = client.post("/preview")
    assert response
    assert response.status_code == 200
