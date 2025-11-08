# ruff: noqa: F841
import os
import pytest
from flask.testing import FlaskClient
from config import config
from app import spanner_service
from app.spanner.test_data import (
    insert_testing_accounts_data,
    insert_testing_transaction_data,
    insert_testing_clients_data,
    insert_testing_entities_data,
    insert_testing_balances_data,
)
from app.spanner import models as m
from app.logger import log
from app.mail import mail


CFG = config("testing")


def test_api_transactions(client: FlaskClient):
    os.environ["TRANSACTIONS_API_URL"] = "https://my.ukrgasbank.com/transactions"
    _, count = insert_testing_clients_data("tests/test-clients.json")
    transactions_object = spanner_service.execute_sql("SELECT * FROM transactions")
    transactions_list = [row for row in transactions_object]
    assert len(transactions_list) == 0

    response = client.get(
        "/api/v1/transactions/add_new",
        headers={"Access-Token": "some_token"},
    )
    assert response
    assert response.status_code == 200
    assert "Add new transactions successful" in response.get_json().get("message", "")

    # transactions_object = spanner_service.execute_sql("SELECT * FROM transactions")
    # transactions_list = [row for row in transactions_object]
    # assert len(transactions_list) == 2 * count


def test_api_accounts(client: FlaskClient):
    os.environ["ACCOUNTS_API_URL"] = "https://my.ukrgasbank.com/accounts"
    insert_testing_clients_data("tests/test-clients.json")
    accounts_object = spanner_service.execute_sql("SELECT * FROM accounts")
    accounts_list = [row for row in accounts_object]
    assert len(accounts_list) == 0

    response = client.get(
        "/api/v1/accounts/add_new",
        headers={"Access-Token": "some_token"},
    )
    log(log.INFO, "First request done")

    assert response
    assert response.status_code == 200
    assert "Add new accounts successfu" in response.get_json().get("message", "")

    accounts_object = spanner_service.execute_sql("SELECT * FROM accounts")
    accounts_list = [row for row in accounts_object]
    assert len(accounts_list) == 2


def test_set_categoory(client: FlaskClient):
    file_transactions, _ = insert_testing_transaction_data()
    null_category_transactions = [
        transaction
        for transaction in file_transactions
        if not transaction.payment_category
    ]

    # Request without auth token
    response = client.get("/api/v1/transactions/set_category")
    assert response.status_code == 403

    # Request with auth token
    response = client.get(
        "/api/v1/transactions/set_category",
        headers={"Access-Token": "some_token"},
    )
    assert response.status_code == 200
    assert response.json
    assert len(null_category_transactions) == response.json["updated_transactions"]


def test_tokens_expired(client: FlaskClient):
    with mail.record_messages() as outbox:
        response = client.get(
            "/api/v1/tokens/",
        )
        assert response
        assert response.status_code == 403

        file_clients, count = insert_testing_clients_data(
            "tests/test-expired-clients.json"
        )
        assert count == 3
        token = os.environ.get("SCHEDULER_ACCESS_TOKEN")
        response = client.get(
            "/api/v1/tokens/",
            headers={"Access-Token": token},
        )
        assert response
        assert response.status_code == 200
        file_clients[0].manager_name in response.data.decode("utf-8")
        file_clients[1].manager_name in response.data.decode("utf-8")
        file_clients[2].manager_name in response.data.decode("utf-8")


def test_webhook(client: FlaskClient):
    payload = {
        "message": {
            "data": "eyJlbWFpbEFkZHJlc3MiOiJtZSIsImhpc3RvcnlJZCI6IjEyMzQ1Njc4OSJ9",
            "messageId": "123456789",
            "publishTime": "2024-12-27T10:00:00Z",
        },
        "subscription": "projects/YOUR_PROJECT_ID/subscriptions/gmail-webhook-sub",
    }
    response = client.post(
        "/api/v1/emails/webhook",
        headers={"Access-Token": "some_token"},
        json=payload,
    )
    assert response
    assert response.status_code == 200
    if response.json:
        assert payload == response.json.get("data")


@pytest.mark.skipif(True, reason="Local test")
def test_prod_webhook(client: FlaskClient):
    import requests

    url = CFG.GMAIL_WEBHOOK
    payload = {
        "message": {
            "data": "eyJlbWFpbEFkZHJlc3MiOiJtZSIsImhpc3RvcnlJZCI6IjEyMzQ1Njc4OSJ9",
            "messageId": "123456789",
            "publishTime": "2024-12-27T10:00:00Z",
        },
        "subscription": "projects/YOUR_PROJECT_ID/subscriptions/gmail-webhook-sub",
    }
    response = requests.post(
        url=url,
        json=payload,
    )
    assert response
    assert response.status_code == 200


def test_get_data_for_ukrgazbank_query(client: FlaskClient):
    inserted_clients, _ = insert_testing_clients_data("tests/test-clients.json")
    assert inserted_clients

    inserted_accounts, _ = insert_testing_accounts_data()
    assert inserted_accounts

    # inserted_transactions, _ = insert_testing_transaction_data()
    # assert inserted_transactions

    edrpous, client_tokens, accounts_data, max_dates = (
        spanner_service.get_data_for_ukrgazbank_query()
    )
    assert edrpous
    assert client_tokens
    assert accounts_data
    assert max_dates


