"""Problem 01 — Binlog Gtid Reconciliation

Topic: 06 MySQL MariaDB InnoDB Replication
Target: Production-grade implementation

Calculate missing GTID intervals for replica to catch up with primary.

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle boundary conditions and empty inputs cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def binlog_gtid_reconciliation(primary_intervals: list[tuple[int, int]], replica_intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Each interval is [start, end] inclusive.
    Both lists are sorted, non-overlapping.
    Returns list of missing intervals primary has that replica does not have.
    """
    raise NotImplementedError("Implement binlog_gtid_reconciliation")
