"""Beginner playground for Module 07 - Low-Rank Structure and Quadratic Forms.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Outer Product Rank-1 Matrix Construction
u = [1.0, 2.0, 3.0]
v = [4.0, 5.0]

M = [[u[i] * v[j] for j in range(len(v))] for i in range(len(u))]
assert len(M) == 3 and len(M[0]) == 2
assert M[0] == [4.0, 5.0]
assert M[1] == [8.0, 10.0]  # Exactly 2 * row 0
print(f"Rank-1 matrix outer product row 0: {M[0]}, row 1: {M[1]}")

# -------------------------------------------- 2. Evaluating a Quadratic Form x^T A x
A = [[2.0, 0.0],
     [0.0, 3.0]]
x = [2.0, 1.0]

val = sum(x[i] * A[i][j] * x[j] for i in range(2) for j in range(2))
assert val == 2.0 * (2.0**2) + 3.0 * (1.0**2)
assert val == 11.0
print(f"Quadratic form value for x=[2, 1]: {val}")

# -------------------------------------------- 3. Positive Definiteness Verification
test_vectors = [[1.0, 0.0], [0.0, 1.0], [1.0, 1.0], [-2.0, 3.0]]
is_pd = all(sum(v[i] * A[i][j] * v[j] for i in range(2) for j in range(2)) > 0 for v in test_vectors)
assert is_pd is True
print("Matrix A confirmed positive-definite across test vectors.")

print()
print("All checks passed.")
