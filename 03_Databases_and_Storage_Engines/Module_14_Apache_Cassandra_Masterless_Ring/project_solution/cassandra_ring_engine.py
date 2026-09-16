"""Module 14: Apache Cassandra Masterless Ring & Tunable Quorum (Solution).

This is a pure-Python MODEL of Apache Cassandra's token ring, consistent hashing, and tunable quorum replication, built to make the
mechanism visible. It does not connect to Apache Cassandra. For the real driver,
real queries and real operational behaviour, see `cassandra_live.py`.

Implements:
1. 64-bit Consistent Hashing Token Ring with natural replica endpoint selection.
2. Last-Write-Wins (LWW) conflict resolution and Tombstone soft deletions.
3. Tunable consistency levels (ONE, QUORUM, ALL) for reads and writes.
4. Active Read Repair reconciling stale replica nodes during read coordination.
"""

from __future__ import annotations

import hashlib
import struct
import time
from typing import Any, Literal

ConsistencyLevel = Literal["ONE", "QUORUM", "ALL"]


class WriteTimeoutError(Exception):
    """Raised when the required write consistency level could not be satisfied."""


class ReadTimeoutError(Exception):
    """Raised when the required read consistency level could not be satisfied."""


class CassandraRow:
    """Represents a row stored inside an SSTable/MemTable partition."""

    def __init__(
        self,
        partition_key: str,
        clustering_key: str,
        data: dict[str, Any],
        timestamp_us: int,
        is_tombstone: bool = False,
    ) -> None:
        self.partition_key = partition_key
        self.clustering_key = clustering_key
        self.data = data
        self.timestamp_us = timestamp_us
        self.is_tombstone = is_tombstone


class CassandraStorageNode:
    """An individual storage node in the Cassandra cluster hosting SSTables and MemTables."""

    def __init__(self, node_id: str, token: int) -> None:
        self.node_id = node_id
        self.token = token
        self.store: dict[tuple[str, str], CassandraRow] = {}
        self.is_online: bool = True

    def write_row(self, row: CassandraRow) -> bool:
        if not self.is_online:
            return False

        key = (row.partition_key, row.clustering_key)
        if key in self.store:
            # Last-Write-Wins: overwrite only if incoming timestamp is newer
            if row.timestamp_us >= self.store[key].timestamp_us:
                self.store[key] = row
        else:
            self.store[key] = row

        return True

    def read_row(self, partition_key: str, clustering_key: str) -> CassandraRow | None:
        if not self.is_online:
            return None
        return self.store.get((partition_key, clustering_key))


class CassandraRingCoordinator:
    """Coordinates consistent hashing token ring, natural endpoints, and tunable quorum."""

    def __init__(self, replication_factor: int = 3) -> None:
        self.replication_factor = replication_factor
        self.nodes: dict[str, CassandraStorageNode] = {}

    def add_node(self, node_id: str, token: int) -> None:
        self.nodes[node_id] = CassandraStorageNode(node_id=node_id, token=token)

    @staticmethod
    def hash_partition_key(partition_key: str) -> int:
        digest = hashlib.md5(partition_key.encode("utf-8")).digest()
        (token,) = struct.unpack(">q", digest[:8])
        return token

    def get_natural_endpoints(self, partition_key: str) -> list[CassandraStorageNode]:
        if not self.nodes:
            return []

        sorted_nodes = sorted(self.nodes.values(), key=lambda n: n.token)
        token = self.hash_partition_key(partition_key)

        # Find first node with token >= key token (clockwise traversal)
        start_idx = 0
        for idx, node in enumerate(sorted_nodes):
            if node.token >= token:
                start_idx = idx
                break

        # Collect replication_factor distinct physical nodes clockwise
        endpoints: list[CassandraStorageNode] = []
        num_nodes = len(sorted_nodes)
        count = min(self.replication_factor, num_nodes)

        for i in range(count):
            endpoints.append(sorted_nodes[(start_idx + i) % num_nodes])

        return endpoints

    def _required_acks(self, consistency: ConsistencyLevel) -> int:
        if consistency == "ONE":
            return 1
        elif consistency == "QUORUM":
            return (self.replication_factor // 2) + 1
        elif consistency == "ALL":
            return self.replication_factor
        raise ValueError(f"Unknown consistency level: {consistency}")

    def write(
        self,
        partition_key: str,
        clustering_key: str,
        data: dict[str, Any],
        consistency: ConsistencyLevel = "QUORUM",
        timestamp_us: int | None = None,
    ) -> bool:
        if timestamp_us is None:
            timestamp_us = int(time.time() * 1_000_000)

        row = CassandraRow(
            partition_key=partition_key,
            clustering_key=clustering_key,
            data=data,
            timestamp_us=timestamp_us,
            is_tombstone=False,
        )

        endpoints = self.get_natural_endpoints(partition_key)
        required = self._required_acks(consistency)
        acks = 0

        for node in endpoints:
            if node.write_row(row):
                acks += 1

        if acks < required:
            raise WriteTimeoutError(
                f"Write consistency {consistency} required {required} acks, received {acks}"
            )
        return True

    def delete(
        self,
        partition_key: str,
        clustering_key: str,
        consistency: ConsistencyLevel = "QUORUM",
        timestamp_us: int | None = None,
    ) -> bool:
        if timestamp_us is None:
            timestamp_us = int(time.time() * 1_000_000)

        tombstone = CassandraRow(
            partition_key=partition_key,
            clustering_key=clustering_key,
            data={},
            timestamp_us=timestamp_us,
            is_tombstone=True,
        )

        endpoints = self.get_natural_endpoints(partition_key)
        required = self._required_acks(consistency)
        acks = 0

        for node in endpoints:
            if node.write_row(tombstone):
                acks += 1

        if acks < required:
            raise WriteTimeoutError(
                f"Delete consistency {consistency} required {required} acks, received {acks}"
            )
        return True

    def read(
        self,
        partition_key: str,
        clustering_key: str,
        consistency: ConsistencyLevel = "QUORUM",
    ) -> dict[str, Any] | None:
        endpoints = self.get_natural_endpoints(partition_key)
        required = self._required_acks(consistency)

        responses: list[tuple[CassandraStorageNode, CassandraRow | None]] = []
        for node in endpoints:
            if node.is_online:
                row = node.read_row(partition_key, clustering_key)
                responses.append((node, row))
                if len(responses) == required:
                    break

        if len(responses) < required:
            raise ReadTimeoutError(
                f"Read consistency {consistency} required {required} responses, received {len(responses)}"
            )

        valid_rows = [r for _, r in responses if r is not None]
        if not valid_rows:
            return None

        # Last-Write-Wins: Pick row with highest timestamp
        freshest_row = max(valid_rows, key=lambda r: r.timestamp_us)

        # Read Repair: reconcile any node that returned stale or missing data
        for node, row in responses:
            if row is None or row.timestamp_us < freshest_row.timestamp_us:
                node.write_row(freshest_row)

        if freshest_row.is_tombstone:
            return None

        return dict(freshest_row.data)
