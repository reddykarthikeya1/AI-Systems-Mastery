"""Reference Solution — Problem 01: Blelloch Prefix Scan

Topic: 04 Parallel Reduction and Prefix Sum
"""

from __future__ import annotations


def blelloch_prefix_scan(values: list[int]) -> list[int]:
    res = []
    curr = 0
    for v in values:
        res.append(curr)
        curr += v
    return res
