"""Starter template for PCA and Ordinary Least Squares."""
from __future__ import annotations

import numpy as np


class PCAModel:
    """Principal Component Analysis from scratch via eigen-decomposition."""

    def __init__(self, n_components: int):
        self.n_components = n_components
        self.mean_: np.ndarray | None = None
        self.components_: np.ndarray | None = None
        self.explained_variance_ratio_: np.ndarray | None = None

    def fit(self, X: np.ndarray) -> PCAModel:
        """Fit PCA model by computing covariance and top eigenvectors."""
        raise NotImplementedError

    def transform(self, X: np.ndarray) -> np.ndarray:
        """Project centered X onto principal components."""
        raise NotImplementedError

    def inverse_transform(self, X_proj: np.ndarray) -> np.ndarray:
        """Reconstruct original space from principal components."""
        raise NotImplementedError


class LinearRegressionNormalEq:
    """Ordinary Least Squares and Ridge Regression solver using the Normal Equation."""

    def __init__(self, l2_reg: float = 0.0, fit_intercept: bool = True):
        self.l2_reg = l2_reg
        self.fit_intercept = fit_intercept
        self.coef_: np.ndarray | None = None
        self.intercept_: float = 0.0

    def fit(self, X: np.ndarray, y: np.ndarray) -> LinearRegressionNormalEq:
        """Solve for weights using (X^T X + lambda * I)^(-1) X^T y."""
        raise NotImplementedError

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict target values for input features X."""
        raise NotImplementedError
