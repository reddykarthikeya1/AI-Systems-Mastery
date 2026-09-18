"""Tests for Roofline Model Arithmetic Intensity."""
from __future__ import annotations

import pytest
from p01_roofline_model_arithmetic_intensity import roofline_model_arithmetic_intensity


def test_roofline_model_arithmetic_intensity():
    # H100 GPU: peak 1000 TFLOPS, memory 3000 GB/s -> balance ~ 333 FLOP/byte
    # Vector add: 1 FLOP / 12 bytes -> ~0.08 FLOP/byte (MEMORY_BOUND)
    ai, reg = roofline_model_arithmetic_intensity(1.0, 12.0, 1000.0, 3000.0)
    assert reg == 'MEMORY_BOUND'
    # Dense GEMM: 1000 FLOP / 2 bytes -> 500 FLOP/byte (COMPUTE_BOUND)
    ai2, reg2 = roofline_model_arithmetic_intensity(1000.0, 2.0, 1000.0, 3000.0)
    assert reg2 == 'COMPUTE_BOUND'
