"""Reference Solution — Problem 01: Compute 3D Rank Coordinates

Topic: 08 3D Parallelism Integration and Orchestration
"""

from __future__ import annotations


def compute_3d_rank_coordinates(global_rank: int, tp_size: int, pp_size: int, dp_size: int) -> tuple[int, int, int]:
    tp = global_rank % tp_size
    rem = global_rank // tp_size
    pp = rem % pp_size
    dp = rem // pp_size
    return (dp, pp, tp)
