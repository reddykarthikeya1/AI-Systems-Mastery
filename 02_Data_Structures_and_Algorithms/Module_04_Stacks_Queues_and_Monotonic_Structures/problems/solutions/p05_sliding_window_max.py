"""Reference solution — Problem 05: Sliding Window Maximum

Pattern:    Monotonic deque
Complexity: Time O(n), Space O(k)
"""

from __future__ import annotations


def sliding_window_max(nums: list[int], k: int) -> list[int]:
    from collections import deque

    n = len(nums)
    if k <= 0 or k > n:
        raise ValueError(f"window size {k} is invalid for an array of length {n}")

    dq: deque[int] = deque()    # indices, values decreasing front -> back
    out: list[int] = []

    for i, x in enumerate(nums):
        # Anything smaller than x and older than x can never be a maximum again.
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)

        # Drop the front once it falls outside the window.
        if dq[0] <= i - k:
            dq.popleft()

        if i >= k - 1:
            out.append(nums[dq[0]])

    return out
