"""Production reference implementation for Triton Block Execution Engine."""
from __future__ import annotations

import numpy as np


def triton_masked_load(
    data: np.ndarray, offsets: np.ndarray, boundary: int, fill_value: float = 0.0
) -> np.ndarray:
    """Simulate tl.load(ptr + offsets, mask=offsets < boundary, other=fill_value).

    Loads elements at offsets where offset < boundary; fills remaining with fill_value.
    """
    flat = data.ravel()
    out = np.full(offsets.shape, fill_value, dtype=data.dtype)
    valid_mask = (offsets >= 0) & (offsets < boundary)
    valid_offsets = offsets[valid_mask]
    out[valid_mask] = flat[valid_offsets]
    return out


def triton_masked_store(
    target: np.ndarray, offsets: np.ndarray, values: np.ndarray, boundary: int
) -> None:
    """Simulate tl.store(ptr + offsets, values, mask=offsets < boundary).

    Stores values into target only at valid unmasked positions.
    """
    flat = target.ravel()
    valid_mask = (offsets >= 0) & (offsets < boundary)
    valid_offsets = offsets[valid_mask]
    flat[valid_offsets] = values[valid_mask]


def triton_vector_add_sim(
    x: np.ndarray, y: np.ndarray, block_size: int = 128
) -> np.ndarray:
    """Simulate full Triton program launch for elementwise vector addition.

    Launches grid of blocks = ceil(n / block_size).
    Each program_id loads a block with boundary mask, adds, and stores.
    """
    if x.shape != y.shape:
        raise ValueError("Arrays must have identical shapes.")

    n = x.size
    out = np.zeros_like(x)
    num_programs = (n + block_size - 1) // block_size

    for pid in range(num_programs):
        block_start = pid * block_size
        offsets = block_start + np.arange(block_size)
        x_block = triton_masked_load(x, offsets, boundary=n, fill_value=0.0)
        y_block = triton_masked_load(y, offsets, boundary=n, fill_value=0.0)
        sum_block = x_block + y_block
        triton_masked_store(out, offsets, sum_block, boundary=n)

    return out


def triton_block_softmax_sim(x: np.ndarray, block_size: int = 64) -> np.ndarray:
    """Simulate Triton row-wise safe softmax using block reduction.

    In Triton row-wise softmax:
    Each row is processed by one block (or program_id).
    1. tl.load row elements with mask
    2. row_max = tl.max(row, axis=0)
    3. row_exp = tl.exp(row - row_max)
    4. row_sum = tl.sum(row_exp, axis=0)
    5. tl.store(row_exp / row_sum)
    """
    if x.ndim != 2:
        raise ValueError("Input must be a 2D matrix.")

    rows, cols = x.shape
    out = np.zeros_like(x, dtype=np.float64)

    # Next power of 2 for block size >= cols
    bs = block_size
    while bs < cols:
        bs *= 2

    for row_idx in range(rows):
        offsets = np.arange(bs)
        row_data = triton_masked_load(x[row_idx], offsets, boundary=cols, fill_value=-1e9)
        # Block max
        row_max = np.max(row_data)
        # Numerically stable exp
        row_exp = np.exp(row_data - row_max)
        # Mask out values beyond boundary before sum
        row_exp[offsets >= cols] = 0.0
        row_sum = np.sum(row_exp)
        # Softmax probabilities
        softmax_probs = row_exp / (row_sum + 1e-12)
        triton_masked_store(out[row_idx], offsets, softmax_probs, boundary=cols)

    return out
