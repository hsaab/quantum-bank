"""Profile read model contract: named-column projection for the account page."""

import pytest

import models


@pytest.fixture(scope="module", autouse=True)
def seeded_demo_user():
    """Seed the session temp DB so the demo user (id=1) exists standalone."""
    models.init_db()


def _profile_fn():
    return getattr(models, "get_user_profile", None)


@pytest.mark.models
def test_profile_returns_contract_keys():
    fn = _profile_fn()
    assert (
        fn is not None
    ), "get_user_profile not implemented: profile key-set equals contract"

    result = fn(1)

    assert set(result.keys()) == {
        "username",
        "email",
        "full_name",
        "address",
    }, "profile key-set equals contract"


@pytest.mark.models
def test_profile_returns_none_for_unknown_user():
    fn = _profile_fn()
    assert (
        fn is not None
    ), "get_user_profile not implemented: profile returns None for unknown user"

    assert fn(99999) is None, "profile returns None for unknown user"


@pytest.mark.models
def test_profile_address_non_empty():
    fn = _profile_fn()
    assert (
        fn is not None
    ), "get_user_profile not implemented: profile address is non-empty"

    result = fn(1)

    assert isinstance(result["address"], str), "profile address is non-empty"
    assert result["address"], "profile address is non-empty"
