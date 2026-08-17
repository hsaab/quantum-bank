"""Write Data Access Object for transaction creation and management."""

from dao.base_dao import BaseDAO


class WriteDAO(BaseDAO):
    """Write operations: transaction creation, rewards insertion, transfers."""

    def create_transaction_internal(
        self,
        conn,
        account_id: int,
        transaction_type: str,
        amount: float,
        description: str,
        recipient: str = "",
    ) -> int:
        """Create a new transaction (DAO method, receives caller's connection)."""
        from models import _insert_returning_id, _sql

        cursor = conn.cursor()

        transaction_id = _insert_returning_id(
            cursor,
            """
            INSERT INTO transactions (account_id, transaction_type, amount, description, recipient)
            VALUES (?, ?, ?, ?, ?)
            """,
            (account_id, transaction_type, amount, description, recipient),
        )

        cursor.execute(
            _sql("""
                UPDATE accounts
                SET balance = balance + ?
                WHERE id = ?
                """),
            (amount, account_id),
        )

        return transaction_id

    def transfer_internal(
        self,
        conn,
        from_account_id: int,
        to_account_id: int,
        amount: float,
        description: str = "Transfer",
        acting_user_id: int | None = None,
    ) -> tuple[bool, str]:
        """Move money between two accounts (DAO method, receives caller's connection).

        Returns ``(ok, message)``. Never commits, rolls back, or closes: the
        caller owns the connection lifecycle. Amount validation stays in the
        models wrapper so no connection is opened for an invalid amount.
        """
        import models
        from models import _normalize_row, _row_to_dict, _sql

        cursor = conn.cursor()

        cursor.execute(
            _sql("SELECT balance, account_number, user_id FROM accounts WHERE id = ?"),
            (from_account_id,),
        )
        from_account = _normalize_row(_row_to_dict(cursor.fetchone()))

        cursor.execute(
            _sql("SELECT account_number FROM accounts WHERE id = ?"),
            (to_account_id,),
        )
        to_account = _row_to_dict(cursor.fetchone())

        if not from_account or not to_account:
            return False, "Account not found"

        if acting_user_id is not None and from_account["user_id"] != acting_user_id:
            return False, "Forbidden"

        if from_account["balance"] < amount:
            return False, "Insufficient funds"

        cursor.execute(
            _sql("""
                INSERT INTO transactions (account_id, transaction_type, amount, description, recipient)
                VALUES (?, ?, ?, ?, ?)
                """),
            (
                from_account_id,
                "transfer",
                -amount,
                description,
                to_account["account_number"],
            ),
        )

        cursor.execute(
            _sql("UPDATE accounts SET balance = balance - ? WHERE id = ?"),
            (amount, from_account_id),
        )

        cursor.execute(
            _sql("""
                INSERT INTO transactions (account_id, transaction_type, amount, description, recipient)
                VALUES (?, ?, ?, ?, ?)
                """),
            (
                to_account_id,
                "transfer",
                amount,
                description,
                from_account["account_number"],
            ),
        )

        cursor.execute(
            _sql("UPDATE accounts SET balance = balance + ? WHERE id = ?"),
            (amount, to_account_id),
        )

        # Demo-only progressive delivery:
        # writes to rewards_ledger should succeed only after schema is applied.
        cursor.execute("SAVEPOINT rewards_savepoint")
        try:
            # Load-bearing: called through the models module attribute, not a
            # bound import, so monkeypatching models.try_insert_rewards_points
            # still intercepts. Do not hoist this into a `from models import`.
            models.try_insert_rewards_points(
                conn=conn,
                cursor=cursor,
                user_id=from_account["user_id"],
                source_account_id=from_account_id,
                target_account_id=to_account_id,
                transfer_amount=amount,
            )
            cursor.execute("RELEASE SAVEPOINT rewards_savepoint")
        except Exception:
            # Load-bearing: on an aborted PG txn, RELEASE SAVEPOINT raises InFailedSqlTransaction;
            # this except IS the rollback path, not just cleanup — do not collapse this try/except.
            cursor.execute("ROLLBACK TO SAVEPOINT rewards_savepoint")
            cursor.execute("RELEASE SAVEPOINT rewards_savepoint")

        return True, "Transfer successful"

    def insert_rewards_points(
        self,
        *,
        conn,
        cursor,
        user_id: int,
        source_account_id: int,
        target_account_id: int,
        transfer_amount: float,
    ) -> bool:
        """Attempt to insert rewards points; never fail the core transfer (exact copy of current implementation)."""
        from db_flags import is_demo_rollout_feature_enabled
        from models import (
            _resolve_rewards_schema_state,
            _compute_reward_points,
            _sql,
            logger,
        )

        if not is_demo_rollout_feature_enabled():
            return False
        if _resolve_rewards_schema_state(cursor) != "ready":
            return False

        try:
            points = _compute_reward_points(transfer_amount)
            if points <= 0:
                return False

            cursor.execute(
                _sql("""
                    INSERT INTO rewards_ledger
                        (user_id, source_account_id, target_account_id, points)
                    VALUES (?, ?, ?, ?)
                    """),
                (user_id, source_account_id, target_account_id, points),
            )
            logger.info("rewards.rollout.write_succeeded points=%s", points)
            return True
        except Exception as exc:
            logger.warning(
                "rewards.rollout.write_failed reason=%s", exc.__class__.__name__
            )
            return False
