"""Problem 02 — All Permutations

Pattern:    Backtracking with a used set
Difficulty: Medium
Target:     Time O(n * n!), Space O(n) excluding output

Return every permutation of ``nums``. The input has no duplicates. Return them
sorted for determinism.

Constraints
- ``1 <= len(nums) <= 8`` — the output has n! entries

Example
    permutations([1, 2, 3])
    -> [[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]]

Hints — read one at a time, and try again between each.

    Hint 1: Unlike subsets, order matters and every element must be used exactly once.
    Hint 2: So at each position you may choose any element not already used.
    Hint 3: Track which indices are used. Mark before recursing and unmark after - the unmark is the part people forget.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p02
"""

from __future__ import annotations


def permutations(nums: list[int]) -> list[list[int]]:
    raise NotImplementedError("implement permutations")
