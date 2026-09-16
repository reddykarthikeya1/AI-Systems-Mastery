"""Problem 08 — Partition Labels

Pattern:    Greedy with last-occurrence bounds
Difficulty: Medium
Target:     Time O(n), Space O(alphabet)

Split ``s`` into as many parts as possible so that each letter appears in at
most one part. Return the sizes of the parts, in order.

Constraints
- ``1 <= len(s) <= 500``
- lowercase letters

Example
    partition_labels("ababcbacadefegdehijhklij") -> [9, 7, 8]

Hints — read one at a time, and try again between each.

    Hint 1: A part cannot end before the last occurrence of every letter it contains.
    Hint 2: So precompute the last index of each letter in one pass.
    Hint 3: Then sweep, extending the current part's end to the maximum last-index of the letters seen. When the cursor reaches that end, close the part.

Run the tests for just this problem::

    cd problems
    python -m pytest tests -q -k p08
"""

from __future__ import annotations


def partition_labels(s: str) -> list[int]:
    raise NotImplementedError("implement partition_labels")
