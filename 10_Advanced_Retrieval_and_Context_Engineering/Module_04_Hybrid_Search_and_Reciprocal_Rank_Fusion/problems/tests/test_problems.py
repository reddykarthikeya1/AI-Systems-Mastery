"""Tests for Reciprocal Rank Fusion Merge."""
from __future__ import annotations

import pytest
from p01_reciprocal_rank_fusion_merge import reciprocal_rank_fusion_merge


def test_reciprocal_rank_fusion_merge():
    dense = ["docA", "docB"]
    sparse = ["docB", "docC"]
    merged = reciprocal_rank_fusion_merge(dense, sparse, 60)
    # docB appears in both: 1/62 + 1/61 ~= 0.0325
    assert merged[0][0] == "docB"
