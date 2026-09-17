"""Problem 01 — Lsm Leveled Compaction

Topic: 15 LSM Trees Compaction DynamoDB
Target: Production-grade implementation

Merge sorted SSTable runs resolving tombstone deletions.

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle boundary conditions and empty inputs cleanly.
    Hint 3: Run pytest tests/ to verify.
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
