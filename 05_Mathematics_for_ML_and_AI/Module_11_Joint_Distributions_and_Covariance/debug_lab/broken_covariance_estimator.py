"""Covariance estimation with three planted defects.

Runs to completion, raises nothing, exits 0.
"""
from __future__ import annotations

import math


def mean(values):
    return sum(values) / len(values)


def variance(values):
    m = mean(values)
    return sum((v - m) ** 2 for v in values) / len(values)


def covariance(xs, ys):
    mx, my = mean(xs), mean(ys)
    return sum((a - mx) * (b - my) for a, b in zip(xs, ys)) / (len(xs) - 1)


def correlation(xs, ys):
    return covariance(xs, ys) / (variance(xs) * variance(ys))


def main():
    print("=" * 66)
    print("COVARIANCE ESTIMATOR - dataset summary")
    print("=" * 66)

    xs = [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]
    ys = [4.0, 8.0, 8.0, 8.0, 10.0, 10.0, 14.0, 18.0]   # exactly 2 * xs

    print()
    print("[1] The data")
    print(f"    xs = {xs}")
    print(f"    ys = 2 * xs")
    print(f"    mean(xs) = {mean(xs)}   mean(ys) = {mean(ys)}")

    print()
    print("[2] Variance: population versus sample")
    m = mean(xs)
    pop = sum((v - m) ** 2 for v in xs) / len(xs)
    samp = sum((v - m) ** 2 for v in xs) / (len(xs) - 1)
    print(f"    variance() returns        : {variance(xs):.6f}")
    print(f"    dividing by n     gives   : {pop:.6f}")
    print(f"    dividing by n - 1 gives   : {samp:.6f}")
    print(f"    covariance() divides by n - 1: {covariance(xs, xs):.6f}")

    print()
    print("[3] Correlation of a perfectly linear relationship")
    r = correlation(xs, ys)
    print(f"    ys = 2 * xs exactly, so the correlation must be 1.0")
    print(f"    correlation() reports: {r:.6f}")
    print(f"    is it within [-1, 1]? {-1.0 <= r <= 1.0}")

    small = [0.1, 0.2, 0.3, 0.4]
    small_y = [2 * v for v in small]
    r2 = correlation(small, small_y)
    print(f"    the same relationship on a narrower spread {small}:")
    print(f"    correlation() reports: {r2:.6f}")
    print(f"    is it within [-1, 1]? {-1.0 <= r2 <= 1.0}")

    print()
    print("=" * 66)
    print("Report complete. Exit status 0.")
    print("=" * 66)


if __name__ == "__main__":
    main()
