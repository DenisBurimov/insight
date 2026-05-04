import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

import models as m


# ── helpers ──────────────────────────────────────────────────────────────────

def make_payment(session: Session, **kwargs) -> m.Payment:
    defaults = {
        "filename": "test.jpg",
        "number": "001",
        "payment_date": "2024-01-15",
        "summ": "1000.00",
        "payer_name": "John Doe",
        "payer_iban": "UA123456789",
        "recipient_name": "Jane Smith",
        "recipient_iban": "UA987654321",
        "payment_purpose": "Test payment",
    }
    defaults.update(kwargs)
    payment = m.Payment(**defaults)
    session.add(payment)
    session.commit()
    session.refresh(payment)
    return payment


def mcp_post(client: TestClient, method: str, params: dict | None = None, id_: int = 1) -> dict:
    body: dict = {"jsonrpc": "2.0", "id": id_, "method": method}
    if params is not None:
        body["params"] = params
    return client.post("/mcp", json=body)


# ── ping ──────────────────────────────────────────────────────────────────────

def test_mcp_ping(client: TestClient):
    response = client.get("/mcp")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# ── initialize ────────────────────────────────────────────────────────────────

def test_initialize_returns_server_info(client: TestClient):
    response = mcp_post(client, "initialize")
    assert response.status_code == 200
    result = response.json()["result"]
    assert result["protocolVersion"] == "2024-11-05"
    assert result["capabilities"] == {"tools": {}}
    assert result["serverInfo"]["name"] == "insight-mcp"


def test_initialize_echoes_id(client: TestClient):
    response = mcp_post(client, "initialize", id_=42)
    assert response.json()["id"] == 42


# ── tools/list ────────────────────────────────────────────────────────────────

def test_tools_list_returns_all_tools(client: TestClient):
    response = mcp_post(client, "tools/list")
    assert response.status_code == 200
    tools = response.json()["result"]["tools"]
    names = {t["name"] for t in tools}
    assert names == {"get_payments", "get_payment"}


def test_tools_list_have_input_schemas(client: TestClient):
    response = mcp_post(client, "tools/list")
    tools = {t["name"]: t for t in response.json()["result"]["tools"]}
    assert "inputSchema" in tools["get_payments"]
    assert "inputSchema" in tools["get_payment"]
    assert "id" in tools["get_payment"]["inputSchema"]["properties"]


# ── tools/call — get_payments ─────────────────────────────────────────────────

def test_get_payments_empty_db_returns_header_only(client: TestClient):
    response = mcp_post(client, "tools/call", {"name": "get_payments", "arguments": {}})
    assert response.status_code == 200
    text = response.json()["result"]["content"][0]["text"]
    assert text.startswith("id,filename")
    assert len(text.splitlines()) == 1


def test_get_payments_returns_all_rows(client: TestClient, db_session: Session):
    make_payment(db_session, filename="a.jpg", payer_name="Alpha")
    make_payment(db_session, filename="b.jpg", payer_name="Beta")

    response = mcp_post(client, "tools/call", {"name": "get_payments", "arguments": {}})
    text = response.json()["result"]["content"][0]["text"]
    assert "Alpha" in text
    assert "Beta" in text
    assert len(text.splitlines()) == 3  # header + 2 rows


def test_get_payments_filter_payer_name(client: TestClient, db_session: Session):
    make_payment(db_session, filename="a.jpg", payer_name="Alpha Corp")
    make_payment(db_session, filename="b.jpg", payer_name="Beta Ltd")

    response = mcp_post(client, "tools/call", {"name": "get_payments", "arguments": {"payer_name": "alpha"}})
    text = response.json()["result"]["content"][0]["text"]
    assert "Alpha Corp" in text
    assert "Beta Ltd" not in text


def test_get_payments_filter_recipient_name(client: TestClient, db_session: Session):
    make_payment(db_session, filename="a.jpg", recipient_name="Receiver One")
    make_payment(db_session, filename="b.jpg", recipient_name="Receiver Two")

    response = mcp_post(client, "tools/call", {"name": "get_payments", "arguments": {"recipient_name": "Two"}})
    text = response.json()["result"]["content"][0]["text"]
    assert "Receiver Two" in text
    assert "Receiver One" not in text


def test_get_payments_respects_limit(client: TestClient, db_session: Session):
    for i in range(5):
        make_payment(db_session, filename=f"{i}.jpg")

    response = mcp_post(client, "tools/call", {"name": "get_payments", "arguments": {"limit": 2}})
    text = response.json()["result"]["content"][0]["text"]
    assert len(text.splitlines()) == 3  # header + 2 rows


