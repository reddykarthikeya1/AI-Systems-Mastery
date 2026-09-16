"""Starter template for covariance and multivariate Gaussian."""
from __future__ import annotations

import numpy as np


class CovarianceEstimator:
    """Sample covariance and correlation matrix calculator."""

    @staticmethod
    def sample_covariance(X: np.ndarray, ddof: int = 1) -> np.ndarray:
        """Compute sample covariance matrix with Bessel's correction."""
        raise NotImplementedError

    @staticmethod
    def correlation_matrix(X: np.ndarray) -> np.ndarray:
        """Compute Pearson correlation matrix normalized between -1 and 1."""
        raise NotImplementedError


class MultivariateGaussian:
    """Multivariate Normal distribution with stable log-PDF and Mahalanobis distance."""

    def __init__(self, jitter: float = 1e-6):
        self.jitter = jitter
        self.mean_: np.ndarray | None = None
        self.cov_: np.ndarray | None = None
        self.cov_inv_: np.ndarray | None = None
        self.log_det_: float = 0.0

    def fit(self, X: np.ndarray) -> MultivariateGaussian:
        """Fit mean and regularized covariance matrix."""
        raise NotImplementedError

    def mahalanobis_distance(self, X: np.ndarray) -> np.ndarray:
        """Compute Mahalanobis distance sqrt((x - mu)^T inv(Sigma) (x - mu))."""
        raise NotImplementedError

    def log_pdf(self, X: np.ndarray) -> np.ndarray:
        """Evaluate multivariate normal log probability density function."""
        raise NotImplementedError
