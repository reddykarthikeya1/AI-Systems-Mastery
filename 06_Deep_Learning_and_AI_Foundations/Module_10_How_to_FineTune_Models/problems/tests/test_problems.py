"""Tests for Lora Weight Merge."""
from __future__ import annotations

import pytest
from p01_lora_weight_merge import lora_weight_merge


def test_lora_weight_merge():
    W = [[1.0, 0.0], [0.0, 1.0]]
    B = [[1.0], [0.0]]
    A = [[0.5, 0.5]]
    merged = lora_weight_merge(W, B, A, alpha=4.0, r=1)
    # scale = 4.0. delta = [[0.5, 0.5], [0.0, 0.0]].
    # row 0: [1 + 2.0, 0 + 2.0] = [3.0, 2.0]
    assert merged[0] == [3.0, 2.0]
