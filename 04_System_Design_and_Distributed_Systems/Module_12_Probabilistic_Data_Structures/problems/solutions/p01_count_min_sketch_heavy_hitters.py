"""Reference Solution — Problem 01: Count Min Sketch Heavy Hitters

Topic: 12 Probabilistic Data Structures
"""

from __future__ import annotations


def count_min_sketch_heavy_hitters(items: list[str], width: int = 100, depth: int = 4, threshold: int = 5) -> set[str]:
    table = [[0] * width for _ in range(depth)]
    for it in items:
        for r in range(depth):
            idx = abs(hash(f"{it}_{r}")) % width
            table[r][idx] += 1
    
    heavy = set()
    for it in items:
        est = min(table[r][abs(hash(f"{it}_{r}")) % width] for r in range(depth))
        if est >= threshold:
            heavy.add(it)
    return heavy
