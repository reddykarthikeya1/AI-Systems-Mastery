"""Reference solution — Problem 04: Combination Sum

Pattern:    Backtracking with reuse
Complexity: Time O(n^(target/min)) worst case, Space O(target/min)
"""

from __future__ import annotations


def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    ordered = sorted(candidates)
    out: list[list[int]] = []
    path: list[int] = []

    def backtrack(start: int, remaining: int) -> None:
        if remaining == 0:
            out.append(path[:])
            return
        for i in range(start, len(ordered)):
            # Sorted, so once one candidate is too big, so is every later one.
            if ordered[i] > remaining:
                break
            path.append(ordered[i])
            # `i`, not `i + 1`: the same candidate may be reused. Never going
            # backwards is what keeps combinations unique.
            backtrack(i, remaining - ordered[i])
            path.pop()

    backtrack(0, target)
    return sorted(out)
