"""Problem 05 — Sliding Window Maximum

Pattern:    Monotonic deque
Difficulty: Hard
Target:     Time O(n), Space O(k)

Return the maximum of every contiguous window of size ``k``.

Raise ``ValueError`` for an invalid window size.

Constraints
- ``1 <= len(nums) <= 10**5``  -> O(n) required; O(n log k) with a heap is not the target
- ``1 <= k <= len(nums)``

Example
    sliding_window_max([1, 3, -1, -3, 5, 3, 6, 7], 3) -> [3, 3, 5, 5, 6, 7]

Hints — read one at a time, and try again between each.

    Hint 1: A max-heap gives O(n log k) but cannot cheaply evict the element that just left the window. You need something that can drop from both ends.
    Hint 2: Keep a deque of indices whose values are decreasing. The front is always the window's maximum.
    Hint 3: Two evictions per step: pop from the back while the incoming value dominates (newer AND at least as large, so the older one can never be the max again), and pop from the front when its index has left the window.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p05
"""

from __future__ import annotations


def sliding_window_max(nums: list[int], k: int) -> list[int]:
    raise NotImplementedError("implement sliding_window_max")
