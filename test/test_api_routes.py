"""Session-gated JSON API under /api/."""

import uuid

import pytest


def _create_other_account():
    from models import _insert_returning_id, get_db

    suffix = uuid.uuid4().hex
    conn = get_db()
    cursor = conn.cursor()
    user_id = _insert_returning_id(
        cursor,
        """
        INSERT INTO users (username, email, full_name)
        VALUES (?, ?, ?)
        """,
        (f"other_{suffix}", f"other_{suffix}@example.com", "Other User"),
    )
    account_id = _insert_returning_id(
        cursor,
        """
        INSERT INTO accounts (user_id, account_type, account_number, balance)
        VALUES (?, ?, ?, ?)
        """,
        (user_id, "checking", f"QB-OTHER-{suffix[:12]}", 100.0),
    )
    conn.commit()
    conn.close()
    return account_id


@pytest.mark.api
def test_api_account_detail_unauthenticated_returns_json_error(client):
    response = client.get("/api/account/1")

    assert response.status_code == 401
    body = response.get_json()
    assert body is not None
    assert "error" in body


@pytest.mark.api
def test_api_accounts_unauthenticated_returns_json_error(client):
    response = client.get("/api/accounts")

    assert response.status_code == 401
    body = response.get_json()
    assert body is not None
    assert "error" in body


@pytest.mark.api
def test_api_transactions_unauthenticated_returns_json_error(client):
    response = client.get("/api/transactions")

    assert response.status_code == 401
    body = response.get_json()
    assert body is not None
    assert "error" in body


@pytest.mark.api
def test_api_accounts_after_login_non_empty(client):
    client.post("/login", data={"username": "demo"}, follow_redirects=True)

    response = client.get("/api/accounts")

    assert response.status_code == 200
    data = response.get_json()
    assert "accounts" in data
    assert isinstance(data["accounts"], list)
    assert len(data["accounts"]) >= 1


@pytest.mark.api
def test_api_transactions_after_login_list_shape(client):
    client.post("/login", data={"username": "demo"}, follow_redirects=True)

    response = client.get("/api/transactions")

    assert response.status_code == 200
    data = response.get_json()
    assert "transactions" in data
    assert isinstance(data["transactions"], list)


@pytest.mark.api
def test_api_account_detail_unknown_returns_json_error(client):
    client.post("/login", data={"username": "demo"}, follow_redirects=True)

    response = client.get("/api/account/999999")

    assert response.status_code == 404
    body = response.get_json()
    assert body is not None
    assert body.get("error") == "Account not found"


@pytest.mark.api
def test_api_account_detail_other_user_returns_json_error(client):
    other_account_id = _create_other_account()
    client.post("/login", data={"username": "demo"}, follow_redirects=True)

    response = client.get(f"/api/account/{other_account_id}")

    assert response.status_code == 404
    body = response.get_json()
    assert body is not None
    assert body.get("error") == "Account not found"


@pytest.mark.api
def test_api_account_detail_valid_id_200(client):
    client.post("/login", data={"username": "demo"}, follow_redirects=True)

    accounts = client.get("/api/accounts").get_json()["accounts"]
    account_id = accounts[0]["id"]
    response = client.get(f"/api/account/{account_id}")

    assert response.status_code == 200
    body = response.get_json()
    assert body is not None
    assert "account" in body
    assert body["account"]["id"] == account_id


@pytest.mark.api
def test_api_transfer_unauthenticated_401(client):
    response = client.post("/api/transfer", json={})

    assert response.status_code == 401
    body = response.get_json()
    assert body is not None
    assert body.get("success") is False


@pytest.mark.api
def test_api_transfer_missing_fields_400(client):
    client.post("/login", data={"username": "demo"}, follow_redirects=True)

    response = client.post("/api/transfer", json={"from_account_id": 1})

    assert response.status_code == 400
    body = response.get_json()
    assert body is not None
    assert body.get("success") is False
    assert "Missing required fields" in body.get("message", "")


@pytest.mark.api
def test_api_transfer_empty_body_400(client):
    client.post("/login", data={"username": "demo"}, follow_redirects=True)

    response = client.post("/api/transfer")

    assert response.status_code == 400
    body = response.get_json()
    assert body is not None
    assert body.get("success") is False
    assert "Missing required fields" in body.get("message", "")


