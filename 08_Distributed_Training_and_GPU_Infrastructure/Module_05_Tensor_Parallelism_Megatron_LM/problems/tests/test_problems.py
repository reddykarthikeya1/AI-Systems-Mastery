"""Tests for Megatron Column Row Parallel."""
from __future__ import annotations

import pytest
from p01_megatron_column_row_parallel import megatron_column_row_parallel


def test_megatron_column_row_parallel():
    tp = megatron_column_row_parallel(4096, 16384, 8)
    assert tp['w1_cols_per_rank'] == 2048
    assert tp['w2_rows_per_rank'] == 2048
    assert tp['allreduce_calls_per_mlp'] == 1
