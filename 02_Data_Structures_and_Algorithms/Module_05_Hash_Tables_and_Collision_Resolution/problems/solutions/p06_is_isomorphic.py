"""Reference solution — Problem 06: Isomorphic Strings

Pattern:    Two-way hash mapping
Complexity: Time O(n), Space O(alphabet)
"""

from __future__ import annotations


def is_isomorphic(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False

    forward: dict[str, str] = {}
    backward: dict[str, str] = {}

    for a, b in zip(s, t):
        # A single map accepts "badc" -> "baba"; the reverse map is what
        # rejects two characters collapsing onto one.
        if a in forward and forward[a] != b:
            return False
        if b in backward and backward[b] != a:
            return False
        forward[a] = b
        backward[b] = a

    return True
