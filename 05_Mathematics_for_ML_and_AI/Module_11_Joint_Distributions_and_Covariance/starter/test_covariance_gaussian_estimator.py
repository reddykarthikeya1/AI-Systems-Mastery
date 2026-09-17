"""Unit tests for CovarianceEstimator and MultivariateGaussian."""
from __future__ import annotations

import numpy as np
from covariance_gaussian_estimator import CovarianceEstimator, MultivariateGaussian


def test_sample_covariance_matches_numpy():
    np.random.seed(42)
    X = np.random.randn(100, 3)
    our_cov = CovarianceEstimator.sample_covariance(X, ddof=1)
    np_cov = np.cov(X, rowvar=False, ddof=1)
    assert np.allclose(our_cov, np_cov)


def test_correlation_matrix_properties():
    np.random.seed(42)
    X = np.random.randn(50, 4)
    corr = CovarianceEstimator.correlation_matrix(X)
    # Diagonals must be exactly 1.0
    assert np.allclose(np.diag(corr), 1.0)
    # Off-diagonals must be bounded within [-1, 1]
    assert np.all(corr >= -1.0 - 1e-10)
    assert np.all(corr <= 1.0 + 1e-10)


def test_multivariate_gaussian_mahalanobis_and_pdf():
    # Standard 2D normal: mean 0, cov I
    X_train = np.array([[-1.0, 0.0], [1.0, 0.0], [0.0, -1.0], [0.0, 1.0]])
    model = MultivariateGaussian(jitter=0.0).fit(X_train)

    # Point at [1, 1] has squared Euclidean norm 2
    test_pt = np.array([[1.0, 1.0]])
    dist = model.mahalanobis_distance(test_pt)
    assert dist[0] > 0.0

    # Probability at center [0, 0] must be higher than at [1, 1]
    center_pt = np.array([[0.0, 0.0]])
    log_p_center = model.log_pdf(center_pt)
    log_p_outer = model.log_pdf(test_pt)
    assert log_p_center[0] > log_p_outer[0]
