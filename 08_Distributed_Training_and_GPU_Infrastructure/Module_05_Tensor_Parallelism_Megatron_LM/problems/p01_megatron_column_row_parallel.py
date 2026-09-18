"""Problem 01 — Megatron Column Row Parallel

Topic: 05 Tensor Parallelism Megatron LM
Target: Production-grade implementation

Split MLP weights across TP ranks and verify AllReduce reduction.

Example:
    >>> megatron_column_row_parallel(4096, 16384, 8)
    {'w1_cols_per_rank': 2048, 'w2_rows_per_rank': 2048, 'allreduce_calls_per_mlp': 1}

Hints:
    Hint 1: Megatron's whole trick is that the column-parallel W1 and
        row-parallel W2 are split along the *same* dimension (the FFN
        hidden dimension), which is exactly what lets their outputs
        recombine with only one synchronization point per MLP block.
    Hint 2: Both `w1_cols_per_rank` and `w2_rows_per_rank` are just
        `ffn_dim // tp_world_size`; the number of AllReduce calls per MLP
        is a fixed constant (one, applied after the row-parallel linear),
        not something derived from the dimensions.
    Hint 3: `hidden_dim` is part of the signature for realism but never
        enters these particular formulas — don't try to work it into the
        per-rank split sizes, since both splits happen along `ffn_dim`.
"""

from __future__ import annotations


def megatron_column_row_parallel(hidden_dim: int, ffn_dim: int, tp_world_size: int) -> dict[str, int]:
    """Column-parallel splits W1 (hidden x ffn) column-wise: ffn_per_rank = ffn_dim / tp_world_size.
    Row-parallel splits W2 (ffn x hidden) row-wise: ffn_per_rank = ffn_dim / tp_world_size.
    Returns dict with 'w1_cols_per_rank', 'w2_rows_per_rank', 'allreduce_calls_per_mlp'.
    """
    raise NotImplementedError("Implement megatron_column_row_parallel")
