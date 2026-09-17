"""Tests for Concurrency Queue Autoscaler."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_concurrency_queue_autoscaler import concurrency_queue_autoscaler
except ImportError:
    from p01_concurrency_queue_autoscaler import concurrency_queue_autoscaler


def test_concurrency_queue_autoscaler():
    assert concurrency_queue_autoscaler(20, 10, target_concurrency_per_pod=10, min_pods=1, max_pods=5) == 3
    assert concurrency_queue_autoscaler(0, 0, 10, min_pods=2, max_pods=10) == 2
    assert concurrency_queue_autoscaler(500, 500, 10, min_pods=1, max_pods=10) == 10
