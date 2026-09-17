"""Unit tests for NCCL Collectives Simulator."""
from __future__ import annotations

import numpy as np
import pytest
from nccl_primitives_sim import (
    alpha_beta_cost_model,
    ring_allgather,
    ring_allreduce,
    ring_reducescatter,
)


def test_ring_allreduce_correctness() -> None:
    # 4 ranks, each with array of 8 elements
    num_ranks = 4
    tensors = [np.full(8, fill_value=float(r + 1), dtype=np.float64) for r in range(num_ranks)]

    reduced, bytes_sent = ring_allreduce(tensors)

    # Sum of [1, 2, 3, 4] = 10
    for r in range(num_ranks):
        np.testing.assert_allclose(reduced[r], np.full(8, 10.0))

    assert bytes_sent > 0


def test_reducescatter_and_allgather() -> None:
    tensors = [np.array([1.0, 2.0, 3.0, 4.0]) for _ in range(4)]
    # Sum of 4 identical tensors = [4.0, 8.0, 12.0, 16.0]
    shards = ring_reducescatter(tensors)
    assert len(shards) == 4
    assert pytest.approx(float(shards[0][0]), rel=1e-5) == 4.0
    assert pytest.approx(float(shards[1][0]), rel=1e-5) == 8.0

    gathered = ring_allgather(shards)
    np.testing.assert_allclose(gathered[0], np.array([4.0, 8.0, 12.0, 16.0]))


def test_alpha_beta_model() -> None:
    # 8 ranks, 10 MB payload
    size = 10 * 1024 * 1024
    time_s = alpha_beta_cost_model(size_bytes=size, num_ranks=8)
    assert time_s > 0.0
