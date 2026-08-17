"""Login, session, and authenticated HTML banking routes."""

import pytest


@pytest.mark.banking
def test_login_page_renders_sign_in_form(client):
    response = client.get("/login")

    assert response.status_code == 200
    assert b"Sign In" in response.data
    assert b'name="username"' in response.data


@pytest.mark.banking
def test_login_post_missing_username_shows_error(client):
    response = client.post("/login", data={}, follow_redirects=True)

    assert response.status_code == 200
    assert b"Username is required" in response.data


@pytest.mark.banking
def test_login_post_unknown_user_shows_error(client):
    response = client.post(
        "/login", data={"username": "not_a_real_user_xyz"}, follow_redirects=True
    )

    assert response.status_code == 200
    assert b"User not found" in response.data


@pytest.mark.banking
def test_login_post_demo_redirects_to_dashboard(client):
    response = client.post("/login", data={"username": "demo"}, follow_redirects=False)

    assert response.status_code in (302, 303)
    assert "dashboard" in response.headers.get("Location", "").lower()


@pytest.mark.banking
def test_login_post_demo_followed_renders_dashboard(client):
    response = client.post("/login", data={"username": "demo"}, follow_redirects=True)

    assert response.status_code == 200
    assert b"Welcome back" in response.data
    assert b"Your Accounts" in response.data


@pytest.mark.banking
def test_dashboard_requires_login(client):
    response = client.get("/dashboard", follow_redirects=False)

    assert response.status_code in (302, 303)
    assert "login" in response.headers.get("Location", "").lower()


@pytest.mark.banking
def test_logout_after_login_redirects_to_login(client):
    client.post("/login", data={"username": "demo"}, follow_redirects=True)

    response = client.get("/logout", follow_redirects=False)

    assert response.status_code in (302, 303)
    assert "login" in response.headers.get("Location", "").lower()


@pytest.mark.banking
def test_transactions_requires_login_redirect(client):
    response = client.get("/transactions", follow_redirects=False)

    assert response.status_code in (302, 303)
    assert "login" in response.headers.get("Location", "").lower()


@pytest.mark.banking
def test_account_detail_requires_login_redirect(client):
    response = client.get("/account?id=1", follow_redirects=False)

    assert response.status_code in (302, 303)
    assert "login" in response.headers.get("Location", "").lower()


@pytest.mark.banking
def test_transfer_page_renders_when_authenticated(client):
    client.post("/login", data={"username": "demo"}, follow_redirects=True)

    response = client.get("/transfer")

    assert response.status_code == 200
    assert b"Transfer Money" in response.data


@pytest.mark.banking
def test_transfer_post_missing_fields_shows_error(client):
    client.post("/login", data={"username": "demo"}, follow_redirects=True)

    response = client.post("/transfer", data={}, follow_redirects=True)

    assert response.status_code == 200
    assert b"All fields are required" in response.data


