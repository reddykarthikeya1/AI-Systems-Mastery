"""Reference solution — Problem 03: Edit Distance

Pattern:    2D sequence DP
Complexity: Time O(n*m), Space O(min(n, m))
"""

from __future__ import annotations


def edit_distance(a: str, b: str) -> int:
    n, m = len(a), len(b)

    # Two rows suffice: each row depends only on the one before it.
    prev = list(range(m + 1))       # turning "" into b[:j] costs j inserts

    for i in range(1, n + 1):
        cur = [i] + [0] * m         # turning a[:i] into "" costs i deletes
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1]            # free: characters already match
            else:
                cur[j] = 1 + min(
                    prev[j],        # delete a[i-1]
                    cur[j - 1],     # insert b[j-1]
                    prev[j - 1],    # substitute
                )
        prev = cur

    return prev[m]
