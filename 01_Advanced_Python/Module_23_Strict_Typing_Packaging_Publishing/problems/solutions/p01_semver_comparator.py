"""Problem 01 — SemVer 2.0.0 Tri-Part Comparison

Target: Production-grade implementation
"""

from __future__ import annotations


def compare_semver(v1: str, v2: str) -> int:
    def parse(s):
        parts = s.split('-')[0].split('.')
        return [int(p) for p in parts]
    p1, p2 = parse(v1), parse(v2)
    if p1 < p2: return -1
    if p1 > p2: return 1
    return 0
