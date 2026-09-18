"""Problem 01 — Compute 3D Rank Coordinates

Topic: 08 3D Parallelism Integration and Orchestration
Target: Production-grade implementation

Map global rank to 3D grid coordinates (DP, TP, PP).

Example:
    >>> compute_3d_rank_coordinates(11, 2, 4, 8)
    (1, 1, 1)

Hints:
    Hint 1: This is the same kind of problem as decoding a linear index
        into multi-dimensional array coordinates — the rank was flattened
        with TP as the fastest-varying (innermost) axis and DP as the
        slowest-varying (outermost) axis.
    Hint 2: Peel off the innermost axis first with `tp = global_rank %
        tp_size`, then work with the remaining quotient `global_rank //
        tp_size` the same way for `pp`, and whatever's left after that is
        `dp`.
    Hint 3: The division order matters — divide out `tp_size` before
        `pp_size`, not the other way around, since TP is nested inside PP
        which is nested inside DP; getting the nesting order backwards
        silently produces a different but still in-range coordinate.
"""

from __future__ import annotations


def compute_3d_rank_coordinates(global_rank: int, tp_size: int, pp_size: int, dp_size: int) -> tuple[int, int, int]:
    """Map global rank to (dp_coord, pp_coord, tp_coord).
    Indexing order: TP (inner), PP (middle), DP (outer).
    global_rank = dp * (pp_size * tp_size) + pp * tp_size + tp
    Returns (dp, pp, tp).
    """
    raise NotImplementedError("Implement compute_3d_rank_coordinates")
