"""Tests for Kv Cache Footprint Estimator."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_kv_cache_footprint_estimator import kv_cache_footprint_estimator
except ImportError:
    from p01_kv_cache_footprint_estimator import kv_cache_footprint_estimator


def test_kv_cache_footprint_estimator():
    # 32 layers, 8 KV heads (GQA), 128 dim, 4096 tokens, FP16 (2 bytes)
    # bytes_per_tok = 2 * 32 * 8 * 128 * 2 = 131,072 bytes (128 KB)
    # 4096 tokens = 128 KB * 4096 = 536,870,912 bytes (512 MB)
    mem = kv_cache_footprint_estimator(32, 8, 128, 4096, 2)
    assert mem == 536870912