def test_balances(client: FlaskClient):
    balances_object = spanner_service.execute_sql("SELECT * FROM balances")
    balances_list = [row for row in balances_object]
    assert len(balances_list) == 0

    response = client.get(
        "/api/v1/balances/add_new",
    )
    assert response
    assert response.status_code == 403

    insert_testing_clients_data("tests/test-clients.json")

    response = client.get(
        "/api/v1/balances/add_new",
        headers={"Access-Token": "some_token"},
    )

    assert response
    assert response.status_code == 200
    assert "Add and update new balances successful" in response.get_json().get(
        "message", ""
    )

    balances_object = spanner_service.execute_sql("SELECT * FROM balances")
    balances_list = [row for row in balances_object]
    assert len(balances_list) > 0


def test_api_transactions_for_power_bi(client: FlaskClient):
    response = client.get(
        "/api/v1/transactions/power_bi",
    )
    assert response
    assert response.status_code == 403

    file_transactions, count = insert_testing_transaction_data()

    response = client.get(
        "/api/v1/transactions/power_bi",
        headers={"Access-Token": "some_token"},
    )
    assert response
    assert response.status_code == 200
    assert response.json
    assert len(response.json.get("transactions")) == count
    test = [
        item
        for item in response.json.get("transactions")
        if item.get("id_trnsctn") == file_transactions[0].model_dump().get("id_trnsctn")
    ]
    assert len(test) == 1


def test_api_accounts_for_power_bi(client: FlaskClient):
    response = client.get(
        "/api/v1/accounts/power_bi",
    )
    assert response
    assert response.status_code == 403

    file_accounts, count = insert_testing_accounts_data()

    response = client.get(
        "/api/v1/accounts/power_bi",
        headers={"Access-Token": "some_token"},
    )
    assert response
    assert response.status_code == 200
    assert response.json
    assert len(response.json.get("accounts")) == count
    test = [
        item
        for item in response.json.get("accounts")
        if item.get("iban") == file_accounts[0].model_dump().get("iban")
    ]
    assert len(test) == 1


def test_api_clients_for_power_bi(client: FlaskClient):
    response = client.get(
        "/api/v1/clients/power_bi",
    )
    assert response
    assert response.status_code == 403

    file_clients, count = insert_testing_clients_data("tests/test-clients.json")

    response = client.get(
        "/api/v1/clients/power_bi",
        headers={"Access-Token": "some_token"},
    )
    assert response
    assert response.status_code == 200
    assert response.json
    assert len(response.json.get("clients")) == count
    test = [
        item
        for item in response.json.get("clients")
        if item.get("id") == file_clients[0].model_dump().get("id")
    ]
    assert len(test) == 1


def test_api_entities_for_power_bi(client: FlaskClient):
    response = client.get(
        "/api/v1/entities/power_bi",
    )
    assert response
    assert response.status_code == 403

    file_entities, count = insert_testing_entities_data()

    response = client.get(
        "/api/v1/entities/power_bi",
        headers={"Access-Token": "some_token"},
    )
    assert response
    assert response.status_code == 200
    assert response.json
    assert len(response.json.get("entities")) == count
    test = [
        item
        for item in response.json.get("entities")
        if item.get("id") == file_entities[0].model_dump().get("id")
    ]
    assert len(test) == 1


def test_api_balances_for_power_bi(client: FlaskClient):
    response = client.get(
        "/api/v1/balances/power_bi",
    )
    assert response
    assert response.status_code == 403

    file_balances, count = insert_testing_balances_data()

    response = client.get(
        "/api/v1/balances/power_bi",
        headers={"Access-Token": "some_token"},
    )
    assert response
    assert response.status_code == 200
    assert response.json
    assert len(response.json.get("balances")) == count
    test = [
        item
        for item in response.json.get("balances")
        if item.get("id_record") == file_balances[0].model_dump().get("id_record")
    ]
    assert len(test) == 1


def test_api_balances_calculated(client: FlaskClient):
    _, tr_count = insert_testing_transaction_data()
    _ = insert_testing_accounts_data()

    balances_calculated_rows = spanner_service.execute_sql(
        "SELECT * FROM balances_calculated"
    )
    balances_calculated = [
        m.BalancesCalculatedBasicModel.from_spanner(row)
        for row in balances_calculated_rows
    ]
    assert len(balances_calculated) == 0
    response = client.get(
        "/api/v1/balances_calculated/add_new",
    )
    assert response
    assert response.status_code == 403

    response = client.get(
        "/api/v1/balances_calculated/add_new",
        headers={"Access-Token": "some_token"},
    )
    assert response
    assert response.status_code == 200


def test_api_balances_calculate_latest(client: FlaskClient):
    _, tr_count = insert_testing_transaction_data()
    _ = insert_testing_accounts_data()

    balances_calculated_rows = spanner_service.execute_sql(
        "SELECT * FROM balances_calculated"
    )
    balances_calculated = [
        m.BalancesCalculatedBasicModel.from_spanner(row)
        for row in balances_calculated_rows
    ]
    assert len(balances_calculated) == 0
    response = client.get(
        "/api/v1/balances_calculated/calc_latest",
    )
    assert response
    assert response.status_code == 403

    response = client.get(
        "/api/v1/balances_calculated/calc_latest",
        headers={"Access-Token": "some_token"},
    )
    assert response
    assert response.status_code == 200
