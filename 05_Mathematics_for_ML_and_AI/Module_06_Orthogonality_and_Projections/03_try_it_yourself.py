"""Beginner playground for Module 06 - Orthogonality and Projections.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Orthogonal Vector Zero Dot Product
u = [1.0, 2.0, 3.0]
v = [2.0, -1.0, 0.0]

dot_prod = sum(a * b for a, b in zip(u, v))
assert dot_prod == 0.0, "1*2 + 2*(-1) + 3*0 = 0"
print(f"Vectors u and v are orthogonal: dot product = {dot_prod}")

# -------------------------------------------- 2. Vector Projection onto a Line
x = [1.0, 0.0]
y = [3.0, 4.0]

scalar_comp = sum(a * b for a, b in zip(y, x)) / sum(a * a for a in x)
proj = [scalar_comp * a for a in x]

assert proj == [3.0, 0.0]
residual = [y[i] - proj[i] for i in range(2)]
assert residual == [0.0, 4.0]
assert sum(a * b for a, b in zip(proj, residual)) == 0.0, "Projection and residual must be orthogonal"
print(f"Projection of (3, 4) onto x-axis: {proj}, residual shadow: {residual}")

# -------------------------------------------- 3. Pythagorean Theorem for Orthogonal Decompositions
norm_y_sq = sum(a**2 for a in y)
norm_proj_sq = sum(a**2 for a in proj)
norm_res_sq = sum(a**2 for a in residual)

assert abs(norm_y_sq - (norm_proj_sq + norm_res_sq)) < 1e-6
assert norm_y_sq == 25.0  # 3^2 + 4^2 = 25
print(f"Pythagorean theorem satisfied: {norm_y_sq} == {norm_proj_sq} + {norm_res_sq}")

print()
print("All checks passed.")
