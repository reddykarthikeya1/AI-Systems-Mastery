"""Problem 06 — Decode Ways

Pattern:    1D DP with a two-character lookback
Difficulty: Medium
Target:     Time O(n), Space O(1)

``'A'`` maps to ``"1"``, …, ``'Z'`` maps to ``"26"``. Return the number of ways
to decode the digit string ``s``.

Constraints
- ``1 <= len(s) <= 100``
- ``s`` contains only digits and may contain leading zeros

Example
    decode_ways("12")   -> 2      ("AB", "L")
    decode_ways("226")  -> 3      ("BZ", "VF", "BBF")
    decode_ways("06")   -> 0

Hints — read one at a time, and try again between each.

    Hint 1: Very similar to climbing stairs, but with validity conditions on each step.
    Hint 2: A one-digit step is valid only when that digit is not '0'. A two-digit step is valid only when the pair is between 10 and 26.
    Hint 3: ways(i) = (ways(i-1) if s[i-1] != '0') + (ways(i-2) if 10 <= int(s[i-2:i]) <= 26). Zeros are where every wrong answer comes from: '06' is 0, and '10' is 1.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p06
"""

from __future__ import annotations


def decode_ways(s: str) -> int:
    raise NotImplementedError("implement decode_ways")
