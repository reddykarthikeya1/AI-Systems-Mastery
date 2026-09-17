"""Beginner playground for Module 02 - Core AI Intuitions & Gradient Descent.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. 1D Gradient Descent Iteration
# Minimize L(w) = (w - 4)^2; derivative is 2*(w - 4)
w = 0.0
lr = 0.2
for _ in range(10):
    grad = 2.0 * (w - 4.0)
    w -= lr * grad

assert abs(w - 4.0) < 0.1, "Weight must converge near 4.0"
print(f"Converged weight after 10 steps: {w:.4f} (target: 4.0)")

# -------------------------------------------- 2. Learning Rate Stability Bounds
w_divergent = 0.0
bad_lr = 1.1  # For loss with curvature 2, lr > 1.0 diverges
for _ in range(3):
    grad = 2.0 * (w_divergent - 4.0)
    w_divergent -= bad_lr * grad

assert abs(w_divergent - 4.0) > 4.0, "Divergence creates expanding oscillations"
print(f"Divergent weight after unstable learning rate: {w_divergent:.2f}")

# -------------------------------------------- 3. Loss Function Monotonic Reduction
def loss(val): return (val - 4.0)**2
w_step = 0.0
l1 = loss(w_step)
w_step -= 0.1 * 2.0 * (w_step - 4.0)
l2 = loss(w_step)
assert l2 < l1
assert l1 == 16.0
print(f"Loss decreased from {l1} to {l2}")

print()
print("All checks passed.")
