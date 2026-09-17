"""Problem 01 — Mvcc Tuple Visibility

Topic: 05 PostgreSQL MVCC Indexing EXPLAIN
Target: Production-grade implementation

Determine tuple visibility according to MVCC snapshot rules.

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle boundary conditions and empty inputs cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def mvcc_tuple_visibility(xmin: int, xmax: int | None, snapshot_xmin: int, snapshot_xmax: int, active_xids: set[int]) -> bool:
    """Return True if tuple is visible to snapshot, False otherwise.
    Rules:
    - If xmin in active_xids or xmin >= snapshot_xmax: invisible (created in future/active)
    - If xmin < snapshot_xmin or (xmin not in active_xids and xmin < snapshot_xmax): created and committed
    - If xmax is set and (xmax < snapshot_xmin or (xmax not in active_xids and xmax < snapshot_xmax)): deleted by committed tx -> invisible
    """
    raise NotImplementedError("Implement mvcc_tuple_visibility")
