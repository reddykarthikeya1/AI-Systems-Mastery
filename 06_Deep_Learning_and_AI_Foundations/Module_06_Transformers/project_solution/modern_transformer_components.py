"""Modern Transformer Components: Rotary Position Embeddings (RoPE), SwiGLU, and RMSNorm."""

from __future__ import annotations

from collections.abc import Callable

import numpy as np


class RMSNorm:
    """Root Mean Square Normalization (Zhang & Sennrich, 2019)."""

    def __init__(self, d_model: int, eps: float = 1e-6) -> None:
        self.d_model = d_model
        self.eps = eps
        self.weight = np.ones(d_model, dtype=np.float32)

    def forward(self, x: np.ndarray) -> np.ndarray:
        rms = np.sqrt(np.mean(x * x, axis=-1, keepdims=True) + self.eps)
        return (x / rms) * self.weight


class SwiGLU:
    """Swish Gated Linear Unit Activation (Shazeer, 2020)."""

    @staticmethod
    def forward(
        x: np.ndarray,
        w_gate: np.ndarray,
        w_up: np.ndarray,
        w_down: np.ndarray,
    ) -> np.ndarray:
        gate = x @ w_gate
        swish = gate / (1.0 + np.exp(-gate))
        up = x @ w_up
        return (swish * up) @ w_down


class RotaryPositionEmbedding:
    """Rotary Position Embedding (RoPE) (Su et al., 2021)."""

    def __init__(self, d_head: int, base: float = 10000.0) -> None:
        assert d_head % 2 == 0, "d_head must be even for RoPE"
        self.d_head = d_head
        self.base = base
        half_dim = d_head // 2
        self.theta = 1.0 / (base ** (np.arange(0, half_dim, dtype=np.float32) / half_dim))

    def apply_rope(self, x: np.ndarray, seq_len: int) -> np.ndarray:
        """Applies 2D rotation matrix across pairs of head dimensions."""
        m = np.arange(seq_len, dtype=np.float32)
        angles = np.outer(m, self.theta)

        cos = np.cos(angles)[:, None, :]
        sin = np.sin(angles)[:, None, :]

        x1 = x[..., 0::2]
        x2 = x[..., 1::2]

        x_rot1 = x1 * cos - x2 * sin
        x_rot2 = x1 * sin + x2 * cos

        x_out = np.empty_like(x)
        x_out[..., 0::2] = x_rot1
        x_out[..., 1::2] = x_rot2
        return x_out


def numerical_gradient_check(
    fn: Callable[[np.ndarray], float],
    x: np.ndarray,
    eps: float = 1e-5,
) -> tuple[np.ndarray, np.ndarray]:
    """Computes numerical finite-difference gradient."""
    grad = np.zeros_like(x)
    it = np.nditer(x, flags=["multi_index"], op_flags=["readwrite"])
    while not it.finished:
        idx = it.multi_index
        orig = x[idx]
        x[idx] = orig + eps
        pos = fn(x)
        x[idx] = orig - eps
        neg = fn(x)
        x[idx] = orig
        grad[idx] = (pos - neg) / (2.0 * eps)
        it.iternext()
    return grad, x
