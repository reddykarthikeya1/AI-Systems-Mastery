"""Unit tests for ParameterEstimator and InformationMetrics."""
from __future__ import annotations

import numpy as np
import pytest
from mle_information_metrics import InformationMetrics, ParameterEstimator


def test_mle_parameter_recovery():
    np.random.seed(42)
    # Gaussian MLE
    true_mean = 5.0
    true_std = 2.0
    samples = np.random.normal(true_mean, true_std, size=10000)
    mu_hat, var_hat = ParameterEstimator.gaussian_mle(samples)
    assert mu_hat == pytest.approx(true_mean, abs=0.1)
    assert var_hat == pytest.approx(true_std**2, abs=0.2)

    # Bernoulli MLE
    flips = np.array([1, 1, 1, 1, 0, 0, 0, 0, 1, 0])
    p_hat = ParameterEstimator.bernoulli_mle(flips)
    assert p_hat == pytest.approx(0.5)


def test_shannon_entropy_fair_coin_and_uniform():
    # Fair coin has entropy 1.0 bit
    fair_coin = np.array([0.5, 0.5])
    assert InformationMetrics.shannon_entropy(fair_coin, base=2.0) == pytest.approx(1.0)

    # 8-sided die has log2(8) = 3.0 bits
    die_8 = np.ones(8) / 8.0
    assert InformationMetrics.shannon_entropy(die_8, base=2.0) == pytest.approx(3.0)


def test_kl_divergence_properties_and_identity():
    p = np.array([0.7, 0.3])
    q = np.array([0.5, 0.5])

    # Non-negativity D_KL >= 0
    kl_pq = InformationMetrics.kl_divergence(p, q, base=2.0)
    assert kl_pq > 0.0

    # Self-divergence D_KL(P || P) == 0
    assert InformationMetrics.kl_divergence(p, p, base=2.0) == pytest.approx(0.0)

    # Master identity: H(P, Q) == H(P) + D_KL(P || Q)
    h_p = InformationMetrics.shannon_entropy(p, base=2.0)
    h_pq = InformationMetrics.cross_entropy(p, q, base=2.0)
    assert h_pq == pytest.approx(h_p + kl_pq)