def test_get_payments_clamps_limit_to_500(client: TestClient, db_session: Session):
    for i in range(3):
        make_payment(db_session, filename=f"{i}.jpg")

    response = mcp_post(client, "tools/call", {"name": "get_payments", "arguments": {"limit": 99999}})
    text = response.json()["result"]["content"][0]["text"]
    assert len(text.splitlines()) == 4  # header + 3 rows (all 3, since 3 < 500)


def test_get_payments_csv_contains_expected_columns(client: TestClient, db_session: Session):
    make_payment(
        db_session,
        filename="invoice.jpg",
        number="INV-001",
        summ="2500.00",
        payer_iban="UA111",
        recipient_iban="UA222",
        payment_purpose="Consulting services",
    )
    response = mcp_post(client, "tools/call", {"name": "get_payments", "arguments": {}})
    text = response.json()["result"]["content"][0]["text"]
    assert "invoice.jpg" in text
    assert "INV-001" in text
    assert "2500.00" in text
    assert "UA111" in text
    assert "UA222" in text
    assert "Consulting services" in text


# ── tools/call — get_payment ──────────────────────────────────────────────────

def test_get_payment_returns_all_fields(client: TestClient, db_session: Session):
    payment = make_payment(
        db_session,
        filename="single.jpg",
        number="P-999",
        payment_date="2024-03-01",
        summ="750.00",
        summ_words="Seven hundred fifty",
        payer_name="Payer Inc",
        payer_code="12345678",
        payer_bank_name="First Bank",
        payer_iban="UA_PAYER_IBAN",
        recipient_name="Recipient LLC",
        recipient_code="87654321",
        recipient_bank_name="Second Bank",
        recipient_iban="UA_RECIPIENT_IBAN",
        payment_purpose="Rent payment",
    )

    response = mcp_post(client, "tools/call", {"name": "get_payment", "arguments": {"id": payment.id}})
    text = response.json()["result"]["content"][0]["text"]

    assert "single.jpg" in text
    assert "P-999" in text
    assert "750.00" in text
    assert "Seven hundred fifty" in text
    assert "Payer Inc" in text
    assert "12345678" in text
    assert "First Bank" in text
    assert "UA_PAYER_IBAN" in text
    assert "Recipient LLC" in text
    assert "87654321" in text
    assert "Second Bank" in text
    assert "UA_RECIPIENT_IBAN" in text
    assert "Rent payment" in text


def test_get_payment_not_found(client: TestClient):
    response = mcp_post(client, "tools/call", {"name": "get_payment", "arguments": {"id": 99999}})
    text = response.json()["result"]["content"][0]["text"]
    assert "not found" in text.lower()


def test_get_payment_uses_correct_id(client: TestClient, db_session: Session):
    p1 = make_payment(db_session, filename="first.jpg", summ="100.00")
    p2 = make_payment(db_session, filename="second.jpg", summ="200.00")

    response = mcp_post(client, "tools/call", {"name": "get_payment", "arguments": {"id": p2.id}})
    text = response.json()["result"]["content"][0]["text"]
    assert "second.jpg" in text
    assert "first.jpg" not in text


# ── notifications ─────────────────────────────────────────────────────────────

def test_notifications_returns_202(client: TestClient):
    response = mcp_post(client, "notifications/initialized")
    assert response.status_code == 202


def test_notifications_any_subpath_returns_202(client: TestClient):
    response = mcp_post(client, "notifications/cancelled")
    assert response.status_code == 202


# ── error handling ────────────────────────────────────────────────────────────

def test_unknown_tool_returns_error(client: TestClient):
    response = mcp_post(client, "tools/call", {"name": "nonexistent_tool", "arguments": {}})
    assert response.status_code == 200
    error = response.json()["result"]["error"]
    assert error["code"] == -32601
    assert "nonexistent_tool" in error["message"]


def test_unknown_method_returns_error(client: TestClient):
    response = mcp_post(client, "tools/call-nonexistent")
    assert response.status_code == 200
    error = response.json()["result"]["error"]
    assert error["code"] == -32601
    assert "not found" in error["message"].lower()


def test_jsonrpc_id_is_echoed_in_error(client: TestClient):
    response = mcp_post(client, "tools/call", {"name": "bad_tool", "arguments": {}}, id_=7)
    assert response.json()["id"] == 7
    assert response.json()["jsonrpc"] == "2.0"
