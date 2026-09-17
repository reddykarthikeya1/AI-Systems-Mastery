"""Beginner playground for Module 04 - Vector Spaces, Bases, and Rank.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Dot Product and Vector Length
def dot(u, v):
    return sum(a * b for a, b in zip(u, v))

def norm(u):
    return math.sqrt(dot(u, u))

a = [3.0, 4.0]
b = [4.0, -3.0]

assert dot(a, b) == 0.0, "Orthogonal vectors have dot product 0"
assert norm(a) == 5.0, "3-4-5 right triangle length"
print(f"Dot product: {dot(a, b)}, Norm of a: {norm(a)}")

# -------------------------------------------- 2. Linear Independence Check in 2D
def is_linearly_independent_2d(u, v):
    det = u[0] * v[1] - u[1] * v[0]
    return abs(det) > 1e-9

v1 = [1.0, 2.0]
v2 = [2.0, 4.0]  # Dependent: 2 * v1
v3 = [0.0, 1.0]  # Independent

assert is_linearly_independent_2d(v1, v2) is False
assert is_linearly_independent_2d(v1, v3) is True
print("Linear independence tests validated in 2D.")

# -------------------------------------------- 3. Matrix Rank and Column Space Dimension
def rank_2x2(A):
    det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    if abs(det) > 1e-9:
        return 2
    if any(A[r][c] != 0 for r in range(2) for c in range(2)):
        return 1
    return 0

full_rank = [[1, 2], [3, 4]]
rank_1 = [[1, 2], [2, 4]]
assert rank_2x2(full_rank) == 2
assert rank_2x2(rank_1) == 1
print(f"Rank of full-rank matrix: {rank_2x2(full_rank)}, rank of dependent matrix: {rank_2x2(rank_1)}")

print()
print("All checks passed.")
