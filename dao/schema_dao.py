"""Schema Data Access Object (initialization and seeding)."""

from dao.base_dao import BaseDAO


class SchemaDAO(BaseDAO):
    """Schema creation, validation, and sample data seeding."""

    def ensure_rewards_ledger_schema(
        self, conn, cursor=None, *, commit: bool = True
    ) -> str:
        """Ensure the rewards ledger table exists (idempotent).

        Returns a small status string for UX/demo messaging.
        """
        from models import (
            is_demo_rollout_schema_enabled,
            is_demo_force_rollout_migration_fail,
            _rewards_ledger_table_exists,
            using_postgres,
        )

        if not is_demo_rollout_schema_enabled():
            return "skipped_schema_off"

        if is_demo_force_rollout_migration_fail():
            raise RuntimeError("intentional demo migration failure")

        cursor = cursor or conn.cursor()
        if _rewards_ledger_table_exists(cursor):
            return "exists"

        if using_postgres():
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS rewards_ledger (
                    id                  SERIAL PRIMARY KEY,
                    user_id             INTEGER NOT NULL REFERENCES users(id),
                    source_account_id  INTEGER NOT NULL REFERENCES accounts(id),
                    target_account_id  INTEGER NOT NULL REFERENCES accounts(id),
                    points              INTEGER NOT NULL,
                    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
                );
                """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_rewards_ledger_user_id
                ON rewards_ledger(user_id);
                """)
        else:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS rewards_ledger (
                    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id            INTEGER NOT NULL,
                    source_account_id INTEGER NOT NULL,
                    target_account_id INTEGER NOT NULL,
                    points             INTEGER NOT NULL,
                    created_at         TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """)

        if commit:
            conn.commit()
        return "applied"

    def init(self):
        """Initialize the database with tables and sample data."""
        from models import (
            get_db,
            _apply_postgres_schema,
            _create_sqlite_schema,
            using_postgres,
            _sql,
            _scalar_from_row,
            logger,
        )

        global_state = {"rewards_schema_state": "unknown"}

        conn = get_db()
        cursor = conn.cursor()

        if using_postgres():
            _apply_postgres_schema(conn)
        else:
            _create_sqlite_schema(cursor)
            conn.commit()

        try:
            schema_status = self.ensure_rewards_ledger_schema(conn, cursor, commit=True)
            if schema_status in {"applied", "exists"}:
                global_state["rewards_schema_state"] = "ready"
            elif schema_status == "skipped_schema_off":
                global_state["rewards_schema_state"] = "skipped"
            else:
                global_state["rewards_schema_state"] = "runtime_error"
        except RuntimeError as exc:
            if str(exc) == "intentional demo migration failure":
                global_state["rewards_schema_state"] = "forced_fail"
            else:
                global_state["rewards_schema_state"] = "runtime_error"
                logger.warning("Rewards schema setup failed at startup: %s", exc)
        except Exception as exc:
            global_state["rewards_schema_state"] = "runtime_error"
            logger.warning("Rewards schema setup failed at startup: %s", exc)

        logger.info(
            "rewards.rollout.schema state=%s", global_state["rewards_schema_state"]
        )

        # Update module-level state
        import models

        models._rewards_schema_state = global_state["rewards_schema_state"]

        cursor.execute(_sql("SELECT COUNT(*) FROM users"))
        if _scalar_from_row(cursor.fetchone()) == 0:
            self.seed(conn)

        conn.close()

    def seed(self, conn):
        """Create sample users and accounts for demo purposes."""
        from models import _insert_returning_id, _sql

        cursor = conn.cursor()

        user_id = _insert_returning_id(
            cursor,
            """
            INSERT INTO users (username, email, full_name)
            VALUES (?, ?, ?)
            """,
            ("demo", "jpicard@starfleet.fed", "Jean-Luc Picard"),
        )

        checking_id = _insert_returning_id(
            cursor,
            """
            INSERT INTO accounts (user_id, account_type, account_number, balance)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, "checking", "QB-CHK-100001", 5420.50),
        )

        _insert_returning_id(
            cursor,
            """
            INSERT INTO accounts (user_id, account_type, account_number, balance)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, "savings", "QB-SAV-200001", 12850.75),
        )

        _insert_returning_id(
            cursor,
            """
            INSERT INTO accounts (user_id, account_type, account_number, balance)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, "credit", "QB-CCC-300001", -500.00),
        )

        cursor.execute(
            _sql("""
                INSERT INTO cards (account_id, card_type, card_last4, expiry_date)
                VALUES (?, ?, ?, ?)
                """),
            (checking_id, "debit", "1234", "12/2026"),
        )

        conn.commit()
