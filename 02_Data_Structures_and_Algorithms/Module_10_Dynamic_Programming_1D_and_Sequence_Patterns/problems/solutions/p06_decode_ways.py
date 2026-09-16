"""Reference solution — Problem 06: Decode Ways

Pattern:    1D DP with a two-character lookback
Complexity: Time O(n), Space O(1)
"""

from __future__ import annotations


def decode_ways(s: str) -> int:
    n = len(s)
    if n == 0:
        return 0

    # ways[i] = number of decodings of the first i characters.
    prev2, prev1 = 1, (0 if s[0] == "0" else 1)

    for i in range(2, n + 1):
        cur = 0
        # A single digit decodes only if it is not '0'.
        if s[i - 1] != "0":
            cur += prev1
        # A pair decodes only in 10..26 - which excludes any pair starting '0'.
        pair = int(s[i - 2 : i])
        if 10 <= pair <= 26:
            cur += prev2
        prev2, prev1 = prev1, cur

    return prev1
