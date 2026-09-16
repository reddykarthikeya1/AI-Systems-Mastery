#!/usr/bin/env python3
"""Module 13: In-Process Architectural Simulation Model: Partitioned Commit-Log Streaming Broker.

Mimics core Apache Kafka / Apache Pulsar streaming primitives:
- Distributed append-only commit logs
- Key-based deterministic partition routing
- Consumer groups with partition ownership balancing
- Offset tracking, commits, and log replay
"""

from __future__ import annotations

import hashlib
import threading
import time
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class StreamRecord:
    offset: int
    partition_id: int
    key: str
    value: Any
    timestamp: float


class Partition:
    """An immutable, append-only sequential commit log partition."""

    def __init__(self, partition_id: int) -> None:
        self.partition_id = partition_id
        self._log: list[StreamRecord] = []
        self._lock = threading.Lock()

    def append(self, key: str, value: Any) -> StreamRecord:
        with self._lock:
            offset = len(self._log)
            record = StreamRecord(
                offset=offset,
                partition_id=self.partition_id,
                key=key,
                value=value,
                timestamp=time.time(),
            )
            self._log.append(record)
            return record

    def read_from(self, start_offset: int, max_records: int = 10) -> list[StreamRecord]:
        with self._lock:
            if start_offset >= len(self._log):
                return []
            return list(self._log[start_offset : start_offset + max_records])

    @property
    def high_watermark(self) -> int:
        with self._lock:
            return len(self._log)


class Topic:
    """A logical stream composed of P independent physical partitions."""

    def __init__(self, name: str, num_partitions: int = 3) -> None:
        self.name = name
        self.num_partitions = num_partitions
        self.partitions = [Partition(pid) for pid in range(num_partitions)]

    def _get_partition_id(self, key: str) -> int:
        """Deterministic partition assignment using Murmur-style MD5 hash modulo."""
        digest = int(hashlib.md5(key.encode("utf-8")).hexdigest(), 16)
        return digest % self.num_partitions

    def publish(self, key: str, value: Any) -> StreamRecord:
        pid = self._get_partition_id(key)
        return self.partitions[pid].append(key, value)


class ConsumerGroup:
    """Manages a pool of consumers, partitioning assignments, and committed offsets."""

    def __init__(self, group_id: str, topic: Topic) -> None:
        self.group_id = group_id
        self.topic = topic
        self.members: set[str] = set()
        # partition_assignments: member_id -> list of partition_ids
        self.assignments: dict[str, list[int]] = {}
        # committed_offsets: partition_id -> next offset to read
        self.committed_offsets: dict[int, int] = dict.fromkeys(range(topic.num_partitions), 0)
        self._lock = threading.RLock()

    def register_member(self, member_id: str) -> None:
        with self._lock:
            self.members.add(member_id)
            self._rebalance()

    def leave_member(self, member_id: str) -> None:
        with self._lock:
            self.members.discard(member_id)
            self.assignments.pop(member_id, None)
            self._rebalance()

    def _rebalance(self) -> None:
        """Evenly distributes partitions across registered members in round-robin fashion."""
        self.assignments = {m: [] for m in self.members}
        if not self.members:
            return

        sorted_members = sorted(self.members)
        for pid in range(self.topic.num_partitions):
            member = sorted_members[pid % len(sorted_members)]
            self.assignments[member].append(pid)

    def fetch(self, member_id: str, max_records_per_partition: int = 5) -> list[StreamRecord]:
        """Fetches uncommitted records from all partitions assigned to this member."""
        with self._lock:
            assigned_pids = self.assignments.get(member_id, [])
            records: list[StreamRecord] = []

            for pid in assigned_pids:
                curr_offset = self.committed_offsets[pid]
                batch = self.topic.partitions[pid].read_from(curr_offset, max_records=max_records_per_partition)
                records.extend(batch)

            return records

    def commit(self, records: list[StreamRecord]) -> None:
        """Advances committed offsets for the processed records."""
        with self._lock:
            for r in records:
                # Advance offset to record.offset + 1 (the next record to read)
                current = self.committed_offsets[r.partition_id]
                self.committed_offsets[r.partition_id] = max(current, r.offset + 1)

    def seek(self, partition_id: int, offset: int) -> None:
        """Replay functionality: rewinds consumer group offset back to an earlier position."""
        with self._lock:
            if not (0 <= partition_id < self.topic.num_partitions):
                raise ValueError(f"Invalid partition {partition_id}")
            self.committed_offsets[partition_id] = offset
