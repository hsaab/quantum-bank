"""Feature-flag resolution for the postgres_database backend switch."""

from __future__ import annotations

import logging
import os

from split_config import get_split_client

logger = logging.getLogger(__name__)

_ON_VALUES = frozenset({"on", "true", "1", "yes"})
_OFF_VALUES = frozenset({"off", "false", "0", "no"})


def _env_postgres_enabled() -> bool:
    return os.environ.get("POSTGRES_DATABASE", "off").lower() in _ON_VALUES


def is_postgres_database_enabled(user_key: str = "__system__") -> bool:
    """Resolve the postgres_database flag: Split → env → default(off).

    Returns True only when the flag is on *and* ``DATABASE_URL`` is set (D1).
    If the flag is on but ``DATABASE_URL`` is missing, logs a warning and returns False.
    """
    flag_on: bool | None = None

    split_client = get_split_client()
    if split_client and user_key:
        try:
            treatment = split_client.get_treatment(user_key, "postgres_database")
            logger.debug(
                "Split.io flag 'postgres_database' = %r (user: %s)",
                treatment,
                user_key,
            )
            if treatment in _ON_VALUES:
                flag_on = True
            elif treatment in _OFF_VALUES:
                return False
            elif treatment == "control":
                logger.debug(
                    "Split.io returned 'control' for postgres_database — using env var"
                )
            else:
                logger.debug(
                    "Unknown Split treatment %r for postgres_database — using env var",
                    treatment,
                )
        except Exception as exc:
            logger.warning(
                "Error getting Split.io treatment for postgres_database: %s — using env var",
                exc,
            )

    if flag_on is None:
        flag_on = _env_postgres_enabled()

    if not flag_on:
        return False

    if not os.environ.get("DATABASE_URL"):
        logger.warning(
            "postgres_database is on but DATABASE_URL is not set — staying on SQLite"
        )
        return False

    return True


def _env_enabled(var_name: str, default: str = "off") -> bool:
    return os.environ.get(var_name, default).lower() in _ON_VALUES


# Demo-only progressive rollout flags (env-driven on purpose).
# Defaults are OFF so existing app behavior stays unchanged.
DEMO_ROLLOUT_SCHEMA_ENV = "DEMO_ROLLOUT_SCHEMA"
DEMO_ROLLOUT_FEATURE_ENV = "DEMO_ROLLOUT_FEATURE"
DEMO_FORCE_MIGRATION_FAIL_ENV = "DEMO_FORCE_ROLLOUT_MIGRATION_FAIL"


def is_demo_rollout_schema_enabled() -> bool:
    """Whether to allow applying the demo schema change (idempotent)."""
    return _env_enabled(DEMO_ROLLOUT_SCHEMA_ENV, "off")


def is_demo_rollout_feature_enabled() -> bool:
    """Whether the demo feature should read/write the new schema."""
    return _env_enabled(DEMO_ROLLOUT_FEATURE_ENV, "off")


def is_demo_force_rollout_migration_fail() -> bool:
    """If enabled, the migration will intentionally fail (for demo/rollback)."""
    return _env_enabled(DEMO_FORCE_MIGRATION_FAIL_ENV, "off")
