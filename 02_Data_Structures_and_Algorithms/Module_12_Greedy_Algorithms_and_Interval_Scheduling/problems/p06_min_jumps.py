"""Problem 06 — Jump Game II (Fewest Jumps)

Pattern:    Greedy BFS by levels
Difficulty: Hard
Target:     Time O(n), Space O(1)

Return the minimum number of jumps to reach the last index. The last index is
always reachable.

Constraints
- ``1 <= len(nums) <= 10**4``  -> O(n) expected

Example
    min_jumps([2, 3, 1, 1, 4]) -> 2      (index 0 -> 1 -> 4)

Example:
    >>> min_jumps([2, 3, 1, 1, 4])
    2

Hints — read one at a time, and try again between each.

    Hint 1: A BFS over indices works and is the right intuition, but it can be O(n^2) if you enqueue every index.
    Hint 2: Notice that BFS here processes indices in contiguous RANGES: all indices reachable in 1 jump form a range, then 2 jumps, and so on.
    Hint 3: So sweep once, tracking the end of the current range and the furthest index reachable from anywhere within it. When you reach the current range's end, that is one jump.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p06
"""

from __future__ import annotations


def min_jumps(nums: list[int]) -> int:
    raise NotImplementedError("implement min_jumps")
