"""Helper DAO for rewards schema state machine and validation."""

import logging
from models import using_postgres

logger = logging.getLogger(__name__)

REWARDS_LEDGER_TABLE = "rewards_ledger"


class HelperDAO:
    """Rewards schema helpers: validation (state machine stays in models.py for global state)."""

    @staticmethod
    def rewards_ledger_table_exists(cursor) -> bool:
        """Check if rewards_ledger table exists."""
        from models import _row_to_dict

        if using_postgres():
            cursor.execute(
                """
                SELECT EXISTS (
                    SELECT 1 FROM information_schema.tables
                    WHERE table_schema = 'public'
                      AND table_name = %s
                ) AS exists
            """,
                (REWARDS_LEDGER_TABLE,),
            )
            row = _row_to_dict(cursor.fetchone())
            return bool(row.get("exists")) if row else False
        else:
            cursor.execute(
                """
                SELECT 1
                FROM sqlite_master
                WHERE type = 'table'
                  AND name = ?
                LIMIT 1
            """,
                (REWARDS_LEDGER_TABLE,),
            )
            return cursor.fetchone() is not None
