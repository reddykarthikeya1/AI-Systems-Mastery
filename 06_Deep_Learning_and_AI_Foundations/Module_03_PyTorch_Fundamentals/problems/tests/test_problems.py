"""Tests for Tensor Broadcast Strides."""
from __future__ import annotations

import pytest
from p01_tensor_broadcast_strides import tensor_broadcast_strides


def test_tensor_broadcast_strides():
    assert tensor_broadcast_strides([8, 1, 64], [7, 64]) == [8, 7, 64]
    import pytest
    with pytest.raises(ValueError):
        tensor_broadcast_strides([5], [4])
