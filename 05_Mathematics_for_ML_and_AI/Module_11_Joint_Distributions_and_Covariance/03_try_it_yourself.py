"""Beginner playground for Module 11 - Joint Distributions and Covariance.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Expected Value (Mean) Calculation
outcomes = [1, 2, 3, 4, 5, 6]
probs = [1/6] * 6

expected_value = sum(x * p for x, p in zip(outcomes, probs))
assert abs(expected_value - 3.5) < 1e-6
print(f"Expected value of fair 6-sided die: {expected_value}")

# -------------------------------------------- 2. Variance and Standard Deviation
data = [10.0, 12.0, 23.0, 23.0, 16.0, 23.0, 21.0, 16.0]
mean = sum(data) / len(data)
variance = sum((x - mean)**2 for x in data) / len(data)
std_dev = math.sqrt(variance)

assert abs(mean - 18.0) < 1e-6
assert variance > 0.0
assert std_dev == math.sqrt(variance)
print(f"Dataset mean: {mean}, variance: {variance:.2f}, std dev: {std_dev:.2f}")

# -------------------------------------------- 3. Sample Covariance and Positive Correlation
xs = [1.0, 2.0, 3.0, 4.0, 5.0]
ys = [2.0, 4.0, 6.0, 8.0, 10.0]  # y = 2x, perfect correlation

mean_x = sum(xs) / len(xs)
mean_y = sum(ys) / len(ys)
cov = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys)) / len(xs)

assert cov > 0.0, "Positive covariance"
assert cov == 4.0
print(f"Covariance between x and 2x: {cov}")

print()
print("All checks passed.")
