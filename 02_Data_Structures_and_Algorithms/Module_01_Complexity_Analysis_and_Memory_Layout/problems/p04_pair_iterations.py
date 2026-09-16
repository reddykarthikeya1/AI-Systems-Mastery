"""Problem 04 — Count Distinct Pair Iterations

Pattern:    Complexity analysis
Difficulty: Easy
Target:     Time O(1), Space O(1)

A nested loop compares every distinct unordered pair exactly once::

    for i in range(n):
        for j in range(i + 1, n):
            compare(a[i], a[j])

Return how many times ``compare`` runs.

Constraints
- ``0 <= n <= 10**9`` — again, you must not simulate

Example
    count_pair_iterations(4) -> 6

Hints — read one at a time, and try again between each.

    Hint 1: Write out the inner-loop counts for n = 4: 3, 2, 1, 0.
    Hint 2: That is the sum of the first n-1 integers.
    Hint 3: Closed form: n*(n-1)//2. Use integer division, not /, so the result stays exact at large n.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p04
"""

from __future__ import annotations


def count_pair_iterations(n: int) -> int:
    raise NotImplementedError("implement count_pair_iterations")
