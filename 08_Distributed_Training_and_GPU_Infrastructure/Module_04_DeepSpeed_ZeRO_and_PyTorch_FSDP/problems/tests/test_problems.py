"""Tests for Zero Memory Partitioning."""
from __future__ import annotations

import pytest
from p01_zero_memory_partitioning import zero_memory_partitioning


def test_zero_memory_partitioning():
    mem = zero_memory_partitioning(10.0, 64)  # 10B model on 64 GPUs
    assert mem['baseline_gb'] == 160.0
    assert mem['zero_3_gb'] == 2.5
