"""Reference solution — Problem 05: Duplicate Within Distance K

Pattern:    Sliding window + hash set
Complexity: Time O(n), Space O(min(n, k))
"""

from __future__ import annotations


def contains_nearby_duplicate(nums: list[int], k: int) -> bool:
    if k <= 0:
        return False        # i != j is required, so distance 0 is impossible

    window: set[int] = set()
    for i, x in enumerate(nums):
        if x in window:
            return True
        window.add(x)
        # Keep the window to exactly the previous k elements.
        if len(window) > k:
            window.remove(nums[i - k])
    return False
