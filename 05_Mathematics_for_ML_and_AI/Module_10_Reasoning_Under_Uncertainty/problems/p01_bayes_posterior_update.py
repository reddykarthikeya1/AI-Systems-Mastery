"""Problem 01 — Bayes Posterior Update

Topic: 10 Reasoning Under Uncertainty
Target: Production-grade implementation

Compute Bayesian posterior probability P(Hypothesis | Evidence).

Example:
    >>> bayes_posterior_update(0.01, 0.9, 0.05)
    0.18

Hints:
    Hint 1: The posterior reweights the prior by how much more (or less)
        likely the evidence is under this hypothesis than on average —
        that ratio is exactly `likelihood / p_evidence`.
    Hint 2: Apply Bayes' rule directly: multiply `prior * likelihood` and
        divide by `p_evidence`.
    Hint 3: `p_evidence` of 0.0 (or negative, which shouldn't occur but
        could from bad input) makes the division undefined — return 0.0 in
        that case instead of raising, and round the normal-case result to
        4 decimal places.
"""

from __future__ import annotations


def bayes_posterior_update(prior: float, likelihood: float, p_evidence: float) -> float:
    """Bayes rule: P(H|E) = (likelihood * prior) / p_evidence.
    Returns posterior rounded to 4 decimals.
    """
    raise NotImplementedError("Implement bayes_posterior_update")
