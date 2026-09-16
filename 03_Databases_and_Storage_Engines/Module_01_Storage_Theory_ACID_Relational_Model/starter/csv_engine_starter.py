"""Module 01 Starter Skeleton: Transactional Flat-File CSV Engine.

Complete the TODO sections to implement BEGIN, COMMIT, ROLLBACK, and WAL Recovery.
"""

from __future__ import annotations
from pathlib import Path
from typing import Any

class TransactionalCSVEngineStarter:
    def __init__(self, data_path: str | Path):
        self.data_path = Path(data_path)
        self.wal_path = self.data_path.with_suffix(".wal")
        self.in_transaction = False
        self.uncommitted_rows: list[dict[str, Any]] = []
        self._recover_wal()

    def _recover_wal(self) -> None:
        # TODO: Check if self.wal_path exists.
        # If it has a BEGIN and COMMIT, replay to CSV. If incomplete, discard.
        pass

    def begin(self) -> None:
        if self.in_transaction:
            raise RuntimeError("Transaction already in progress")
        self.in_transaction = True
        self.uncommitted_rows = []
        with open(self.wal_path, "a", encoding="utf-8") as f:
            f.write("BEGIN\n")

    def insert(self, row: dict[str, Any]) -> None:
        if not self.in_transaction:
            raise RuntimeError("Must call begin() before insert()")
        self.uncommitted_rows.append(row)
        # TODO: Append ROW entry to WAL

    def commit(self) -> None:
        if not self.in_transaction:
            raise RuntimeError("No active transaction to commit")
        # TODO: Write COMMIT to WAL, flush uncommitted_rows to CSV, truncate WAL
        self.in_transaction = False

    def rollback(self) -> None:
        if not self.in_transaction:
            raise RuntimeError("No active transaction to rollback")
        # TODO: Truncate/remove WAL, clear uncommitted_rows
        self.in_transaction = False
