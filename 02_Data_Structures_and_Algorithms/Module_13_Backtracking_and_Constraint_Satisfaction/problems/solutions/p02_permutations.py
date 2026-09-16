"""Reference solution — Problem 02: All Permutations

Pattern:    Backtracking with a used set
Complexity: Time O(n * n!), Space O(n) excluding output
"""

from __future__ import annotations


def permutations(nums: list[int]) -> list[list[int]]:
    ordered = sorted(nums)
    n = len(ordered)
    used = [False] * n
    out: list[list[int]] = []
    path: list[int] = []

    def backtrack() -> None:
        if len(path) == n:
            out.append(path[:])
            return
        for i in range(n):
            if used[i]:
                continue
            used[i] = True
            path.append(ordered[i])
            backtrack()
            path.pop()              # undo both pieces of state
            used[i] = False

    backtrack()
    return sorted(out)
