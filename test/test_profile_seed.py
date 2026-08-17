"""Demo seed identity contract: the seeded demo user is Jean-Luc Picard."""

import pytest

import models

PROFILE_ADDRESS_CANARY = b"USS Enterprise NCC-1701-D"


@pytest.fixture(scope="module", autouse=True)
def seeded_demo_user():
    """Seed the session temp DB so the demo user exists standalone."""
    models.init_db()


@pytest.mark.banking
def test_seed_identity_is_picard():
    user = models.get_user_by_username("demo")

    assert user is not None, "seeded identity is Jean-Luc Picard"
    assert user["full_name"] == "Jean-Luc Picard", "seeded identity is Jean-Luc Picard"
    assert (
        user["email"] == "jpicard@starfleet.fed"
    ), "seeded identity is Jean-Luc Picard"


@pytest.mark.banking
def test_login_with_demo_still_works(client):
    response = client.post("/login", data={"username": "demo"}, follow_redirects=False)

    assert response.status_code in (
        302,
        303,
    ), "login with demo still succeeds after seed change"
    assert (
        "dashboard" in response.headers.get("Location", "").lower()
    ), "login with demo still succeeds after seed change"


@pytest.mark.banking
def test_profile_shows_picard_identity(client):
    client.post("/login", data={"username": "demo"}, follow_redirects=True)

    response = client.get("/profile")

    assert response.status_code == 200, "profile shows Picard identity per A1"
    assert b"Jean-Luc Picard" in response.data, "profile shows Picard identity per A1"
    assert (
        b"jpicard@starfleet.fed" in response.data
    ), "profile shows Picard identity per A1"
    assert (
        PROFILE_ADDRESS_CANARY in response.data
    ), "profile shows Picard identity per A1"
