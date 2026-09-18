"""Tests for Int8 Symmetric Quantization."""
from __future__ import annotations

import pytest
from p01_int8_symmetric_quantization import int8_symmetric_quantization


def test_int8_symmetric_quantization():
    scale, q = int8_symmetric_quantization([-127.0, 0.0, 127.0])
    assert scale == 1.0
    assert q == [-127, 0, 127]
