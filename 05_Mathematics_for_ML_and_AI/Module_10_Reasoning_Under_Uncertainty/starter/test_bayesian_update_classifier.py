"""Unit tests for BayesianUpdater and GaussianNaiveBayes."""
from __future__ import annotations

import numpy as np
import pytest
from bayesian_update_classifier import BayesianUpdater, GaussianNaiveBayes


def test_rare_disease_bayesian_posterior():
    prior = 0.001
    sensitivity = 0.99
    fpr = 0.05
    posterior = BayesianUpdater.posterior_probability(prior, sensitivity, fpr)
    # Expected: (0.99 * 0.001) / (0.99 * 0.001 + 0.05 * 0.999) = 0.00099 / 0.05094 = ~0.01943
    assert posterior == pytest.approx(0.019434, rel=1e-3)


def test_bayes_filter_update_normalizes():
    priors = np.array([0.25, 0.25, 0.5])
    likelihoods = np.array([0.8, 0.4, 0.1])
    posterior = BayesianUpdater.bayes_filter_update(priors, likelihoods)
    assert np.sum(posterior) == pytest.approx(1.0)
    # Class 0 should have highest updated belief
    assert np.argmax(posterior) == 0


def test_gaussian_naive_bayes_classification():
    np.random.seed(42)
    # Generate two separated clusters
    X_0 = np.random.randn(50, 2) + np.array([-3.0, -3.0])
    X_1 = np.random.randn(50, 2) + np.array([3.0, 3.0])
    X = np.vstack([X_0, X_1])
    y = np.array([0] * 50 + [1] * 50)

    gnb = GaussianNaiveBayes().fit(X, y)
    preds = gnb.predict(X)
    accuracy = np.mean(preds == y)
    assert accuracy == 1.0
