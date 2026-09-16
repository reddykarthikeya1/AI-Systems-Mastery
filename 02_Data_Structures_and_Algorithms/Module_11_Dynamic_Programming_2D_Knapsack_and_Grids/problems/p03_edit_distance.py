"""Problem 03 — Edit Distance

Pattern:    2D sequence DP
Difficulty: Hard
Target:     Time O(n*m), Space O(min(n, m))

Return the minimum number of single-character insertions, deletions or
substitutions needed to turn ``a`` into ``b``.

Constraints
- ``0 <= len(a), len(b) <= 500``

Example
    edit_distance("horse", "ros")     -> 3
    edit_distance("intention", "execution") -> 5

Hints — read one at a time, and try again between each.

    Hint 1: State: dist[i][j] is the cost of turning the first i characters of a into the first j characters of b.
    Hint 2: Base cases: turning a prefix into the empty string costs one deletion per character, so dist[i][0] = i and dist[0][j] = j.
    Hint 3: If the characters match, no operation is needed and the cost carries over diagonally. Otherwise it is 1 + min(delete, insert, substitute), which are the three neighbours above, left, and diagonal.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p03
"""

from __future__ import annotations


def edit_distance(a: str, b: str) -> int:
    raise NotImplementedError("implement edit_distance")
