"""Production reference implementation for Fused Normalization and Activations Engine."""
from __future__ import annotations

import numpy as np


def fused_rmsnorm(x: np.ndarray, weight: np.ndarray, eps: float = 1e-6) -> np.ndarray:
    """Compute Root Mean Square Normalization in a single fused pass.

    Formula: y_i = (x_i / sqrt(mean(x^2) + eps)) * weight_i
    In GPU hardware, this is computed within registers/SRAM in one memory roundtrip.
    """
    if x.ndim < 1:
        raise ValueError("Input array must have at least 1 dimension.")

    dim = x.shape[-1]
    if weight.shape != (dim,):
        raise ValueError(f"Weight shape {weight.shape} must match hidden dimension {dim}.")

    # Mean square across the last dimension
    mean_sq = np.mean(x ** 2, axis=-1, keepdims=True)
    r_rms = 1.0 / np.sqrt(mean_sq + eps)

    return (x * r_rms) * weight


def fused_swiglu(gate: np.ndarray, up: np.ndarray) -> np.ndarray:
    """Compute fused SwiGLU activation: (gate * sigmoid(gate)) * up.

    Swish(x) = x * sigmoid(x) = x / (1 + exp(-x)).
    Fused execution computes sigmoid and multiplications without writing intermediate
    gate activations back to HBM.
    """
    if gate.shape != up.shape:
        raise ValueError("Gate and up projection arrays must have identical shapes.")

    # Numerically stable sigmoid
    # For gate >= 0: 1 / (1 + exp(-gate))
    # For gate < 0: exp(gate) / (1 + exp(gate))
    sigmoid_gate = np.where(
        gate >= 0,
        1.0 / (1.0 + np.exp(-gate)),
        np.exp(gate) / (1.0 + np.exp(gate))
    )

    swish_gate = gate * sigmoid_gate
    return swish_gate * up


def online_safe_softmax_step(
    m_prev: float,
    l_prev: float,
    acc_prev: np.ndarray,
    new_block_scores: np.ndarray,
    new_block_values: np.ndarray,
) -> tuple[float, float, np.ndarray]:
    """Perform one step of online softmax accumulating P @ V.

    Online Softmax recurrence (Milakov & Gimelshein / FlashAttention):
    m_curr = max(m_prev, max(new_block_scores))
    factor_prev = exp(m_prev - m_curr)
    p_new = exp(new_block_scores - m_curr)
    l_curr = l_prev * factor_prev + sum(p_new)
    acc_curr = acc_prev * factor_prev + (p_new @ new_block_values)

    Returns:
        tuple of (m_curr, l_curr, acc_curr).
    """
    m_new = float(np.max(new_block_scores))
    m_curr = max(m_prev, m_new)

    factor_prev = float(np.exp(m_prev - m_curr))
    p_new = np.exp(new_block_scores - m_curr)

    l_curr = float(l_prev * factor_prev + np.sum(p_new))
    acc_curr = acc_prev * factor_prev + np.dot(p_new, new_block_values)

    return m_curr, l_curr, acc_curr
