"""Reference Solution — Problem 01: Bplus Tree Node Split

Topic: 21 Storage Engine Internals BPlus Trees
"""

from __future__ import annotations


def bplus_tree_node_split(leaf_keys: list[int], new_key: int, max_capacity: int = 4) -> tuple[list[int], int | None, list[int] | None]:
    keys = sorted(leaf_keys + [new_key])
    if len(keys) <= max_capacity:
        return (keys, None, None)
    mid = len(keys) // 2
    left = keys[:mid]
    right = keys[mid:]
    return (left, right[0], right)
