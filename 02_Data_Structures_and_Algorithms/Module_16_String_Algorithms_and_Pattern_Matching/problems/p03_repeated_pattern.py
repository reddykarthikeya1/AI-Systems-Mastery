"""Problem 03 - Is the String a Repeated Block?

Pattern:    String period
Difficulty: Medium
Target:     Time O(n), Space O(n)

Return True if ``s`` can be built by concatenating some proper
substring of itself two or more times.

Constraints
- ``1 <= len(s) <= 10**5``

Example
    is_repeated_pattern("abab")     -> True   ("ab" twice)
    is_repeated_pattern("aba")      -> False
    is_repeated_pattern("abcabcabc")-> True   ("abc" three times)
    is_repeated_pattern("a")        -> False  (needs at least two copies)

The O(n^2) approach tries every divisor length. There is an O(n) answer that
falls straight out of the prefix table.

Hints - read one at a time, and try again between each.

    Hint 1: Let `k = pi[-1]`. Then `n - k` is the smallest period of the string.
    Hint 2: The string tiles exactly when that period divides `n`.
    Hint 3: And you need at least two copies, so the period must be strictly smaller than `n`.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p03
"""

from __future__ import annotations


def is_repeated_pattern(s: str) -> bool:
    raise NotImplementedError("implement is_repeated_pattern")
