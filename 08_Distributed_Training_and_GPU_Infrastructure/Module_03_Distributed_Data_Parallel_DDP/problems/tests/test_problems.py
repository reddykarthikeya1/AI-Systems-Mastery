"""Tests for Bucket Gradient Allreduce."""
from __future__ import annotations

import pytest
from p01_bucket_gradient_allreduce import bucket_gradient_allreduce


def test_bucket_gradient_allreduce():
    params = [10.0, 15.0, 20.0, 10.0]  # indices 0, 1, 2, 3
    # Reverse order: 3 (10MB) + 2 (20MB) > 25MB -> bucket 1: [3], bucket 2: [2], bucket 3: [1, 0]
    buckets = bucket_gradient_allreduce(params, 25.0)
    assert buckets[0] == [3]
    assert buckets[1] == [2]
    assert buckets[2] == [1, 0]