@pytest.mark.api
def test_api_transfer_invalid_amount_400(client):
    client.post("/login", data={"username": "demo"}, follow_redirects=True)

    accounts = client.get("/api/accounts").get_json()["accounts"]
    checking = next(a for a in accounts if a["account_type"] == "checking")
    savings = next(a for a in accounts if a["account_type"] == "savings")
    response = client.post(
        "/api/transfer",
        json={
            "from_account_id": checking["id"],
            "to_account_id": savings["id"],
            "amount": -1,
            "description": "negative",
        },
    )

    assert response.status_code == 400
    body = response.get_json()
    assert body is not None
    assert body.get("success") is False
    assert "Invalid amount" in body.get("message", "")


@pytest.mark.api
def test_api_transfer_invalid_amount_non_numeric_400(client):
    client.post("/login", data={"username": "demo"}, follow_redirects=True)

    accounts = client.get("/api/accounts").get_json()["accounts"]
    checking = next(a for a in accounts if a["account_type"] == "checking")
    savings = next(a for a in accounts if a["account_type"] == "savings")
    response = client.post(
        "/api/transfer",
        json={
            "from_account_id": checking["id"],
            "to_account_id": savings["id"],
            "amount": "not-a-number",
            "description": "bad",
        },
    )

    assert response.status_code == 400
    body = response.get_json()
    assert body is not None
    assert body.get("success") is False


@pytest.mark.api
def test_api_transfer_same_account_400(client):
    client.post("/login", data={"username": "demo"}, follow_redirects=True)

    checking = next(
        a
        for a in client.get("/api/accounts").get_json()["accounts"]
        if a["account_type"] == "checking"
    )
    response = client.post(
        "/api/transfer",
        json={
            "from_account_id": checking["id"],
            "to_account_id": checking["id"],
            "amount": 1.0,
            "description": "same account",
        },
    )

    assert response.status_code == 400
    body = response.get_json()
    assert body is not None
    assert body.get("success") is False
    assert "Cannot transfer to the same account" in body.get("message", "")


@pytest.mark.api
def test_api_transfer_insufficient_funds_400(client):
    client.post("/login", data={"username": "demo"}, follow_redirects=True)

    accounts = client.get("/api/accounts").get_json()["accounts"]
    checking = next(a for a in accounts if a["account_type"] == "checking")
    savings = next(a for a in accounts if a["account_type"] == "savings")
    response = client.post(
        "/api/transfer",
        json={
            "from_account_id": checking["id"],
            "to_account_id": savings["id"],
            "amount": 999999999.0,
            "description": "too big",
        },
    )

    assert response.status_code == 400
    body = response.get_json()
    assert body is not None
    assert body.get("success") is False
    assert "Insufficient funds" in body.get("message", "")


@pytest.mark.api
def test_api_transfer_account_not_found_400(client):
    client.post("/login", data={"username": "demo"}, follow_redirects=True)

    response = client.post(
        "/api/transfer",
        json={
            "from_account_id": 999998,
            "to_account_id": 999999,
            "amount": 1.0,
            "description": "ghost accounts",
        },
    )

    assert response.status_code == 400
    body = response.get_json()
    assert body is not None
    assert body.get("success") is False
    assert "Account not found" in body.get("message", "")


@pytest.mark.api
def test_api_transfer_other_user_account_400(client):
    other_account_id = _create_other_account()
    client.post("/login", data={"username": "demo"}, follow_redirects=True)

    accounts = client.get("/api/accounts").get_json()["accounts"]
    checking = next(a for a in accounts if a["account_type"] == "checking")
    response = client.post(
        "/api/transfer",
        json={
            "from_account_id": checking["id"],
            "to_account_id": other_account_id,
            "amount": 1.0,
            "description": "other user",
        },
    )

    assert response.status_code == 400
    body = response.get_json()
    assert body is not None
    assert body.get("success") is False
    assert "Account not found" in body.get("message", "")


@pytest.mark.api
def test_api_transfer_small_amount_succeeds(client):
    client.post("/login", data={"username": "demo"}, follow_redirects=True)

    accounts = client.get("/api/accounts").get_json()["accounts"]
    checking = next(a for a in accounts if a["account_type"] == "checking")
    savings = next(a for a in accounts if a["account_type"] == "savings")
    response = client.post(
        "/api/transfer",
        json={
            "from_account_id": checking["id"],
            "to_account_id": savings["id"],
            "amount": 1.0,
            "description": "API pytest transfer",
        },
    )

    assert response.status_code == 200
    body = response.get_json()
    assert body is not None
    assert body.get("success") is True
    assert "Transfer successful" in body.get("message", "")
