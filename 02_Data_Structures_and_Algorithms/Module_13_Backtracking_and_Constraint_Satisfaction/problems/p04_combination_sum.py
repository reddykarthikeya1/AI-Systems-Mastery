"""Problem 04 — Combination Sum

Pattern:    Backtracking with reuse
Difficulty: Medium
Target:     Time O(n^(target/min)) worst case, Space O(target/min)

Return all unique combinations of ``candidates`` summing to ``target``. Each
candidate may be used **any number of times**. Return sorted combinations,
sorted.

Constraints
- ``1 <= len(candidates) <= 30``, all distinct and positive
- ``1 <= target <= 40``

Example
    combination_sum([2, 3, 6, 7], 7) -> [[2, 2, 3], [7]]

Example:
    >>> combination_sum([2, 3, 6, 7], 7)
    [[2, 2, 3], [7]]

Hints — read one at a time, and try again between each.

    Hint 1: Reuse is allowed, so after choosing candidate i you may choose i again - recurse with the same start index, not start + 1.
    Hint 2: But do not go BACKWARDS, or [2,3] and [3,2] both appear.
    Hint 3: Prune: sort the candidates and break out of the loop once a candidate exceeds the remaining target. Everything after it is larger.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p04
"""

from __future__ import annotations


def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    raise NotImplementedError("implement combination_sum")
