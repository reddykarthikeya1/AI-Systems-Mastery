"""Starter template for Fused Normalization and Activations Engine."""
from __future__ import annotations

import numpy as np


def fused_rmsnorm(x: np.ndarray, weight: np.ndarray, eps: float = 1e-6) -> np.ndarray:
    """Compute Root Mean Square Normalization in a single fused pass."""
    raise NotImplementedError("Implement fused_rmsnorm")


def fused_swiglu(gate: np.ndarray, up: np.ndarray) -> np.ndarray:
    """Compute fused SwiGLU activation: (gate * sigmoid(gate)) * up."""
    raise NotImplementedError("Implement fused_swiglu")


def online_safe_softmax_step(
    m_prev: float,
    l_prev: float,
    acc_prev: np.ndarray,
    new_block_scores: np.ndarray,
    new_block_values: np.ndarray,
) -> tuple[float, float, np.ndarray]:
    """Perform one step of online softmax accumulating P @ V."""
    raise NotImplementedError("Implement online_safe_softmax_step")
