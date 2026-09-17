"""Reference Solution — Problem 01: Skip List Probabilistic Index

Topic: 21 Vector Database HNSW Index Milvus
"""

from __future__ import annotations


def skip_list_probabilistic_index(layers: list[dict[int, int]], target: int) -> int | None:
    if not layers:
        return None
    curr = min(layers[-1].keys()) if layers[-1] else None
    if curr is None:
        return None
    for layer in layers:
        while curr in layer and layer[curr] <= target:
            curr = layer[curr]
            if curr == target:
                return target
    return curr if curr == target else None
