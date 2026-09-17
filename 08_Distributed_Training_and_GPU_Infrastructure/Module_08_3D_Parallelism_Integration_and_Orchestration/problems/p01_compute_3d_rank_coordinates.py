"""Problem 01 — Compute 3D Rank Coordinates

Topic: 08 3D Parallelism Integration and Orchestration
Target: Production-grade implementation

Map global rank to 3D grid coordinates (DP, TP, PP).

Hints:
    Hint 1: Review module invariants and mathematical definitions.
    Hint 2: Handle edge cases, dimensions, and numerical stability cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def compute_3d_rank_coordinates(global_rank: int, tp_size: int, pp_size: int, dp_size: int) -> tuple[int, int, int]:
    """Map global rank to (dp_coord, pp_coord, tp_coord).
    Indexing order: TP (inner), PP (middle), DP (outer).
    global_rank = dp * (pp_size * tp_size) + pp * tp_size + tp
    Returns (dp, pp, tp).
    """
    raise NotImplementedError("Implement compute_3d_rank_coordinates")
