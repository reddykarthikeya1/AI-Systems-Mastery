"""Module 06: MySQL InnoDB Clustered Index & Binlog Replication Engine Reference Solution.

Implements:
1. InnoDB Clustered Index table where the Primary Key directly stores the row data.
2. Secondary Index structure that points to Primary Key values (bookmark lookups).
3. Covering Index detection to bypass the clustered table when all queried columns exist in index.
4. Binlog ROW-event recorder with unique GTID sequence generation.
5. Replica synchronization engine applying binlog events idempotently.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class BinlogEventType(Enum):
    WRITE_ROWS = "WRITE_ROWS"
    UPDATE_ROWS = "UPDATE_ROWS"
    DELETE_ROWS = "DELETE_ROWS"


@dataclass(frozen=True)
class BinlogEvent:
    gtid: str
    event_type: BinlogEventType
    table_name: str
    before_image: dict[str, Any] | None
    after_image: dict[str, Any] | None


class InnoDBClusteredTable:
    """Simulates an InnoDB table with a Clustered Primary Key and Secondary Indexes."""

    def __init__(self, table_name: str, primary_key: str) -> None:
        self.table_name = table_name
        self.primary_key = primary_key
        self._clustered_index: dict[Any, dict[str, Any]] = {}
        self._secondary_indexes: dict[str, dict[Any, Any]] = {}  # col_name -> {val: pk}

    def create_secondary_index(self, column_name: str) -> None:
        """Initializes a secondary index on the specified column."""
        self._secondary_indexes[column_name] = {}
        for pk, row in self._clustered_index.items():
            if column_name in row:
                self._secondary_indexes[column_name][row[column_name]] = pk

    def insert(self, row: dict[str, Any]) -> None:
        """Inserts row into Clustered Index and updates all secondary indexes."""
        if self.primary_key not in row:
            raise KeyError(f"Row missing required primary key: '{self.primary_key}'")

        pk_val = row[self.primary_key]
        if pk_val in self._clustered_index:
            raise ValueError(f"Duplicate entry for primary key: '{pk_val}'")

        # 1. Store directly in Clustered Index
        self._clustered_index[pk_val] = dict(row)

        # 2. Update Secondary Indexes
        for col_name, idx_map in self._secondary_indexes.items():
            if col_name in row:
                idx_map[row[col_name]] = pk_val

    def update(self, pk_value: Any, updates: dict[str, Any]) -> None:
        """Updates row in Clustered Index and maintains secondary indexes."""
        if pk_value not in self._clustered_index:
            raise KeyError(f"Primary key '{pk_value}' does not exist.")

        old_row = self._clustered_index[pk_value]
        new_row = dict(old_row)
        new_row.update(updates)

        # Update secondary indexes if indexed columns changed
        for col_name, idx_map in self._secondary_indexes.items():
            if col_name in updates:
                old_val = old_row.get(col_name)
                if old_val in idx_map:
                    del idx_map[old_val]
                idx_map[new_row[col_name]] = pk_value

        self._clustered_index[pk_value] = new_row

    def delete(self, pk_value: Any) -> None:
        """Deletes row from Clustered Index and all secondary indexes."""
        if pk_value not in self._clustered_index:
            raise KeyError(f"Primary key '{pk_value}' does not exist.")

        old_row = self._clustered_index.pop(pk_value)
        for col_name, idx_map in self._secondary_indexes.items():
            val = old_row.get(col_name)
            if val in idx_map:
                del idx_map[val]

    def get_by_primary_key(self, pk_value: Any) -> dict[str, Any] | None:
        """Direct single-hop lookup in the clustered index."""
        row = self._clustered_index.get(pk_value)
        return dict(row) if row else None

    def get_by_secondary_index(
        self,
        column_name: str,
        value: Any,
        projected_columns: list[str] | None = None,
    ) -> tuple[dict[str, Any] | None, bool]:
        """Looks up row via secondary index.

        Returns (result_dict, was_covering_index).
        """
        if column_name not in self._secondary_indexes:
            raise KeyError(f"No secondary index on column '{column_name}'")

        idx_map = self._secondary_indexes[column_name]
        pk_val = idx_map.get(value)
        if pk_val is None:
            return None, False

        # Check if query can be answered purely by the secondary index (Covering Index)
        # In InnoDB, secondary index leaf stores (index_column_value, primary_key)
        available_in_index = {column_name, self.primary_key}
        if projected_columns and set(projected_columns).issubset(available_in_index):
            # Covering index hit! Bypass clustered index lookup completely.
            result = {col: value if col == column_name else pk_val for col in projected_columns}
            return result, True

        # Secondary Bookmark Lookup: Traverses clustered index to fetch remaining columns
        row = self._clustered_index[pk_val]
        if projected_columns:
            result = {col: row[col] for col in projected_columns if col in row}
        else:
            result = dict(row)

        return result, False


class BinlogReplicationEngine:
    """Manages GTID event streaming and asynchronous replica synchronization."""

    def __init__(self, server_uuid: str) -> None:
        self.server_uuid = server_uuid
        self.sequence = 0
        self.binlog: list[BinlogEvent] = []

    def record_event(
        self,
        event_type: BinlogEventType,
        table_name: str,
        before_image: dict[str, Any] | None,
        after_image: dict[str, Any] | None,
    ) -> BinlogEvent:
        """Appends a new event to the binary log with a sequential GTID."""
        self.sequence += 1
        gtid = f"{self.server_uuid}:{self.sequence}"
        event = BinlogEvent(
            gtid=gtid,
            event_type=event_type,
            table_name=table_name,
            before_image=dict(before_image) if before_image else None,
            after_image=dict(after_image) if after_image else None,
        )
        self.binlog.append(event)
        return event

    def replicate_to(self, replica_table: InnoDBClusteredTable, executed_gtids: set[str]) -> int:
        """Applies unexecuted binlog events to the replica table in strict GTID order."""
        applied_count = 0
        for event in self.binlog:
            if event.gtid in executed_gtids:
                continue

            if event.event_type == BinlogEventType.WRITE_ROWS:
                assert event.after_image is not None
                replica_table.insert(event.after_image)
            elif event.event_type == BinlogEventType.UPDATE_ROWS:
                assert event.after_image is not None
                pk_val = event.after_image[replica_table.primary_key]
                replica_table.update(pk_val, event.after_image)
            elif event.event_type == BinlogEventType.DELETE_ROWS:
                assert event.before_image is not None
                pk_val = event.before_image[replica_table.primary_key]
                replica_table.delete(pk_val)

            executed_gtids.add(event.gtid)
            applied_count += 1

        return applied_count
