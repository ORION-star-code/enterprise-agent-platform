from __future__ import annotations


class MySQLClient:
    """MySQL client stub. Not implemented in MVP.

    Will connect to business-service MySQL database when available.
    """

    def __init__(self, dsn: str | None = None) -> None:
        self.dsn = dsn

    async def execute(self, query: str, params: tuple | None = None) -> list:
        """Execute a SQL query. Stub returns empty list."""
        return []
