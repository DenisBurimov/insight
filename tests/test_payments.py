from flask.testing import FlaskClient
from config import config

CFG = config("testing")


def test_payments_sync_requires_token(client: FlaskClient):
    response = client.get("/api/v1/payments/sync")
    assert response.status_code == 403
    assert response.get_json()["message"] == "Access denied"


def test_payments_sync_with_valid_token(client: FlaskClient):
    response = client.get(
        "/api/v1/payments/sync",
        headers={"Access-Token": CFG.SCHEDULER_ACCESS_TOKEN},
    )
    assert response.status_code == 200
    assert response.get_json()["message"] == "Sample endpoint"