@pytest.mark.banking
def test_transfer_post_invalid_amount_shows_error(client):
    client.post("/login", data={"username": "demo"}, follow_redirects=True)

    accounts = client.get("/api/accounts").get_json()["accounts"]
    checking = next(a for a in accounts if a["account_type"] == "checking")
    savings = next(a for a in accounts if a["account_type"] == "savings")
    response = client.post(
        "/transfer",
        data={
            "from_account": str(checking["id"]),
            "to_account": str(savings["id"]),
            "amount": "not-a-number",
            "description": "bad",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Invalid amount" in response.data


@pytest.mark.banking
def test_transfer_post_nan_amount_shows_error(client):
    client.post("/login", data={"username": "demo"}, follow_redirects=True)

    accounts = client.get("/api/accounts").get_json()["accounts"]
    checking = next(a for a in accounts if a["account_type"] == "checking")
    savings = next(a for a in accounts if a["account_type"] == "savings")
    response = client.post(
        "/transfer",
        data={
            "from_account": str(checking["id"]),
            "to_account": str(savings["id"]),
            "amount": "nan",
            "description": "bad-nan",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Invalid amount" in response.data


@pytest.mark.banking
@pytest.mark.parametrize("bad_amount", ["nan", "NaN", "inf"])
def test_transfer_post_rejects_nan_inf_strings(client, bad_amount):
    client.post("/login", data={"username": "demo"}, follow_redirects=True)

    accounts = client.get("/api/accounts").get_json()["accounts"]
    checking = next(a for a in accounts if a["account_type"] == "checking")
    savings = next(a for a in accounts if a["account_type"] == "savings")
    response = client.post(
        "/transfer",
        data={
            "from_account": str(checking["id"]),
            "to_account": str(savings["id"]),
            "amount": bad_amount,
            "description": "bad-float-string",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Invalid amount" in response.data


@pytest.mark.banking
def test_transfer_post_zero_amount_shows_error(client):
    client.post("/login", data={"username": "demo"}, follow_redirects=True)

    accounts = client.get("/api/accounts").get_json()["accounts"]
    checking = next(a for a in accounts if a["account_type"] == "checking")
    savings = next(a for a in accounts if a["account_type"] == "savings")
    response = client.post(
        "/transfer",
        data={
            "from_account": str(checking["id"]),
            "to_account": str(savings["id"]),
            "amount": "0",
            "description": "zero",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Invalid amount" in response.data


@pytest.mark.banking
def test_transfer_post_insufficient_funds_shows_error(client):
    client.post("/login", data={"username": "demo"}, follow_redirects=True)

    accounts = client.get("/api/accounts").get_json()["accounts"]
    checking = next(a for a in accounts if a["account_type"] == "checking")
    savings = next(a for a in accounts if a["account_type"] == "savings")
    response = client.post(
        "/transfer",
        data={
            "from_account": str(checking["id"]),
            "to_account": str(savings["id"]),
            "amount": "999999999.00",
            "description": "too big",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Insufficient funds" in response.data


@pytest.mark.banking
def test_account_detail_unknown_id_redirects_to_dashboard(client):
    client.post("/login", data={"username": "demo"}, follow_redirects=True)

    response = client.get("/account?id=999999", follow_redirects=False)

    assert response.status_code in (302, 303)
    assert "dashboard" in response.headers.get("Location", "").lower()


@pytest.mark.banking
def test_transactions_authenticated_200(client):
    client.post("/login", data={"username": "demo"}, follow_redirects=True)

    response = client.get("/transactions")

    assert response.status_code == 200
    assert b"All Transactions" in response.data


@pytest.mark.banking
def test_account_detail_authenticated_200(client):
    client.post("/login", data={"username": "demo"}, follow_redirects=True)

    acct = client.get("/api/accounts").get_json()["accounts"][0]
    response = client.get(f"/account?id={acct['id']}")

    assert response.status_code == 200
    assert b"Back to Dashboard" in response.data


@pytest.mark.banking
def test_transfer_get_requires_login_redirect(client):
    response = client.get("/transfer", follow_redirects=False)

    assert response.status_code in (302, 303)
    assert "login" in response.headers.get("Location", "").lower()


@pytest.mark.banking
def test_account_detail_non_numeric_id_redirects_to_dashboard(client):
    """Postgres rejects non-int comparisons; coerce at the boundary on both backends."""
    client.post("/login", data={"username": "demo"}, follow_redirects=True)

    response = client.get("/account?id=not-a-number", follow_redirects=False)

    assert response.status_code in (302, 303)
    assert "dashboard" in response.headers.get("Location", "").lower()


@pytest.mark.banking
def test_account_without_id_redirects_to_dashboard(client):
    client.post("/login", data={"username": "demo"}, follow_redirects=True)

    response = client.get("/account", follow_redirects=False)

    assert response.status_code in (302, 303)
    assert "dashboard" in response.headers.get("Location", "").lower()


@pytest.mark.banking
def test_transfer_post_same_account_shows_error(client):
    client.post("/login", data={"username": "demo"}, follow_redirects=True)

    checking = next(
        a
        for a in client.get("/api/accounts").get_json()["accounts"]
        if a["account_type"] == "checking"
    )
    aid = str(checking["id"])
    response = client.post(
        "/transfer",
        data={
            "from_account": aid,
            "to_account": aid,
            "amount": "10.00",
            "description": "Test",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Cannot transfer to the same account" in response.data


@pytest.mark.banking
def test_transfer_post_small_amount_succeeds(client):
    client.post("/login", data={"username": "demo"}, follow_redirects=True)

    accounts = client.get("/api/accounts").get_json()["accounts"]
    checking = next(a for a in accounts if a["account_type"] == "checking")
    savings = next(a for a in accounts if a["account_type"] == "savings")
    checking_before = checking["balance"]
    savings_before = savings["balance"]
    amount = 1.00
    response = client.post(
        "/transfer",
        data={
            "from_account": str(checking["id"]),
            "to_account": str(savings["id"]),
            "amount": str(amount),
            "description": "Pytest transfer",
        },
        follow_redirects=True,
    )
    accounts_after = client.get("/api/accounts").get_json()["accounts"]
    checking_after = next(a for a in accounts_after if a["account_type"] == "checking")
    savings_after = next(a for a in accounts_after if a["account_type"] == "savings")

    assert response.status_code == 200
    assert b"Transfer successful" in response.data
    assert checking_after["balance"] == pytest.approx(checking_before - amount)
    assert savings_after["balance"] == pytest.approx(savings_before + amount)


@pytest.mark.banking
def test_transfer_post_rejects_cross_user_source_account(client):
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
            (f"attacker_{suffix}", f"attacker_{suffix}@example.com", "Attacker User"),
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

    accounts = client.get("/api/accounts").get_json()["accounts"]
    victim_savings = next(a for a in accounts if a["account_type"] == "savings")
    response = client.post(
        "/transfer",
        data={
            "from_account": str(attacker_checking_id),
            "to_account": str(victim_savings["id"]),
            "amount": "10.00",
            "description": "forbidden transfer",
        },
        follow_redirects=True,
    )

    assert response.status_code == 403
    assert b"Forbidden" in response.data
