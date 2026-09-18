"""Tests for Layer Norm Fused Moments."""
from __future__ import annotations

import pytest
from p01_layer_norm_fused_moments import layer_norm_fused_moments


def test_layer_norm_fused_moments():
    m, v = layer_norm_fused_moments([2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0])
    assert m == 5.0
    assert v == 4.0
