import os
import sqlite3
import tempfile

import pytest


def pytest_configure(config):
    """Stable env before lazy `from app import app` in the client fixture."""
    os.environ.setdefault("SECRET_KEY", "pytest-secret-key")
    os.environ.setdefault("POSTGRES_DATABASE", "off")
    if "QUANTUM_BANK_DATABASE" not in os.environ:
        _fd, path = tempfile.mkstemp(suffix=".sqlite")
        os.close(_fd)
        os.environ["QUANTUM_BANK_DATABASE"] = path


@pytest.fixture
def split_unavailable(monkeypatch):
    """Flag logic tests use env only — Split is an external boundary."""
    monkeypatch.setattr("db_flags.get_split_client", lambda: None)


@pytest.fixture
def client():
    """HTTP client against the Flask app (same process, no network)."""
    from app import app

    testing_enabled = os.environ.get("FLASK_TESTING", "1").lower() in {
        "1",
        "true",
        "yes",
        "on",
    }
    app.testing = testing_enabled
    with app.test_client() as c:
        yield c


@pytest.fixture
def rollout_env(monkeypatch):
    """Reset rollout flags so scenarios cannot leak state."""
    for key in (
        "DEMO_ROLLOUT_SCHEMA",
        "DEMO_ROLLOUT_FEATURE",
        "DEMO_FORCE_ROLLOUT_MIGRATION_FAIL",
    ):
        monkeypatch.delenv(key, raising=False)
    yield


@pytest.fixture
def rewards_ledger_clean():
    """Drop rewards table and clear cache after each test."""
    yield

    use_pg = os.environ.get("POSTGRES_DATABASE", "off").lower() in {
        "on",
        "true",
        "1",
        "yes",
    } and bool(os.environ.get("DATABASE_URL"))

    if use_pg:
        import psycopg2

        conn = psycopg2.connect(os.environ["DATABASE_URL"])
        try:
            with conn.cursor() as cursor:
                cursor.execute("DROP TABLE IF EXISTS rewards_ledger")
            conn.commit()
        finally:
            conn.close()
    else:
        conn = sqlite3.connect(os.environ["QUANTUM_BANK_DATABASE"])
        try:
            conn.execute("DROP TABLE IF EXISTS rewards_ledger")
            conn.commit()
        finally:
            conn.close()

    import models

    if hasattr(models, "_rewards_schema_state"):
        models._rewards_schema_state = "unknown"
