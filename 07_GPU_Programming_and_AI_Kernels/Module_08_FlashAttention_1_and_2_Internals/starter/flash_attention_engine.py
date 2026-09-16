"""Starter template for FlashAttention Engine."""
from __future__ import annotations

import numpy as np


def flash_attention_forward(
    q: np.ndarray,
    k: np.ndarray,
    v: np.ndarray,
    block_r: int = 16,
    block_c: int = 16,
) -> tuple[np.ndarray, int, int]:
    """Execute IO-aware FlashAttention forward algorithm.

    Returns:
        tuple of (output_matrix, hbm_reads, hbm_writes).
    """
    raise NotImplementedError("Implement flash_attention_forward")
