"""Tests for Fp8 E4M3 Dequantize."""
from __future__ import annotations

import pytest
try:
    from solutions.p01_fp8_e4m3_dequantize import fp8_e4m3_dequantize
except ImportError:
    from p01_fp8_e4m3_dequantize import fp8_e4m3_dequantize


def test_fp8_e4m3_dequantize():
    assert fp8_e4m3_dequantize([10, -5, 0], 0.05) == [0.5, -0.25, 0.0]
