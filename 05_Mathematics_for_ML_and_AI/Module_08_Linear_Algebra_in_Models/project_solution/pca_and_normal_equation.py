"""Production solution for PCA and Ordinary Least Squares."""
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
        X = np.asarray(X, dtype=float)
        n_samples, _ = X.shape
        self.mean_ = np.mean(X, axis=0)
        X_centered = X - self.mean_

        # Sample covariance matrix
        cov = (X_centered.T @ X_centered) / (n_samples - 1)

        # Eigen decomposition of symmetric covariance
        evals, evecs = np.linalg.eigh(cov)

        # Sort in descending order
        idx = np.argsort(evals)[::-1]
        evals = evals[idx]
        evecs = evecs[:, idx]

        total_var = np.sum(evals)
        self.explained_variance_ratio_ = (
            evals[: self.n_components] / total_var if total_var > 0 else np.zeros(self.n_components)
        )
        self.components_ = evecs[:, : self.n_components]  # Columns are principal axes
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        if self.mean_ is None or self.components_ is None:
            raise RuntimeError("Model is not fitted.")
        X = np.asarray(X, dtype=float)
        X_centered = X - self.mean_
        return X_centered @ self.components_

    def inverse_transform(self, X_proj: np.ndarray) -> np.ndarray:
        if self.mean_ is None or self.components_ is None:
            raise RuntimeError("Model is not fitted.")
        X_proj = np.asarray(X_proj, dtype=float)
        return (X_proj @ self.components_.T) + self.mean_


class LinearRegressionNormalEq:
    """Ordinary Least Squares and Ridge Regression solver using the Normal Equation."""

    def __init__(self, l2_reg: float = 0.0, fit_intercept: bool = True):
        self.l2_reg = l2_reg
        self.fit_intercept = fit_intercept
        self.coef_: np.ndarray | None = None
        self.intercept_: float = 0.0

    def fit(self, X: np.ndarray, y: np.ndarray) -> LinearRegressionNormalEq:
        X = np.asarray(X, dtype=float)
        y = np.asarray(y, dtype=float)
        n_samples, n_features = X.shape

        if self.fit_intercept:
            # Augment with column of ones
            X_design = np.hstack([np.ones((n_samples, 1)), X])
            reg_eye = np.eye(n_features + 1)
            reg_eye[0, 0] = 0.0  # Do not regularize bias term
        else:
            X_design = X
            reg_eye = np.eye(n_features)

        # Solve (X^T X + lambda * I) w = X^T y
        lhs = X_design.T @ X_design + self.l2_reg * reg_eye
        rhs = X_design.T @ y

        w = np.linalg.solve(lhs, rhs)

        if self.fit_intercept:
            self.intercept_ = float(w[0])
            self.coef_ = w[1:]
        else:
            self.intercept_ = 0.0
            self.coef_ = w
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        if self.coef_ is None:
            raise RuntimeError("Model is not fitted.")
        X = np.asarray(X, dtype=float)
        return (X @ self.coef_) + self.intercept_
