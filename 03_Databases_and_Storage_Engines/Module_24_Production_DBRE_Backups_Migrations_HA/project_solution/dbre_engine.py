"""Module 24: Production DBRE, PITR & Zero-Downtime Migrations (Solution).

This is a pure-Python MODEL of database reliability engineering (DBRE) operations including PITR, WAL archiving, and zero-downtime migrations, built to make the
mechanism visible. It does not connect to a production database cluster. For real pg_dump/restore,
real replication, and real operational behaviour, see `dbre_live.py`.

Implements:
1. ContinuousWALArchiver tracking LSN sequences and timestamps.
2. PITRRecoveryEngine: Point-in-Time Recovery replaying WAL up to exact microsecond targets.
3. ExpandContractMigrator: 5-phase zero-downtime schema evolution pipeline.
4. TransactionConnectionPooler: PgBouncer-style connection pool management.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


class ConnectionPoolExhaustedError(Exception):
    """Raised when maximum server connection limit has been reached."""


class WALRecord:
    """A Write-Ahead Log entry with LSN and timestamp."""

    def __init__(
        self,
        lsn: int,
        timestamp_us: int,
        op_type: str,
        table_name: str,
        row_id: str,
        payload: dict[str, Any],
    ) -> None:
        self.lsn = lsn
        self.timestamp_us = timestamp_us
        self.op_type = op_type
        self.table_name = table_name
        self.row_id = row_id
        self.payload = dict(payload)

    def __repr__(self) -> str:
        return f"WAL(lsn={self.lsn}, t={self.timestamp_us}, op={self.op_type}, row={self.row_id})"


class ContinuousWALArchiver:
    """Manages sequential WAL record appending and shipping."""

    def __init__(self) -> None:
        self.records: list[WALRecord] = []
        self.next_lsn: int = 1

    def append(
        self,
        op_type: str,
        table_name: str,
        row_id: str,
        payload: dict[str, Any],
        timestamp_us: int,
    ) -> WALRecord:
        record = WALRecord(
            lsn=self.next_lsn,
            timestamp_us=timestamp_us,
            op_type=op_type,
            table_name=table_name,
            row_id=row_id,
            payload=payload,
        )
        self.records.append(record)
        self.next_lsn += 1
        return record


class PITRRecoveryEngine:
    """Executes physical base backup restoration and Point-in-Time WAL roll-forward."""

    def __init__(self) -> None:
        self.backups: dict[int, tuple[dict[str, dict[str, Any]], int]] = {}
        self.next_backup_id: int = 1

    def take_base_backup(self, tables: dict[str, dict[str, Any]], timestamp_us: int) -> int:
        snapshot = {
            tbl: {rid: dict(row) for rid, row in rows.items()}
            for tbl, rows in tables.items()
        }
        bid = self.next_backup_id
        self.backups[bid] = (snapshot, timestamp_us)
        self.next_backup_id += 1
        return bid

    def restore_to_timestamp(
        self,
        backup_id: int,
        target_timestamp_us: int,
        wal_stream: list[WALRecord],
    ) -> dict[str, dict[str, Any]]:
        if backup_id not in self.backups:
            raise KeyError(f"Base backup {backup_id} not found in catalog")

        base_tables, _ = self.backups[backup_id]
        restored = {
            tbl: {rid: dict(row) for rid, row in rows.items()}
            for tbl, rows in base_tables.items()
        }

        for w in wal_stream:
            # Stop replay at target recovery boundary!
            if w.timestamp_us > target_timestamp_us:
                break

            if w.op_type in ("INSERT", "UPDATE"):
                if w.table_name not in restored:
                    restored[w.table_name] = {}
                restored[w.table_name][w.row_id] = dict(w.payload)
            elif w.op_type == "DELETE":
                if w.table_name in restored and w.row_id in restored[w.table_name]:
                    del restored[w.table_name][w.row_id]
            elif w.op_type == "DROP_TABLE":
                if w.table_name in restored:
                    del restored[w.table_name]

        return restored


class ExpandContractMigrator:
    """Coordinates the 5-phase zero-downtime column migration pipeline."""

    @staticmethod
    def expand_add_column(rows: list[dict[str, Any]], new_column: str) -> None:
        for r in rows:
            if new_column not in r:
                r[new_column] = None

    @staticmethod
    def dual_write_insert(
        rows: list[dict[str, Any]],
        row_data: dict[str, Any],
        old_col: str,
        new_col: str,
    ) -> None:
        val = row_data.get(old_col) if old_col in row_data else row_data.get(new_col)
        item = dict(row_data)
        item[old_col] = val
        item[new_col] = val
        rows.append(item)

    @staticmethod
    def backfill_batch(
        rows: list[dict[str, Any]],
        old_col: str,
        new_col: str,
        transform: Callable[[Any], Any] | None = None,
        batch_size: int = 2,
    ) -> int:
        """Copy `old_col` into `new_col` for up to `batch_size` rows.

        `transform` exists because an expand/contract migration is rarely a
        straight copy: splitting `full_name` into `first_name`, normalising a
        currency, or widening a type all need a per-value function. Without it
        the model could only express the trivial case, which is not the case
        anyone actually performs.

        Batching matters for the same reason it matters in SQL: a single
        `UPDATE` over ten million rows holds locks and bloats the WAL. Real
        backfills run in bounded batches with a pause between them, which is
        why this returns the number updated so the caller can loop.
        """
        updated = 0
        for r in rows:
            if r.get(new_col) is None and r.get(old_col) is not None:
                source = r[old_col]
                r[new_col] = transform(source) if transform is not None else source
                updated += 1
                if updated >= batch_size:
                    break
        return updated

    @staticmethod
    def contract_drop_column(rows: list[dict[str, Any]], old_col: str) -> None:
        for r in rows:
            if old_col in r:
                del r[old_col]


class TransactionConnectionPooler:
    """Manages transaction-level client connection pooling."""

    def __init__(self, max_connections: int = 5) -> None:
        self.max_connections = max_connections
        self.available_connections: list[int] = list(range(1, max_connections + 1))
        self.in_use_connections: set[int] = set()

    def acquire(self) -> int:
        if not self.available_connections:
            raise ConnectionPoolExhaustedError(
                f"Connection pool exhausted (all {self.max_connections} connections in use)"
            )
        conn_id = self.available_connections.pop(0)
        self.in_use_connections.add(conn_id)
        return conn_id

    def release(self, conn_id: int) -> None:
        if conn_id in self.in_use_connections:
            self.in_use_connections.remove(conn_id)
            self.available_connections.append(conn_id)
