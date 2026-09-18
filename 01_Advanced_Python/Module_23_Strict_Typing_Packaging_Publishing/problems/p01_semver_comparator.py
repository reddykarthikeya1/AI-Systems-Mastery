"""Problem 01 — SemVer 2.0.0 Tri-Part Comparison

Target: Production-grade implementation

Example:
    >>> compare_semver('1.2.3', '1.2.4')
    -1
    >>> compare_semver('2.0.0', '1.9.9')
    1
    >>> compare_semver('1.0.0', '1.0.0')
    0

Hints:
    Hint 1: A version string isn't one number to compare lexicographically —
        '1.9.9' must sort below '2.0.0' even though '9' > '2' as characters,
        so each dot-separated part needs to be compared numerically.
    Hint 2: Strip off any pre-release suffix after a `-`, split the remaining
        `major.minor.patch` on `.`, convert each part to an `int`, and
        compare the two resulting integer lists directly with `<`/`>`.
    Hint 3: Return exactly `-1`, `1`, or `0` (not a bool or a raw
        difference) — Python's list comparison already does the right
        tri-part comparison lexicographically once the parts are integers,
        so '1.9.9' vs '1.10.0' compares correctly instead of by string order.
"""

from __future__ import annotations


def compare_semver(v1: str, v2: str) -> int:
    raise NotImplementedError('Implement compare_semver')
