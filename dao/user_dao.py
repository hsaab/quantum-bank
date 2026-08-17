"""User data access object."""

from dao.base_dao import BaseDAO


class UserDAO(BaseDAO):
    """User query operations (read-only)."""

    def get_by_username(self, username: str) -> dict | None:
        """Get user by username."""
        from models import _sql, _row_to_dict

        self.get_connection()
        try:
            self.cursor.execute(
                _sql("SELECT * FROM users WHERE username = ?"),
                (username,),
            )
            user = self.cursor.fetchone()
            return _row_to_dict(user)
        finally:
            self.close()

    def get_profile(self, user_id: int) -> dict | None:
        """Get user profile (display-safe columns only)."""
        from models import PROFILE_DEMO_ADDRESS as address_constant, _sql, _row_to_dict

        self.get_connection()
        try:
            self.cursor.execute(
                _sql("SELECT username, email, full_name FROM users WHERE id = ?"),
                (user_id,),
            )
            row = self.cursor.fetchone()
            if row is None:
                return None
            profile = _row_to_dict(row)
            profile["address"] = address_constant
            return profile
        finally:
            self.close()
