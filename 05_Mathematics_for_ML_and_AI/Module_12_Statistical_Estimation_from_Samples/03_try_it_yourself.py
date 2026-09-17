"""Beginner playground for Module 12 - Statistical Estimation from Samples.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Sample Mean as an Unbiased Estimator
population_mean = 50.0
sample = [48.0, 52.0, 51.0, 49.0, 50.0]

sample_mean = sum(sample) / len(sample)
assert sample_mean == population_mean
print(f"Sample mean: {sample_mean} accurately estimates population mean {population_mean}")

# -------------------------------------------- 2. Bessel's Correction for Sample Variance
n = len(sample)
biased_var = sum((x - sample_mean)**2 for x in sample) / n
unbiased_var = sum((x - sample_mean)**2 for x in sample) / (n - 1)

assert unbiased_var > biased_var, "Bessel's correction increases estimate to eliminate bias"
assert biased_var == 2.0
assert unbiased_var == 2.5
print(f"Biased variance (N={n}): {biased_var}, Unbiased variance (N-1={n-1}): {unbiased_var}")

# -------------------------------------------- 3. Standard Error of the Mean (SEM)
sigma = 10.0
sem_100 = sigma / math.sqrt(100)
sem_400 = sigma / math.sqrt(400)

assert sem_100 == 1.0
assert sem_400 == 0.5, "Quadrupling sample size cuts error in half"
print(f"SEM with N=100: {sem_100}, SEM with N=400: {sem_400}")

print()
print("All checks passed.")
