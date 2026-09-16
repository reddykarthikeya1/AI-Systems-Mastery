"""Reference solution — Problem 03: Median From A Data Stream

Pattern:    Two heaps
Complexity: Time O(n log n) total, O(1) per query, Space O(n)
"""

from __future__ import annotations


def streaming_median(nums: list[int]) -> list[float]:
    import heapq

    lower: list[int] = []   # max-heap via negation: the largest of the small half
    upper: list[int] = []   # min-heap: the smallest of the large half
    out: list[float] = []

    for x in nums:
        # Always push to `lower` first, then shuttle its max across, which keeps
        # the ordering invariant without any comparison special-casing.
        heapq.heappush(lower, -x)
        heapq.heappush(upper, -heapq.heappop(lower))
        # Rebalance so len(lower) is len(upper) or one more.
        if len(upper) > len(lower):
            heapq.heappush(lower, -heapq.heappop(upper))

        if len(lower) > len(upper):
            out.append(float(-lower[0]))
        else:
            out.append((-lower[0] + upper[0]) / 2.0)

    return out
