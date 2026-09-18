"""Tests for Shard Key Range Router."""
from __future__ import annotations

import pytest
from p01_shard_key_range_router import shard_key_range_router


def test_shard_key_range_router():
    chunks = [
        {'min': 0, 'max': 100, 'shard_id': 'shard01'},
        {'min': 100, 'max': 200, 'shard_id': 'shard02'},
        {'min': 200, 'max': 1000, 'shard_id': 'shard03'}
    ]
    assert shard_key_range_router(chunks, 50) == 'shard01'
    assert shard_key_range_router(chunks, 100) == 'shard02'
    assert shard_key_range_router(chunks, 999) == 'shard03'
    assert shard_key_range_router(chunks, 1000) == 'UNROUTED'
