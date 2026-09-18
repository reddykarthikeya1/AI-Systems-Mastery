"""Problem 01 — Count Min Sketch Heavy Hitters

Topic: 12 Probabilistic Data Structures
Target: Production-grade implementation

Estimate frequencies using Count-Min Sketch and detect heavy hitters above threshold.

Example:
    >>> count_min_sketch_heavy_hitters(['apple'] * 10 + ['banana'] * 2 + ['orange'], width=50, depth=4, threshold=5)
    {'apple'}

Hints:
    Hint 1: A Count-Min Sketch never underestimates a frequency, only ever
        overestimates it (due to hash collisions) -- so the best estimate
        of an item's true count is the MINIMUM across all hashed rows.
    Hint 2: Use a depth x width 2D counter table; on insert, bump
        `table[row][hash(item + row) % width]` for every row, and on
        query take the min across rows and compare it to `threshold`.
    Hint 3: Each of the `depth` rows must hash with a distinguishable
        function, e.g. by folding the row index into the hashed string
        (`f"{item}_{row}"`) -- otherwise every row collapses to the same
        hash and you lose the benefit of independent estimates; wrap the
        hash in `abs(...)` since Python's `hash()` can be negative.
"""

from __future__ import annotations


def count_min_sketch_heavy_hitters(items: list[str], width: int = 100, depth: int = 4, threshold: int = 5) -> set[str]:
    """Insert items into Count-Min Sketch of dimensions (depth x width).
    Use hash(f"{item}_{row}") % width.
    Return items whose minimum estimated count >= threshold.
    """
    raise NotImplementedError("Implement count_min_sketch_heavy_hitters")
