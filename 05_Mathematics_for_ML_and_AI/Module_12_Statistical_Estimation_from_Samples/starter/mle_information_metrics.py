"""Starter template for MLE and Information Theory metrics."""
from __future__ import annotations

import numpy as np


class ParameterEstimator:
    """Maximum Likelihood Estimation for standard parametric families."""

    @staticmethod
    def gaussian_mle(samples: np.ndarray) -> tuple[float, float]:
        """Compute MLE for Gaussian parameters (mean, sample variance)."""
        raise NotImplementedError

    @staticmethod
    def bernoulli_mle(samples: np.ndarray) -> float:
        """Compute MLE for Bernoulli parameter p (probability of success)."""
        raise NotImplementedError


class InformationMetrics:
    """Shannon Entropy, Cross-Entropy, and KL Divergence."""

    @staticmethod
    def shannon_entropy(p: np.ndarray, base: float = 2.0, tol: float = 1e-12) -> float:
        """Compute Shannon Entropy H(P) = -sum(p * log_b(p))."""
        raise NotImplementedError

    @staticmethod
    def cross_entropy(p: np.ndarray, q: np.ndarray, base: float = 2.0, tol: float = 1e-12) -> float:
        """Compute Cross-Entropy H(P, Q) = -sum(p * log_b(q))."""
        raise NotImplementedError

    @staticmethod
    def kl_divergence(p: np.ndarray, q: np.ndarray, base: float = 2.0, tol: float = 1e-12) -> float:
        """Compute KL Divergence D_KL(P || Q) = sum(p * log_b(p / q))."""
        raise NotImplementedError
