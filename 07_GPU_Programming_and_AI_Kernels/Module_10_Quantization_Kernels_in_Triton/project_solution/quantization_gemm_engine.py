"""Production reference implementation for Quantization GEMM Engine."""
from __future__ import annotations

import numpy as np


def pack_int4_weights(weights_int4: np.ndarray) -> np.ndarray:
    """Pack pairs of 4-bit unsigned integers [0..15] into uint8 array.

    weights_int4: 1D or 2D array of integers in range [0, 15].
    Returns uint8 array of size ceil(size / 2).
    """
    flat = weights_int4.ravel()
    n = flat.size
    pad_len = n % 2
    if pad_len != 0:
        flat = np.pad(flat, (0, 1), mode="constant", constant_values=0)

    low_nibbles = flat[0::2].astype(np.uint8) & 0x0F
    high_nibbles = (flat[1::2].astype(np.uint8) & 0x0F) << 4
    packed = low_nibbles | high_nibbles
    return packed


def unpack_int4_weights(packed: np.ndarray, original_size: int) -> np.ndarray:
    """Unpack uint8 array into 4-bit integers [0..15]."""
    low_nibbles = packed & 0x0F
    high_nibbles = (packed >> 4) & 0x0F

    unpacked = np.empty(packed.size * 2, dtype=np.uint8)
    unpacked[0::2] = low_nibbles
    unpacked[1::2] = high_nibbles
    return unpacked[:original_size]


def dequantize_weights(
    packed: np.ndarray,
    scales: np.ndarray,
    zeros: np.ndarray,
    group_size: int = 128,
    original_size: int | None = None,
) -> np.ndarray:
    """Dequantize packed INT4 weights to float32 using group scales and zeros.

    Formula: W_fp = (W_int4 - zero) * scale.
    """
    n = original_size if original_size is not None else packed.size * 2
    unpacked = unpack_int4_weights(packed, original_size=n).astype(np.float32)

    num_groups = (n + group_size - 1) // group_size
    dequantized = np.empty(n, dtype=np.float32)

    for g in range(num_groups):
        start = g * group_size
        end = min(start + group_size, n)
        scale = scales[g]
        zero = zeros[g]
        dequantized[start:end] = (unpacked[start:end] - zero) * scale

    return dequantized


def quantized_matmul_sim(
    activations: np.ndarray,
    packed_weights: np.ndarray,
    scales: np.ndarray,
    zeros: np.ndarray,
    group_size: int = 128,
) -> np.ndarray:
    """Simulate quantized GEMM: Y = X @ W.T with on-the-fly dequantization.

    activations: (B, K)
    packed_weights: (N, K // 2)
    scales: (N, K // group_size)
    zeros: (N, K // group_size)
    Returns: (B, N)
    """
    b, k = activations.shape
    n = packed_weights.shape[0]

    # Dequantize weights row by row (simulating on-the-fly register unpacking)
    w_dequant = np.empty((n, k), dtype=np.float32)
    for row_idx in range(n):
        w_dequant[row_idx] = dequantize_weights(
            packed_weights[row_idx],
            scales[row_idx],
            zeros[row_idx],
            group_size=group_size,
            original_size=k,
        )

    return (activations @ w_dequant.T).astype(np.float32)
