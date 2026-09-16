"""Starter template for Quantization GEMM Engine."""
from __future__ import annotations

import numpy as np


def pack_int4_weights(weights_int4: np.ndarray) -> np.ndarray:
    """Pack pairs of 4-bit signed/unsigned integers into uint8 array."""
    raise NotImplementedError("Implement pack_int4_weights")


def unpack_int4_weights(packed: np.ndarray, original_size: int) -> np.ndarray:
    """Unpack uint8 array into 4-bit integers."""
    raise NotImplementedError("Implement unpack_int4_weights")


def dequantize_weights(
    packed: np.ndarray,
    scales: np.ndarray,
    zeros: np.ndarray,
    group_size: int = 128,
    original_size: int | None = None,
) -> np.ndarray:
    """Dequantize packed INT4 weights to float32 using group scales and zeros."""
    raise NotImplementedError("Implement dequantize_weights")


def quantized_matmul_sim(
    activations: np.ndarray,
    packed_weights: np.ndarray,
    scales: np.ndarray,
    zeros: np.ndarray,
    group_size: int = 128,
) -> np.ndarray:
    """Simulate quantized GEMM: Y = X @ W.T with on-the-fly dequantization."""
    raise NotImplementedError("Implement quantized_matmul_sim")
