"""Problem 05 — Does This Complexity Fit The Constraint?

Pattern:    Complexity analysis
Difficulty: Medium
Target:     Time O(1) amortised, Space O(1)

Given an input size ``n`` and a complexity class, decide whether the estimated
operation count stays within ``budget`` (default 10**8, a reasonable one-second
allowance).

Support exactly these classes:
``"O(1)"``, ``"O(log n)"``, ``"O(n)"``, ``"O(n log n)"``, ``"O(n^2)"``,
``"O(n^3)"``, ``"O(2^n)"``, ``"O(n!)"``.

Raise ``ValueError`` for anything else — silently returning False for a typo
would make this function worse than useless.

Constraints
- ``1 <= n <= 10**9``

Example
    fits_budget(100_000, "O(n log n)")  -> True
    fits_budget(100_000, "O(n^2)")      -> False

This is Step 1 of the triage, executable.

Hints — read one at a time, and try again between each.

    Hint 1: Map each class name to a function of n, then compare against the budget.
    Hint 2: For O(2^n) and O(n!) the value explodes; guard with a small-n cutoff before computing, or you will hang building a huge integer.
    Hint 3: math.log2 is fine for the log terms. Use n.bit_length() if you prefer to stay in integers.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p05
"""

from __future__ import annotations


def fits_budget(n: int, complexity: str, budget: int = 10**8) -> bool:
    raise NotImplementedError("implement fits_budget")
