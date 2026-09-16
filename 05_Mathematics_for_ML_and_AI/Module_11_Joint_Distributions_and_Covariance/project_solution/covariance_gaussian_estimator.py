"""Production solution for covariance and multivariate Gaussian."""
from __future__ import annotations

import numpy as np


class CovarianceEstimator:
    """Sample covariance and correlation matrix calculator."""

    @staticmethod
    def sample_covariance(X: np.ndarray, ddof: int = 1) -> np.ndarray:
        X = np.asarray(X, dtype=float)
        n_samples = X.shape[0]
        mean = np.mean(X, axis=0)
        X_centered = X - mean
        return (X_centered.T @ X_centered) / (n_samples - ddof)

    @staticmethod
    def correlation_matrix(X: np.ndarray) -> np.ndarray:
        cov = CovarianceEstimator.sample_covariance(X)
        diag_std = np.sqrt(np.diag(cov))
        # Prevent division by zero
        diag_std[diag_std == 0.0] = 1e-12
        return cov / np.outer(diag_std, diag_std)


class MultivariateGaussian:
    """Multivariate Normal distribution with stable log-PDF and Mahalanobis distance."""

    def __init__(self, jitter: float = 1e-6):
        self.jitter = jitter
        self.mean_: np.ndarray | None = None
        self.cov_: np.ndarray | None = None
        self.cov_inv_: np.ndarray | None = None
        self.log_det_: float = 0.0

    def fit(self, X: np.ndarray) -> MultivariateGaussian:
        X = np.asarray(X, dtype=float)
        _, d = X.shape
        self.mean_ = np.mean(X, axis=0)
        cov = CovarianceEstimator.sample_covariance(X)
        self.cov_ = cov + self.jitter * np.eye(d)
        self.cov_inv_ = np.linalg.inv(self.cov_)

        # Stable log-determinant
        sign, logdet = np.linalg.slogdet(self.cov_)
        if sign <= 0:
            raise ValueError("Covariance matrix must be strictly positive definite.")
        self.log_det_ = float(logdet)
        return self

    def mahalanobis_distance(self, X: np.ndarray) -> np.ndarray:
        if self.mean_ is None or self.cov_inv_ is None:
            raise RuntimeError("Model is not fitted.")
        X = np.asarray(X, dtype=float)
        diff = X - self.mean_
        # (diff @ cov_inv) * diff summed across features
        sq_dist = np.sum((diff @ self.cov_inv_) * diff, axis=1)
        return np.sqrt(np.maximum(sq_dist, 0.0))

    def log_pdf(self, X: np.ndarray) -> np.ndarray:
        if self.mean_ is None or self.cov_inv_ is None:
            raise RuntimeError("Model is not fitted.")
        X = np.asarray(X, dtype=float)
        d = len(self.mean_)
        sq_mahal = self.mahalanobis_distance(X) ** 2
        # -0.5 * (d * log(2*pi) + log|Sigma| + (x-mu)^T inv(Sigma) (x-mu))
        return -0.5 * (d * np.log(2.0 * np.pi) + self.log_det_ + sq_mahal)
