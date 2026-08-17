"""GET /profile route contract: auth guard, DB-sourced render, fail-closed on stale session."""

import pytest

import models

PROFILE_ADDRESS_CANARY = b"USS Enterprise"


def _demo_user():
    return models.get_user_by_username("demo")


def _demo_created_at(user_id: int) -> str:
    conn = models.get_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            models._sql("SELECT created_at FROM users WHERE id = ?"), (user_id,)
        )
        row = models._row_to_dict(cursor.fetchone())
    finally:
        conn.close()
    return str(row["created_at"])


@pytest.mark.banking
def test_profile_requires_login(client):
    response = client.get("/profile", follow_redirects=False)

    assert response.status_code in (
        302,
        303,
    ), "profile requires authenticated session"
    assert (
        "login" in response.headers.get("Location", "").lower()
    ), "profile requires authenticated session"


@pytest.mark.banking
def test_profile_no_leak_on_redirect(client):
    response = client.get("/profile", follow_redirects=False)

    assert response.status_code in (302, 303), "profile redirect leaks no user data"
    assert (
        PROFILE_ADDRESS_CANARY not in response.data
    ), "profile redirect leaks no user data"


@pytest.mark.banking
def test_profile_renders_all_four_fields(client):
    client.post("/login", data={"username": "demo"}, follow_redirects=True)
    profile = models.get_user_profile(_demo_user()["id"])

    response = client.get("/profile")

    assert response.status_code == 200, "profile renders all four contract fields"
    assert (
        profile["username"].encode() in response.data
    ), "profile renders all four contract fields"
    assert (
        profile["email"].encode() in response.data
    ), "profile renders all four contract fields"
    assert (
        profile["full_name"].encode() in response.data
    ), "profile renders all four contract fields"
    assert (
        PROFILE_ADDRESS_CANARY in response.data
    ), "profile renders all four contract fields"


@pytest.mark.banking
def test_profile_no_internal_columns(client):
    client.post("/login", data={"username": "demo"}, follow_redirects=True)
    created_at = _demo_created_at(_demo_user()["id"])

    response = client.get("/profile")

    assert response.status_code == 200, "profile does not expose internal columns"
    assert created_at, "profile does not expose internal columns"
    assert (
        created_at.encode() not in response.data
    ), "profile does not expose internal columns"


@pytest.mark.banking
def test_profile_stale_session_redirects(client):
    with client.session_transaction() as s:
        s["user_id"] = 99999

    response = client.get("/profile", follow_redirects=False)

    assert response.status_code in (
        302,
        303,
    ), "profile stale session redirects to login"
    assert (
        "login" in response.headers.get("Location", "").lower()
    ), "profile stale session redirects to login"


@pytest.mark.banking
def test_profile_follows_db_not_session(client):
    db_full_name = _demo_user()["full_name"]
    client.post("/login", data={"username": "demo"}, follow_redirects=True)
    with client.session_transaction() as s:
        s["full_name"] = "DIVERGED_VALUE_NOT_IN_DB"

    response = client.get("/profile")

    assert response.status_code == 200, "profile follows DB not session"
    assert db_full_name.encode() in response.data, "profile follows DB not session"
    assert (
        b"DIVERGED_VALUE_NOT_IN_DB" not in response.data
    ), "profile follows DB not session"
