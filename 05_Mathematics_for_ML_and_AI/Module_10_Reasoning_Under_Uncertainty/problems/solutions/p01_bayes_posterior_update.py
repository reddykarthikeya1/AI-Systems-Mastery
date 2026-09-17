"""Reference Solution — Problem 01: Bayes Posterior Update

Topic: 10 Reasoning Under Uncertainty
"""

from __future__ import annotations


def bayes_posterior_update(prior: float, likelihood: float, p_evidence: float) -> float:
    if p_evidence <= 0.0:
        return 0.0
    return round((likelihood * prior) / p_evidence, 4)
