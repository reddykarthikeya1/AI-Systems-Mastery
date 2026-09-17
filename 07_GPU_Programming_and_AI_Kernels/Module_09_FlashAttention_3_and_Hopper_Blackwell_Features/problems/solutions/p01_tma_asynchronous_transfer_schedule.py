"""Reference Solution — Problem 01: Tma Asynchronous Transfer Schedule

Topic: 09 FlashAttention 3 and Hopper Blackwell Features
"""

from __future__ import annotations


def tma_asynchronous_transfer_schedule(total_tiles: int) -> list[tuple[str, int, int]]:
    if total_tiles <= 0:
        return []
    sched = [('LOAD', 0, 0)]
    for i in range(1, total_tiles):
        sched.append(('LOAD', i, i % 2))
        sched.append(('COMPUTE', i - 1, (i - 1) % 2))
    sched.append(('COMPUTE', total_tiles - 1, (total_tiles - 1) % 2))
    return sched
