"""Problem 04 — 0/1 Knapsack

Pattern:    0/1 knapsack DP
Difficulty: Hard
Target:     Time O(n*capacity), Space O(capacity)

Each item may be taken **at most once**. Return the maximum total value that
fits within ``capacity``.

Constraints
- ``0 <= len(weights) == len(values) <= 100``
- ``0 <= capacity <= 10**4``
- weights and values are non-negative

Example
    knapsack_01([1, 3, 4, 5], [1, 4, 5, 7], 7) -> 9    (items of weight 3 and 4)

**The trap.** The one-row space optimisation must iterate capacity from high to
low. Iterating low to high lets the same item be picked up again within the same
pass, which silently computes *unbounded* knapsack — a larger, plausible, wrong
answer. The tests below include a case where the two differ.

Hints — read one at a time, and try again between each.

    Hint 1: The 2D form is clear: best[i][c] = max(skip item i, take item i). Write that first and get it right.
    Hint 2: Then notice row i depends only on row i-1, so a single row of length capacity+1 suffices.
    Hint 3: In the one-row version, iterate c DOWNWARD. Going upward means best[c - w] has already been updated with item i this pass, so item i gets taken twice.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p04
"""

from __future__ import annotations


def knapsack_01(weights: list[int], values: list[int], capacity: int) -> int:
    raise NotImplementedError("implement knapsack_01")
