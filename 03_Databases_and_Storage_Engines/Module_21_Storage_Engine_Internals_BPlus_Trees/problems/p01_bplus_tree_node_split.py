"""Problem 01 — Bplus Tree Node Split

Topic: 21 Storage Engine Internals BPlus Trees
Target: Production-grade implementation

Insert key into B+ tree leaf node and split when exceeding capacity.

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle boundary conditions and empty inputs cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def bplus_tree_node_split(leaf_keys: list[int], new_key: int, max_capacity: int = 4) -> tuple[list[int], int | None, list[int] | None]:
    """Insert new_key in sorted order into leaf_keys.
    If len(leaf_keys) <= max_capacity: return (leaf_keys, None, None).
    If len(leaf_keys) > max_capacity:
    - split at midpoint = len // 2
    - left = leaf_keys[:midpoint]
    - right = leaf_keys[midpoint:]
    - promoted_key = right[0]
    Returns (left, promoted_key, right).
    """
    raise NotImplementedError("Implement bplus_tree_node_split")
