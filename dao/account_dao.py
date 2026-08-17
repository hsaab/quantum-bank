"""Account data access object."""

from dao.base_dao import BaseDAO


class AccountDAO(BaseDAO):
    """Account query operations (read-only)."""

    def get_by_user(self, user_id: int) -> list[dict]:
        """Get all accounts for a user."""
        from models import _sql, _row_to_dict, _normalize_row

        self.get_connection()
        try:
            self.cursor.execute(
                _sql("SELECT * FROM accounts WHERE user_id = ? ORDER BY created_at"),
                (user_id,),
            )
            accounts = self.cursor.fetchall()
            return [_normalize_row(_row_to_dict(account)) for account in accounts]
        finally:
            self.close()

    def get_by_id(self, account_id: int) -> dict | None:
        """Get account by ID."""
        from models import _sql, _row_to_dict, _normalize_row

        self.get_connection()
        try:
            self.cursor.execute(
                _sql("SELECT * FROM accounts WHERE id = ?"),
                (account_id,),
            )
            account = self.cursor.fetchone()
            return _normalize_row(_row_to_dict(account))
        finally:
            self.close()

    def get_cards_by_account(self, account_id: int) -> list[dict]:
        """Get cards for an account."""
        from models import _sql, _row_to_dict, _normalize_row

        self.get_connection()
        try:
            self.cursor.execute(
                _sql("SELECT * FROM cards WHERE account_id = ?"),
                (account_id,),
            )
            cards = self.cursor.fetchall()
            return [_normalize_row(_row_to_dict(card)) for card in cards]
        finally:
            self.close()
