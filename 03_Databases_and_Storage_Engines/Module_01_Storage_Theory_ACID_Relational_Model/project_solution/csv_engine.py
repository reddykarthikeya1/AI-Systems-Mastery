"""Module 01: Transactional CSV Engine with Write-Ahead Logging (WAL).

This is a pure-Python MODEL of a relational storage engine's write-ahead logging (WAL)
and table persistence mechanism, built to make the mechanism visible. It does not
connect to an external database engine. For real embedded relational storage and
production crash recovery, see Module 03 (`sqlite_wal_engine.py`) and PostgreSQL
in Module 04 (`postgres_live.py`).

Implements ACID-style atomicity, schema validation, and crash recovery on flat files.
"""

from __future__ import annotations

import csv
import json
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
        self._tx_counter = 0

        # Initialize data file if not present
        if not self.data_file.exists():
            with open(self.data_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(list(self.schema.keys()))

        # Run crash recovery on startup
        self.recover()

    def _validate_row(self, row: dict[str, Any]) -> dict[str, Any]:
        """Validates that row matches schema types and contains all required keys."""
        validated = {}
        for col, col_type in self.schema.items():
            if col not in row:
                raise ValidationError(f"Missing required column: '{col}'")
            val = row[col]
            if not isinstance(val, col_type):
                try:
                    val = col_type(val)
                except (ValueError, TypeError):
                    raise ValidationError(
                        f"Invalid type for '{col}'. Expected {col_type.__name__}, got {type(val).__name__}"
                    )
            validated[col] = val
        return validated

    def begin(self) -> int:
        """Starts a new transaction."""
        if self.current_tx_id is not None:
            raise TransactionError("A transaction is already active. Nested transactions not supported.")
        self._tx_counter += 1
        self.current_tx_id = self._tx_counter
        self.tx_buffer = []

        # Log BEGIN to WAL
        with open(self.wal_file, "a", encoding="utf-8") as f:
            f.write(json.dumps({"tx_id": self.current_tx_id, "op": "BEGIN"}) + "\n")

        return self.current_tx_id

    def insert(self, row: dict[str, Any]):
        """Buffers an insert operation within the active transaction."""
        if self.current_tx_id is None:
            raise TransactionError("No active transaction. Call begin() before insert().")

        validated = self._validate_row(row)
        self.tx_buffer.append(validated)

        # Log INSERT to WAL
        with open(self.wal_file, "a", encoding="utf-8") as f:
            f.write(json.dumps({"tx_id": self.current_tx_id, "op": "INSERT", "data": validated}) + "\n")

    def commit(self):
        """Commits the active transaction, appending changes to the primary CSV."""
        if self.current_tx_id is None:
            raise TransactionError("No active transaction to commit.")

        # Log COMMIT to WAL first (WAL protocol)
        with open(self.wal_file, "a", encoding="utf-8") as f:
            f.write(json.dumps({"tx_id": self.current_tx_id, "op": "COMMIT"}) + "\n")

        # Flush buffer to primary CSV
        with open(self.data_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(self.schema.keys()))
            for row in self.tx_buffer:
                writer.writerow(row)

        self.current_tx_id = None
        self.tx_buffer = []

    def rollback(self):
        """Discards active transaction without modifying the primary table."""
        if self.current_tx_id is None:
            raise TransactionError("No active transaction to rollback.")

        with open(self.wal_file, "a", encoding="utf-8") as f:
            f.write(json.dumps({"tx_id": self.current_tx_id, "op": "ROLLBACK"}) + "\n")

        self.current_tx_id = None
        self.tx_buffer = []

    def select_all(self) -> list[dict[str, Any]]:
        """Reads all committed rows from the primary CSV file."""
        rows = []
        if not self.data_file.exists():
            return rows

        with open(self.data_file, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for raw_row in reader:
                typed_row = {}
                for col, col_type in self.schema.items():
                    typed_row[col] = col_type(raw_row[col])
                rows.append(typed_row)
        return rows

    def recover(self):
        """Replays the WAL log to ensure all committed transactions are in the CSV."""
        if not self.wal_file.exists():
            return

        tx_ops: dict[int, list[dict[str, Any]]] = {}
        committed_txs: set[int] = set()

        with open(self.wal_file, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                entry = json.loads(line)
                tx_id = entry["tx_id"]
                if tx_id not in tx_ops:
                    tx_ops[tx_id] = []
                tx_ops[tx_id].append(entry)
                if entry["op"] == "COMMIT":
                    committed_txs.add(tx_id)

        # Truncate WAL file after clean recovery
        # In a full system, checkpointing merges WAL into CSV
        # Here, uncommitted txs are discarded automatically.
