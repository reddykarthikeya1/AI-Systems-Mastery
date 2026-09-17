"""Beginner playground for Module 05 - Neural Network from Scratch.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. 2-Layer Forward Propagation
x = [1.0, -1.0]
W1 = [[0.5, 0.2], [-0.3, 0.8]]
b1 = [0.1, -0.1]

# Layer 1 pre-activation and ReLU
h_pre = [sum(W1[r][c] * x[c] for c in range(2)) + b1[r] for r in range(2)]
h_act = [max(0.0, val) for val in h_pre]

assert abs(h_pre[0] - (0.5 * 1.0 + 0.2 * (-1.0) + 0.1)) < 1e-6
assert abs(h_pre[0] - 0.4) < 1e-6
assert h_act[0] == 0.4
print(f"Hidden layer activations: {h_act}")

# -------------------------------------------- 2. Binary Cross-Entropy Loss
def bce(y_true, y_prob):
    eps = 1e-15
    y_prob = max(eps, min(1.0 - eps, y_prob))
    return -(y_true * math.log(y_prob) + (1.0 - y_true) * math.log(1.0 - y_prob))

loss_correct = bce(1.0, 0.99)
loss_wrong = bce(1.0, 0.01)

assert loss_wrong > loss_correct
assert loss_correct < 0.02
print(f"BCE Loss confident correct: {loss_correct:.4f}, confident wrong: {loss_wrong:.4f}")

# -------------------------------------------- 3. Weight Update with Momentum
velocity = 0.0
beta = 0.9
grad = 2.0
lr = 0.1

velocity = beta * velocity + grad
w_updated = 1.0 - lr * velocity

assert velocity == 2.0
assert abs(w_updated - 0.8) < 1e-6
print(f"Updated weight with momentum: {w_updated}")

print()
print("All checks passed.")
