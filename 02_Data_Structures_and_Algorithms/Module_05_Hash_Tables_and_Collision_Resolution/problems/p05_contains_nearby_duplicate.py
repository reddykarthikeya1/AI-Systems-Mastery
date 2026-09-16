"""Problem 05 — Duplicate Within Distance K

Pattern:    Sliding window + hash set
Difficulty: Medium
Target:     Time O(n), Space O(min(n, k))

Return True if there are two equal values at indices ``i`` and ``j`` with
``i != j`` and ``abs(i - j) <= k``.

Constraints
- ``1 <= len(nums) <= 10**5``
- ``0 <= k <= 10**5``

Example
    contains_nearby_duplicate([1, 2, 3, 1], 3) -> True
    contains_nearby_duplicate([1, 2, 3, 1], 2) -> False

Hints — read one at a time, and try again between each.

    Hint 1: A plain 'seen' set answers 'is there any duplicate', which is a different question - it ignores the distance.
    Hint 2: Keep only the last k elements in the set: a window.
    Hint 3: Add the current element, and once the set exceeds k entries, remove the one that just fell out of range. k = 0 must return False, since i != j is required.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p05
"""

from __future__ import annotations


def contains_nearby_duplicate(nums: list[int], k: int) -> bool:
    raise NotImplementedError("implement contains_nearby_duplicate")
