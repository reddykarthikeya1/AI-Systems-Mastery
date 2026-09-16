"""Reference solution — Problem 06: Jump Game II (Fewest Jumps)

Pattern:    Greedy BFS by levels
Complexity: Time O(n), Space O(1)
"""

from __future__ import annotations


def min_jumps(nums: list[int]) -> int:
    n = len(nums)
    if n <= 1:
        return 0

    jumps = 0
    current_end = 0     # last index reachable with `jumps` jumps
    furthest = 0        # furthest reachable from anywhere in the current range

    # Stop before the last index: arriving there needs no further jump.
    for i in range(n - 1):
        furthest = max(furthest, i + nums[i])
        if i == current_end:
            # Exhausted this BFS level, so spend a jump to open the next.
            jumps += 1
            current_end = furthest
            if current_end >= n - 1:
                break
    return jumps
