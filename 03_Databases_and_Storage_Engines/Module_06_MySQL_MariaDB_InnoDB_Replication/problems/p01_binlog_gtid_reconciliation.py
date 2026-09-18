"""Problem 01 — Binlog Gtid Reconciliation

Topic: 06 MySQL MariaDB InnoDB Replication
Target: Production-grade implementation

Calculate missing GTID intervals for replica to catch up with primary.

Example:
    >>> primary = [(1, 10), (15, 20)]
    >>> replica = [(1, 8), (17, 18)]
    >>> binlog_gtid_reconciliation(primary, replica)
    [(9, 10), (15, 16), (19, 20)]

Hints:
    Hint 1: Think of each interval list as the set of individual GTID
        sequence numbers it covers; the replica is missing exactly the
        numbers the primary has that the replica doesn't.
    Hint 2: Expand both interval lists into sets of integers, take the set
        difference, then re-collapse the sorted leftover numbers back into
        contiguous (start, end) runs.
    Hint 3: A run only continues while the next missing number is exactly
        prev + 1; the moment there's a gap (like 10 -> 15 above, where 11-14
        are present on the replica), close out the current (start, end)
        pair and begin a new one — and a single isolated missing number
        must still come out as (n, n), not be dropped or merged.
"""

from __future__ import annotations


def binlog_gtid_reconciliation(primary_intervals: list[tuple[int, int]], replica_intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Each interval is [start, end] inclusive.
    Both lists are sorted, non-overlapping.
    Returns list of missing intervals primary has that replica does not have.
    """
    raise NotImplementedError("Implement binlog_gtid_reconciliation")
