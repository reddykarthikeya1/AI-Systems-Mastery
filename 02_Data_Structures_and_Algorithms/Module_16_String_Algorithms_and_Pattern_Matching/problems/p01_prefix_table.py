"""Problem 01 - Build the KMP Prefix Table

Pattern:    KMP prefix function
Difficulty: Medium
Target:     Time O(m), Space O(m)

Return ``pi`` where ``pi[i]`` is the length of the longest proper
prefix of ``pattern[:i+1]`` that is also a suffix of it. A *proper* prefix is
one that is not the whole string.

Constraints
- ``0 <= len(pattern) <= 10**5``
- O(m) is the target; an O(m^2) double loop will time out on the scale test

Example
    build_prefix_table("ababaca") -> [0, 0, 1, 2, 3, 0, 1]

This one table is the whole of KMP. Everything else in this module is built on
it, so get it right before moving on.

Hints - read one at a time, and try again between each.

    Hint 1: Track `k`, the length currently matched. For each new character, if it extends the match, `k += 1`.
    Hint 2: On a mismatch you do not reset to 0 - you fall back to `pi[k-1]`, the next-longest prefix that is still a candidate, and try again.
    Hint 3: That fallback is a `while` loop, not an `if`: you may have to fall back several times before the character matches or `k` reaches 0.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p01
"""

from __future__ import annotations


def build_prefix_table(pattern: str) -> list[int]:
    raise NotImplementedError("implement build_prefix_table")
