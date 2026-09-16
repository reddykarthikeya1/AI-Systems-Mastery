"""Module 01 Starter Skeleton: Transactional Flat-File CSV Engine.

Complete the TODO sections to implement BEGIN, COMMIT, ROLLBACK, and WAL Recovery.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


class ValidationError(Exception):
    """Raised when data violates table schema."""
    pass


class TransactionError(Exception):
    """Raised when transaction state is invalid."""
    pass


class TransactionalCSVEngine:
    def __init__(self, table_name: str, schema: dict[str, type], base_dir: Path | str = "."):
        self.table_name = table_name
        self.schema = schema
        self.base_dir = Path(base_dir)
        self.data_file = self.base_dir / f"{table_name}.csv"
        self.wal_file = self.base_dir / f"{table_name}.wal"
        self.current_tx_id: int | None = None
        self.tx_buffer: list[dict[str, Any]] = []

    def begin(self) -> int:
        """Starts a new transaction."""
        raise NotImplementedError("TODO: Implement begin()")

    def insert(self, row: dict[str, Any]):
        """Buffers an insert operation within the active transaction."""
        raise NotImplementedError("TODO: Implement insert()")

    def commit(self):
        """Commits the active transaction, appending changes to primary CSV."""
        raise NotImplementedError("TODO: Implement commit()")

    def rollback(self):
        """Discards active transaction without modifying primary table."""
        raise NotImplementedError("TODO: Implement rollback()")

    def select_all(self) -> list[dict[str, Any]]:
        """Reads all committed rows from the primary CSV file."""
        raise NotImplementedError("TODO: Implement select_all()")

    def recover(self):
        """Replays WAL log on startup."""
        raise NotImplementedError("TODO: Implement recover()")
