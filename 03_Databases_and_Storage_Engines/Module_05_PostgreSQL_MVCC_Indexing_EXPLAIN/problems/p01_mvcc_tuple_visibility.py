"""Problem 01 — Mvcc Tuple Visibility

Topic: 05 PostgreSQL MVCC Indexing EXPLAIN
Target: Production-grade implementation

Determine tuple visibility according to MVCC snapshot rules.

Example:
    >>> active = {102, 104}
    >>> mvcc_tuple_visibility(90, None, 100, 105, active)
    True
    >>> mvcc_tuple_visibility(102, None, 100, 105, active)
    False

Hints:
    Hint 1: Visibility is a two-sided question: the tuple's creator (xmin)
        must be "already committed as far as this snapshot is concerned",
        and its deleter (xmax), if any, must NOT be already committed.
    Hint 2: No data structure is needed beyond the given active_xids set —
        just two membership/comparison checks, one against snapshot_xmin
        and snapshot_xmax, and one against active_xids.
    Hint 3: A xid counts as "committed before this snapshot" only when it is
        strictly less than snapshot_xmax AND not itself in active_xids
        (an xid can be numerically below snapshot_xmax yet still be an
        in-flight transaction); xmax=None means never deleted, so the
        deletion check is skipped entirely in that case.
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
