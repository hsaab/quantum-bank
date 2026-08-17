"""Session-gated JSON API under /api/."""

import pytest


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
def test_api_transfer_invalid_amount_nan_400(client):
    client.post("/login", data={"username": "demo"}, follow_redirects=True)

    accounts = client.get("/api/accounts").get_json()["accounts"]
    checking = next(a for a in accounts if a["account_type"] == "checking")
    savings = next(a for a in accounts if a["account_type"] == "savings")
    response = client.post(
        "/api/transfer",
        json={
            "from_account_id": checking["id"],
            "to_account_id": savings["id"],
            "amount": "nan",
            "description": "bad-nan",
        },
    )

    assert response.status_code == 400
    body = response.get_json()
    assert body is not None
    assert body.get("success") is False
    assert "Invalid amount" in body.get("message", "")


@pytest.mark.api
@pytest.mark.parametrize("bad_amount", ["nan", "NaN", "inf"])
def test_api_transfer_rejects_nan_inf_strings_400(client, bad_amount):
    client.post("/login", data={"username": "demo"}, follow_redirects=True)

    accounts = client.get("/api/accounts").get_json()["accounts"]
    checking = next(a for a in accounts if a["account_type"] == "checking")
    savings = next(a for a in accounts if a["account_type"] == "savings")
    response = client.post(
        "/api/transfer",
        json={
            "from_account_id": checking["id"],
            "to_account_id": savings["id"],
            "amount": bad_amount,
            "description": "bad-float-string",
        },
    )

    assert response.status_code == 400
    body = response.get_json()
    assert body is not None
    assert body.get("success") is False
    assert "Invalid amount" in body.get("message", "")


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
def test_api_transfer_small_amount_succeeds(client):
    client.post("/login", data={"username": "demo"}, follow_redirects=True)

    accounts = client.get("/api/accounts").get_json()["accounts"]
    checking = next(a for a in accounts if a["account_type"] == "checking")
    savings = next(a for a in accounts if a["account_type"] == "savings")
    checking_before = checking["balance"]
    savings_before = savings["balance"]
    amount = 1.0
    response = client.post(
        "/api/transfer",
        json={
            "from_account_id": checking["id"],
            "to_account_id": savings["id"],
            "amount": amount,
            "description": "API pytest transfer",
        },
    )
    accounts_after = client.get("/api/accounts").get_json()["accounts"]
    checking_after = next(a for a in accounts_after if a["account_type"] == "checking")
    savings_after = next(a for a in accounts_after if a["account_type"] == "savings")

    assert response.status_code == 200
    body = response.get_json()
    assert body is not None
    assert body.get("success") is True
    assert "Transfer successful" in body.get("message", "")
    assert checking_after["balance"] == pytest.approx(checking_before - amount)
    assert savings_after["balance"] == pytest.approx(savings_before + amount)


@pytest.mark.api
def test_api_transfer_rejects_cross_user_source_account(client):
    client.post("/login", data={"username": "demo"}, follow_redirects=True)

    import models
    import uuid

    suffix = uuid.uuid4().hex[:12]

    conn = models.get_db()
    try:
        cursor = conn.cursor()
        attacker_user_id = models._insert_returning_id(
            cursor,
            """
            INSERT INTO users (username, email, full_name)
            VALUES (?, ?, ?)
            """,
            (
                f"api_attacker_{suffix}",
                f"api_attacker_{suffix}@example.com",
                "API Attacker",
            ),
        )
        attacker_checking_id = models._insert_returning_id(
            cursor,
            """
            INSERT INTO accounts (user_id, account_type, account_number, balance)
            VALUES (?, ?, ?, ?)
            """,
            (attacker_user_id, "checking", f"QB-CHK-{suffix}", 500.0),
        )
        conn.commit()
    finally:
        conn.close()

    victim_accounts = client.get("/api/accounts").get_json()["accounts"]
    victim_savings = next(a for a in victim_accounts if a["account_type"] == "savings")
    response = client.post(
        "/api/transfer",
        json={
            "from_account_id": attacker_checking_id,
            "to_account_id": victim_savings["id"],
            "amount": 10.0,
            "description": "forbidden api transfer",
        },
    )

    assert response.status_code == 403
    body = response.get_json()
    assert body is not None
    assert body.get("success") is False
    assert body.get("message") == "Forbidden"
