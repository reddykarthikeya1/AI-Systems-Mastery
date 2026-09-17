"""Beginner playground for Module 01 - Math Fundamentals for Deep Learning.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Vector Dot Product in Neurons
inputs = [0.5, 0.8, -0.2]
weights = [0.4, 0.7, 0.9]
bias = 0.1

activation = sum(x * w for x, w in zip(inputs, weights)) + bias
assert abs(activation - (0.2 + 0.56 - 0.18 + 0.1)) < 1e-6
assert activation > 0
print(f"Neuron pre-activation: {activation:.4f}")

# -------------------------------------------- 2. Sigmoid and ReLU Activation Functions
def relu(x): return max(0.0, x)
def sigmoid(x): return 1.0 / (1.0 + math.exp(-x))

assert relu(3.5) == 3.5
assert relu(-2.0) == 0.0
assert abs(sigmoid(0.0) - 0.5) < 1e-6
print(f"ReLU(3.5)={relu(3.5)}, ReLU(-2.0)={relu(-2.0)}, Sigmoid(0)={sigmoid(0.0)}")

# -------------------------------------------- 3. Mean Squared Error (MSE) Loss
y_true = [1.0, 2.0, 3.0]
y_pred = [1.2, 1.8, 3.1]

mse = sum((yt - yp)**2 for yt, yp in zip(y_true, y_pred)) / len(y_true)
assert abs(mse - (0.04 + 0.04 + 0.01) / 3) < 1e-6
assert mse > 0
print(f"Mean Squared Error loss: {mse:.4f}")

print()
print("All checks passed.")
