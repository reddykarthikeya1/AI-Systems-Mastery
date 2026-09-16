"""Production solution for MLE and Information Theory metrics."""
from __future__ import annotations

import numpy as np


class ParameterEstimator:
    """Maximum Likelihood Estimation for standard parametric families."""

    @staticmethod
    def gaussian_mle(samples: np.ndarray) -> tuple[float, float]:
        arr = np.asarray(samples, dtype=float)
        if len(arr) == 0:
            return 0.0, 0.0
        mean = float(np.mean(arr))
        # MLE variance divides by N, not N - 1
        var = float(np.mean((arr - mean) ** 2))
        return mean, var

    @staticmethod
    def bernoulli_mle(samples: np.ndarray) -> float:
        arr = np.asarray(samples, dtype=float)
        if len(arr) == 0:
            return 0.0
        return float(np.mean(arr))


class InformationMetrics:
    """Shannon Entropy, Cross-Entropy, and KL Divergence."""

    @staticmethod
    def shannon_entropy(p: np.ndarray, base: float = 2.0, tol: float = 1e-12) -> float:
        p_arr = np.asarray(p, dtype=float)
        # Filter out zeros where 0 * log(0) = 0
        p_valid = p_arr[p_arr > tol]
        return float(-np.sum(p_valid * (np.log(p_valid) / np.log(base))))

    @staticmethod
    def cross_entropy(
        p: np.ndarray, q: np.ndarray, base: float = 2.0, tol: float = 1e-12
    ) -> float:
        p_arr = np.asarray(p, dtype=float)
        q_arr = np.asarray(q, dtype=float)
        q_clipped = np.clip(q_arr, tol, 1.0)
        # Only sum where p > 0
        mask = p_arr > tol
        return float(-np.sum(p_arr[mask] * (np.log(q_clipped[mask]) / np.log(base))))

    @staticmethod
    def kl_divergence(
        p: np.ndarray, q: np.ndarray, base: float = 2.0, tol: float = 1e-12
    ) -> float:
        p_arr = np.asarray(p, dtype=float)
        q_arr = np.asarray(q, dtype=float)
        q_clipped = np.clip(q_arr, tol, 1.0)
        mask = p_arr > tol
        ratio = p_arr[mask] / q_clipped[mask]
        return float(np.sum(p_arr[mask] * (np.log(ratio) / np.log(base))))
