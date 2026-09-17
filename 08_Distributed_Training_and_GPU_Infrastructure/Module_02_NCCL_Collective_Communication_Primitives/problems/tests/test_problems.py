"""Tests for Ring Allreduce Steps."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_ring_allreduce_steps import ring_allreduce_steps
except ImportError:
    from p01_ring_allreduce_steps import ring_allreduce_steps


def test_ring_allreduce_steps():
    res = ring_allreduce_steps(8000, 8)
    assert res['scatter_bytes'] == 7000.0
    assert res['allgather_bytes'] == 7000.0
    assert res['total_bytes_per_gpu'] == 14000.0
