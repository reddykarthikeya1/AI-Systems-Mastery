"""Tests for Compute 3D Rank Coordinates."""
from __future__ import annotations

import pytest
from p01_compute_3d_rank_coordinates import compute_3d_rank_coordinates


def test_compute_3d_rank_coordinates():
    # TP=2, PP=4, DP=8 -> total 64 ranks
    dp, pp, tp = compute_3d_rank_coordinates(11, 2, 4, 8)
    # 11 % 2 = 1 (tp=1). 11 // 2 = 5. 5 % 4 = 1 (pp=1). 5 // 4 = 1 (dp=1).
    assert (dp, pp, tp) == (1, 1, 1)
