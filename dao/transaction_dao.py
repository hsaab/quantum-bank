"""Transaction data access object."""

from dao.base_dao import BaseDAO


class TransactionDAO(BaseDAO):
    """Transaction query operations (read-only)."""

    def get_by_account(self, account_id: int, limit: int = 10) -> list[dict]:
        """Get transactions for an account."""
        from models import _sql, _row_to_dict, _normalize_row

        self.get_connection()
        try:
            self.cursor.execute(
                _sql("""
                    SELECT * FROM transactions
                    WHERE account_id = ?
                    ORDER BY created_at DESC
                    LIMIT ?
                    """),
                (account_id, limit),
            )
            transactions = self.cursor.fetchall()
            return [_normalize_row(_row_to_dict(trans)) for trans in transactions]
        finally:
            self.close()

    def get_by_user(self, user_id: int, limit: int = 20) -> list[dict]:
        """Get all transactions for a user across all accounts."""
        from models import _sql, _row_to_dict, _normalize_row

        self.get_connection()
        try:
            self.cursor.execute(
                _sql("""
                    SELECT t.*, a.account_type, a.account_number
                    FROM transactions t
                    JOIN accounts a ON t.account_id = a.id
                    WHERE a.user_id = ?
                    ORDER BY t.created_at DESC
                    LIMIT ?
                    """),
                (user_id, limit),
            )
            transactions = self.cursor.fetchall()
            return [_normalize_row(_row_to_dict(trans)) for trans in transactions]
        finally:
            self.close()

    def get_rewards_for_user(self, user_id: int) -> tuple[int | None, str | None]:
        """Return (points, banner) for UI; rolls back to legacy mode on errors."""
        from db_flags import is_demo_rollout_feature_enabled
        from models import logger, _resolve_rewards_schema_state, _sql, _row_to_dict

        if not is_demo_rollout_feature_enabled():
            return None, None

        self.get_connection()
        try:
            schema_state = _resolve_rewards_schema_state(self.cursor)

            if schema_state == "forced_fail":
                return None, "rollback_forced_fail"
            if schema_state in {"skipped", "unknown"}:
                return None, "legacy_no_schema"
            if schema_state == "runtime_error":
                return None, "rollback_runtime_error"

            try:
                self.cursor.execute(
                    _sql("""
                        SELECT COALESCE(SUM(points), 0) AS points_total
                        FROM rewards_ledger
                        WHERE user_id = ?
                        """),
                    (user_id,),
                )
                row = self.cursor.fetchone()
                data = _row_to_dict(row) or {}
                points_total = data.get("points_total")
                return (
                    int(points_total) if points_total is not None else 0,
                    None,
                )
            except Exception as exc:
                logger.warning(
                    "rewards.rollout.read_failed reason=%s",
                    exc.__class__.__name__,
                )
                return None, "rollback_runtime_error"
        finally:
            self.close()
