"""Problem 01 — Lsm Leveled Compaction

Topic: 15 LSM Trees Compaction DynamoDB
Target: Production-grade implementation

Merge sorted SSTable runs resolving tombstone deletions.

Example:
    >>> run1 = [("k1", "v1_old", 10), ("k2", "v2", 15)]
    >>> run2 = [("k1", "v1_new", 20), ("k2", None, 25)]  # k2 tombstone
    >>> lsm_leveled_compaction([run1, run2])
    [('k1', 'v1_new')]

Hints:
    Hint 1: Timestamp, not run order or list position, is the only thing
        that decides which version of a key survives compaction — a newer
        write in an earlier run still beats an older write in a later one.
    Hint 2: Use a dict keyed by key that tracks the (value, timestamp) with
        the highest timestamp seen so far across every run; only after
        scanning all runs do you know each key's true final state.
    Hint 3: A tombstone (value is None) can still "win" a key during the
        merge if it has the highest timestamp — as with k2 above, whose
        None at ts=25 beats "v2" at ts=15 — but it must then be filtered out
        of the final output entirely, not emitted as (k2, None).
"""

from __future__ import annotations


def lsm_leveled_compaction(sstable_runs: list[list[tuple[str, str | None, int]]]) -> list[tuple[str, str]]:
    """Each entry is (key, value, timestamp).
    If value is None, it is a tombstone deletion.
    Merge all sorted runs. For duplicate keys, keep entry with greatest timestamp.
    Filter out tombstones from final compacted output.
    Returns list of (key, value) sorted by key.
    """
    raise NotImplementedError("Implement lsm_leveled_compaction")
