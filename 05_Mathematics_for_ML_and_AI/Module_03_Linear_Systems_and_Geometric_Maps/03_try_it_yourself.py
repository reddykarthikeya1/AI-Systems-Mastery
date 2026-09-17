"""Beginner playground for Module 03 - Linear Systems and Geometric Maps.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Vector Addition and Scalar Scaling
v1 = [2.0, 3.0]
v2 = [4.0, -1.0]

v_sum = [a + b for a, b in zip(v1, v2)]
scaled = [2.5 * x for x in v1]

assert v_sum == [6.0, 2.0]
assert scaled == [5.0, 7.5]
print(f"v1 + v2 = {v_sum}, 2.5 * v1 = {scaled}")

# -------------------------------------------- 2. Matrix-Vector Multiplication as Linear Map
A = [[2.0, 1.0],
     [0.0, 3.0]]
x = [3.0, 2.0]

Ax = [sum(row[i] * x[i] for i in range(len(x))) for row in A]

assert Ax == [8.0, 6.0], "Row 0: 2*3+1*2=8; Row 1: 0*3+3*2=6"
assert len(Ax) == 2
print(f"Matrix A applied to vector x yields: {Ax}")

# -------------------------------------------- 3. 2D Rotation Matrix Invariant
theta = math.pi / 2  # 90 degrees
R = [[math.cos(theta), -math.sin(theta)],
     [math.sin(theta),  math.cos(theta)]]

p = [1.0, 0.0]  # Point on x-axis
p_rot = [sum(R[r][c] * p[c] for c in range(2)) for r in range(2)]

# After 90 deg rotation, (1, 0) becomes (0, 1)
assert abs(p_rot[0] - 0.0) < 1e-6
assert abs(p_rot[1] - 1.0) < 1e-6
orig_len = math.sqrt(p[0]**2 + p[1]**2)
rot_len = math.sqrt(p_rot[0]**2 + p_rot[1]**2)
assert abs(orig_len - rot_len) < 1e-6, "Length must be preserved"
print(f"Point (1, 0) rotated by 90 deg: ({p_rot[0]:.1f}, {p_rot[1]:.1f})")

print()
print("All checks passed.")
