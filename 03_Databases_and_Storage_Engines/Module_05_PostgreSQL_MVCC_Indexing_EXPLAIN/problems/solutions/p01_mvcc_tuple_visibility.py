"""Reference Solution — Problem 01: Mvcc Tuple Visibility

Topic: 05 PostgreSQL MVCC Indexing EXPLAIN
"""

from __future__ import annotations


def mvcc_tuple_visibility(xmin: int, xmax: int | None, snapshot_xmin: int, snapshot_xmax: int, active_xids: set[int]) -> bool:
    # Check creation
    if xmin >= snapshot_xmax or xmin in active_xids:
        return False
    # Check deletion
    if xmax is not None:
        if xmax < snapshot_xmin or (xmax not in active_xids and xmax < snapshot_xmax):
            return False
    return True
