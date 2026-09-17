"""Reference Solution — Problem 01: Binlog Gtid Reconciliation

Topic: 06 MySQL MariaDB InnoDB Replication
"""

from __future__ import annotations


def binlog_gtid_reconciliation(primary_intervals: list[tuple[int, int]], replica_intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    p_set = set()
    for s, e in primary_intervals:
        p_set.update(range(s, e + 1))
    r_set = set()
    for s, e in replica_intervals:
        r_set.update(range(s, e + 1))
    missing = sorted(p_set - r_set)
    if not missing:
        return []
    res = []
    start = missing[0]
    prev = missing[0]
    for x in missing[1:]:
        if x == prev + 1:
            prev = x
        else:
            res.append((start, prev))
            start = x
            prev = x
    res.append((start, prev))
    return res
