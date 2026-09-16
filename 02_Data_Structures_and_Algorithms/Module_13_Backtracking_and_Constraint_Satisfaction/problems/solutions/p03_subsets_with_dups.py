"""Reference solution — Problem 03: Subsets With Duplicates

Pattern:    Backtracking with duplicate skipping
Complexity: Time O(n * 2^n), Space O(n) excluding output
"""

from __future__ import annotations


def subsets_with_dups(nums: list[int]) -> list[list[int]]:
    ordered = sorted(nums)
    out: list[list[int]] = []
    path: list[int] = []

    def backtrack(start: int) -> None:
        out.append(path[:])
        for i in range(start, len(ordered)):
            # `i > start` restricts the skip to SIBLING branches at this level.
            # Dropping it would also block a legitimate repeat inside one
            # subset, so [1, 2, 2] would never be produced.
            if i > start and ordered[i] == ordered[i - 1]:
                continue
            path.append(ordered[i])
            backtrack(i + 1)
            path.pop()

    backtrack(0)
    return sorted(out)
