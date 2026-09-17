"""Reference Solution — Problem 01: Sharded State Dict Merge

Topic: 09 Distributed Checkpointing DCP and Failure Recovery
"""

from __future__ import annotations


def sharded_state_dict_merge(shards: list[tuple[int, list[float]]]) -> list[float]:
    sorted_shards = sorted(shards, key=lambda x: x[0])
    unified = []
    for _, sl in sorted_shards:
        unified.extend(sl)
    return unified
