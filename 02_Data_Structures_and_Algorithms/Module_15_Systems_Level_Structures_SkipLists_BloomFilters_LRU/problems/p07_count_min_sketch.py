"""Problem 07 — Count-Min Sketch: Frequency Estimation

Pattern:    Count-Min sketch
Difficulty: Hard
Target:     Time O((n + q) * depth), Space O(width * depth)

Estimate each query's frequency in ``items`` using a ``depth x width`` table of
counters, with no per-key storage.

The contract: the estimate is **never an underestimate**. It may overestimate
when hashes collide.

Constraints
- ``0 <= len(items) <= 10**6``
- must be deterministic

Example
    count_min_estimate(["a","a","b"], ["a","b","c"]) -> [2, 1, 0 or more]

Example:
    >>> count_min_estimate(["a", "a", "b"], ["a", "b", "c"])
    [2, 1, 0]

Hints — read one at a time, and try again between each.

    Hint 1: Use `depth` independent hash functions. Each item increments one counter per row.
    Hint 2: To estimate, take the MINIMUM across the rows. Collisions can only push a counter up, so the smallest row is the closest to the truth - and it can never be below the true count.
    Hint 3: That is why it is called count-MIN, and why the guarantee is one-sided. Use hashlib for reproducibility.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p07
"""

from __future__ import annotations


def count_min_estimate(items: list[str], queries: list[str], width: int = 2048, depth: int = 4) -> list[int]:
    raise NotImplementedError("implement count_min_estimate")
