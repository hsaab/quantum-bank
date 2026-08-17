"""Base Data Access Object with connection management."""

from models import get_db as models_get_db


class BaseDAO:
    """Base DAO with connection lifecycle management."""

    def __init__(self):
        self.conn = None
        self.cursor = None

    def get_connection(self):
        """Acquire database connection and cursor."""
        self.conn = models_get_db()
        self.cursor = self.conn.cursor()
        return self.cursor

    def close(self):
        """Close connection (safe to call multiple times)."""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
