"""Reference Solution — Problem 01: Megatron Column Row Parallel

Topic: 05 Tensor Parallelism Megatron LM
"""

from __future__ import annotations


def megatron_column_row_parallel(hidden_dim: int, ffn_dim: int, tp_world_size: int) -> dict[str, int]:
    return {
        'w1_cols_per_rank': ffn_dim // tp_world_size,
        'w2_rows_per_rank': ffn_dim // tp_world_size,
        'allreduce_calls_per_mlp': 1  # only 1 all-reduce after row-parallel linear!
    }
