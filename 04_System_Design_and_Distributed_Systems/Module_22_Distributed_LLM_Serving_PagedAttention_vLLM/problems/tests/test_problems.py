"""Tests for Kv Cache Block Allocator."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_kv_cache_block_allocator import kv_cache_block_allocator
except ImportError:
    from p01_kv_cache_block_allocator import kv_cache_block_allocator


def test_kv_cache_block_allocator():
    alloc = kv_cache_block_allocator(16, [('req_1', 32), ('req_2', 17)], total_physical_blocks=10)
    assert alloc['req_1'] == [0, 1]
    assert alloc['req_2'] == [2, 3]
    import pytest
    with pytest.raises(MemoryError):
        kv_cache_block_allocator(16, [('req_heavy', 200)], total_physical_blocks=2)
