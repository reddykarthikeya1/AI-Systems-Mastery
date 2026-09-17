"""Problem 01 — Megatron Column Row Parallel

Topic: 05 Tensor Parallelism Megatron LM
Target: Production-grade implementation

Split MLP weights across TP ranks and verify AllReduce reduction.

Hints:
    Hint 1: Review module invariants and mathematical definitions.
    Hint 2: Handle edge cases, dimensions, and numerical stability cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def megatron_column_row_parallel(hidden_dim: int, ffn_dim: int, tp_world_size: int) -> dict[str, int]:
    """Column-parallel splits W1 (hidden x ffn) column-wise: ffn_per_rank = ffn_dim / tp_world_size.
    Row-parallel splits W2 (ffn x hidden) row-wise: ffn_per_rank = ffn_dim / tp_world_size.
    Returns dict with 'w1_cols_per_rank', 'w2_rows_per_rank', 'allreduce_calls_per_mlp'.
    """
    raise NotImplementedError("Implement megatron_column_row_parallel")
