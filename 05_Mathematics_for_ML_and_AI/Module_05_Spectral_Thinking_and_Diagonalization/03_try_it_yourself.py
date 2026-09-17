"""Beginner playground for Module 05 - Spectral Thinking and Diagonalization.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. The Eigenvalue Equation A*v = lambda*v
A = [[2.0, 0.0],
     [0.0, 5.0]]
v1 = [1.0, 0.0]  # Eigenvector corresponding to lambda=2
v2 = [0.0, 1.0]  # Eigenvector corresponding to lambda=5

def mat_vec(M, v):
    return [sum(M[r][c] * v[c] for c in range(len(v))) for r in range(len(M))]

Av1 = mat_vec(A, v1)
Av2 = mat_vec(A, v2)

assert Av1 == [2.0 * x for x in v1]
assert Av2 == [5.0 * x for x in v2]
print(f"Av1 = {Av1} (2*v1), Av2 = {Av2} (5*v2)")

# -------------------------------------------- 2. Matrix Trace and Determinant Spectral Properties
trace = A[0][0] + A[1][1]
det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
eig1, eig2 = 2.0, 5.0

assert trace == eig1 + eig2, "Trace must equal sum of eigenvalues"
assert det == eig1 * eig2, "Determinant must equal product of eigenvalues"
print(f"Trace: {trace} (2+5), Det: {det} (2*5)")

# -------------------------------------------- 3. Matrix Power Acceleration via Diagonalization
k = 3
A_cubed = [[A[0][0]**k, 0.0],
           [0.0, A[1][1]**k]]

assert A_cubed[0][0] == 8.0, "2^3 = 8"
assert A_cubed[1][1] == 125.0, "5^3 = 125"
print(f"A^3 computed via spectral powers: {A_cubed}")

print()
print("All checks passed.")
