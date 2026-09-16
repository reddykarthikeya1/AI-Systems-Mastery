"""Reference solution — Problem 02: Top K Frequent Elements

Pattern:    Counting + bucket sort
Complexity: Time O(n), Space O(n)
"""

from __future__ import annotations


def top_k_frequent(nums: list[int], k: int) -> list[int]:
    counts: dict[int, int] = {}
    for x in nums:
        counts[x] = counts.get(x, 0) + 1

    if k > len(counts):
        raise ValueError(f"k={k} exceeds the {len(counts)} distinct elements present")

    # No frequency can exceed len(nums), so bucket by frequency for O(n).
    buckets: list[list[int]] = [[] for _ in range(len(nums) + 1)]
    for value, freq in counts.items():
        buckets[freq].append(value)

    out: list[int] = []
    for freq in range(len(nums), 0, -1):
        # Ascending value breaks frequency ties deterministically.
        for value in sorted(buckets[freq]):
            out.append(value)
            if len(out) == k:
                return out
    return out
