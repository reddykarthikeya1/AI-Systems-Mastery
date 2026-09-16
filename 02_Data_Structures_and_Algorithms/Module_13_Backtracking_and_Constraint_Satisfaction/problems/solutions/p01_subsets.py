"""Reference solution — Problem 01: All Subsets

Pattern:    Backtracking
Complexity: Time O(n * 2^n), Space O(n) excluding output
"""

from __future__ import annotations


def subsets(nums: list[int]) -> list[list[int]]:
    out: list[list[int]] = []
    path: list[int] = []
    ordered = sorted(nums)

    def backtrack(start: int) -> None:
        # A copy: `path` is mutated after this call returns, so storing the
        # live list would make every recorded result identical.
        out.append(path[:])
        for i in range(start, len(ordered)):
            path.append(ordered[i])
            backtrack(i + 1)
            path.pop()              # undo

    backtrack(0)
    return sorted(out)
