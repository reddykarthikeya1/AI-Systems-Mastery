"""MLE and interval estimation with three planted defects.

Runs to completion, raises nothing, exits 0.
"""
from __future__ import annotations

import math
import random


def mean(values):
    return sum(values) / len(values)


def mle_variance(values):
    """Maximum likelihood estimate of the variance."""
    m = mean(values)
    return sum((v - m) ** 2 for v in values) / len(values)


def log_likelihood_normal(values, mu, sigma):
    """Log likelihood of the data under N(mu, sigma^2)."""
    total = 1.0
    for v in values:
        density = (1.0 / (sigma * math.sqrt(2 * math.pi))) * math.exp(
            -((v - mu) ** 2) / (2 * sigma ** 2))
        total *= density
    return math.log(total) if total > 0 else float("-inf")


def confidence_interval(values, z=1.96):
    """Approximate 95% interval for the mean."""
    m = mean(values)
    sd = math.sqrt(mle_variance(values))
    margin = z * sd
    return m - margin, m + margin


def main():
    print("=" * 66)
    print("MLE ESTIMATOR - parameter report")
    print("=" * 66)

    random.seed(12)
    true_mu, true_sigma = 5.0, 2.0
    sample = [random.gauss(true_mu, true_sigma) for _ in range(8)]

    print()
    print("[1] A small sample from N(5, 4)")
    print(f"    n = {len(sample)}")
    print(f"    sample mean: {mean(sample):.4f}   (true mu = {true_mu})")

    print()
    print("[2] Variance estimate, averaged over many samples")
    estimates = []
    for _ in range(4000):
        s = [random.gauss(true_mu, true_sigma) for _ in range(8)]
        estimates.append(mle_variance(s))
    print(f"    true variance                   : {true_sigma ** 2:.4f}")
    print(f"    average of 4000 MLE estimates   : {mean(estimates):.4f}")
    print(f"    ratio estimate/true             : {mean(estimates) / true_sigma ** 2:.4f}")

    print()
    print("[3] Log likelihood on a larger sample")
    for n in (50, 200, 800):
        big = [random.gauss(true_mu, true_sigma) for _ in range(n)]
        ll = log_likelihood_normal(big, true_mu, true_sigma)
        print(f"    n={n:>4}  log likelihood = {ll}")

    print()
    print("[4] Confidence interval for the mean")
    low, high = confidence_interval(sample)
    print(f"    sample mean: {mean(sample):.4f}")
    print(f"    reported 95% interval: ({low:.4f}, {high:.4f})")
    print(f"    interval width: {high - low:.4f}")

    print()
    print("=" * 66)
    print("Report complete. Exit status 0.")
    print("=" * 66)


if __name__ == "__main__":
    main()
