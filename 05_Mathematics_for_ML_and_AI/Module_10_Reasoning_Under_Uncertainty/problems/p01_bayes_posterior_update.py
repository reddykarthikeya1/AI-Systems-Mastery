"""Problem 01 — Bayes Posterior Update

Topic: 10 Reasoning Under Uncertainty
Target: Production-grade implementation

Compute Bayesian posterior probability P(Hypothesis | Evidence).

Hints:
    Hint 1: Review module invariants and mathematical definitions.
    Hint 2: Handle edge cases, dimensions, and numerical stability cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def bayes_posterior_update(prior: float, likelihood: float, p_evidence: float) -> float:
    """Bayes rule: P(H|E) = (likelihood * prior) / p_evidence.
    Returns posterior rounded to 4 decimals.
    """
    raise NotImplementedError("Implement bayes_posterior_update")
