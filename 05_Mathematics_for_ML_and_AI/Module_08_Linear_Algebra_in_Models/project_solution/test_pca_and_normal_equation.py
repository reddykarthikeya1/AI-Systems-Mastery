"""Unit tests for PCAModel and LinearRegressionNormalEq."""
from __future__ import annotations

import numpy as np
import pytest
from pca_and_normal_equation import LinearRegressionNormalEq, PCAModel


def test_pca_variance_and_projection():
    np.random.seed(42)
    # Generate 2D data with high variance along x = y
    t = np.linspace(-5, 5, 100)
    x = t + 0.1 * np.random.randn(100)
    y = t + 0.1 * np.random.randn(100)
    data = np.column_stack([x, y])

    pca = PCAModel(n_components=1).fit(data)
    # First component should capture > 98% of variance
    assert pca.explained_variance_ratio_[0] > 0.98

    projected = pca.transform(data)
    assert projected.shape == (100, 1)

    reconstructed = pca.inverse_transform(projected)
    assert reconstructed.shape == (100, 2)
    # Reconstruction should be very close to original
    recon_error = np.mean((data - reconstructed) ** 2)
    assert recon_error < 0.05


def test_ols_exact_fit():
    np.random.seed(42)
    # True relationship: y = 2.5 * x1 - 1.5 * x2 + 4.0
    X = np.random.randn(100, 2)
    true_weights = np.array([2.5, -1.5])
    true_intercept = 4.0
    y = X @ true_weights + true_intercept

    model = LinearRegressionNormalEq(l2_reg=0.0, fit_intercept=True).fit(X, y)
    assert model.coef_ == pytest.approx(true_weights, abs=1e-7)
    assert model.intercept_ == pytest.approx(true_intercept, abs=1e-7)

    preds = model.predict(X)
    assert np.allclose(preds, y, atol=1e-7)


def test_ridge_shrinkage():
    np.random.seed(42)
    # Collinear data where X2 is almost identical to X1
    x1 = np.random.randn(50)
    x2 = x1 + 1e-4 * np.random.randn(50)
    X = np.column_stack([x1, x2])
    y = 3.0 * x1 + np.random.randn(50) * 0.1

    # Unregularized can have huge weights due to collinearity
    ols = LinearRegressionNormalEq(l2_reg=0.0, fit_intercept=False).fit(X, y)
    ridge = LinearRegressionNormalEq(l2_reg=10.0, fit_intercept=False).fit(X, y)

    # Ridge weights should have significantly smaller norm
    assert np.linalg.norm(ridge.coef_) < np.linalg.norm(ols.coef_)
