"""Beginner playground for Module 03 - PyTorch Fundamentals & Computational Graphs.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Forward Graph Evaluation
# Graph: z = (x + y) * w
x, y, w = 2.0, 3.0, 4.0
u = x + y   # Node 1: 5.0
z = u * w   # Node 2: 20.0

assert u == 5.0
assert z == 20.0
print(f"Forward graph evaluated: z={z}")

# -------------------------------------------- 2. Manual Backpropagation (Autograd Simulation)
dz_dz = 1.0
dz_dw = u * dz_dz       # 5.0
dz_du = w * dz_dz       # 4.0
dz_dx = 1.0 * dz_du     # 4.0
dz_dy = 1.0 * dz_du     # 4.0

assert dz_dw == 5.0
assert dz_dx == 4.0
assert dz_dy == 4.0
print(f"Gradients computed: dz/dw={dz_dw}, dz/dx={dz_dx}, dz/dy={dz_dy}")

# -------------------------------------------- 3. Accumulation of Gradients Invariant
# x used in two branches: z = 2*x + 3*x
grad_branch1 = 2.0
grad_branch2 = 3.0
total_dx = grad_branch1 + grad_branch2

assert total_dx == 5.0
assert total_dx == 2.0 + 3.0
print(f"Accumulated gradient across multiple paths: {total_dx}")

print()
print("All checks passed.")
