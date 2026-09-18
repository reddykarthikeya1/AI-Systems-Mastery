"""Problem 01 — Bplus Tree Node Split

Topic: 21 Storage Engine Internals BPlus Trees
Target: Production-grade implementation

Insert key into B+ tree leaf node and split when exceeding capacity.

Example:
    >>> bplus_tree_node_split([10, 20, 30, 40], 25, max_capacity=4)
    ([10, 20], 25, [25, 30, 40])

Hints:
    Hint 1: The insert step itself is trivial (sorted position); the actual
        problem is deciding, after inserting, whether the leaf is now
        overfull and needs to hand a key up to its parent.
    Hint 2: Build the new sorted key list once (sorted(leaf_keys + [new_key])
        works fine at this scale), then slice it at the midpoint into a left
        half and a right half only if its length now exceeds max_capacity.
    Hint 3: Unlike an internal-node split, a B+ tree LEAF split keeps the
        promoted key inside the right leaf as real data (right = keys[mid:],
        not keys[mid+1:]) — as shown above, 25 is both the promoted separator
        AND the first element of the right list — because leaves must hold
        every key for range scans, while only internal nodes drop the
        promoted key.
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
