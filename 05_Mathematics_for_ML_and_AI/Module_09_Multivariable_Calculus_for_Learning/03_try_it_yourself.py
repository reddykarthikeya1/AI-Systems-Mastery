"""Beginner playground for Module 09 - Multivariable Calculus for Learning.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

import math

# -------------------------------------------- 1. Numerical Finite Difference Gradient Estimation
def f(x, y):
    return x**2 + 3 * y**2

h = 1e-5
x0, y0 = 2.0, 1.0
df_dx = (f(x0 + h, y0) - f(x0 - h, y0)) / (2 * h)
df_dy = (f(x0, y0 + h) - f(x0, y0 - h)) / (2 * h)

assert abs(df_dx - 4.0) < 1e-4, "Analytical df/dx = 2x = 4"
assert abs(df_dy - 6.0) < 1e-4, "Analytical df/dy = 6y = 6"
print(f"Numerical gradient at (2, 1): [{df_dx:.3f}, {df_dy:.3f}]")

# -------------------------------------------- 2. Gradient Descent Step Decreases Loss
lr = 0.1
x_new = x0 - lr * df_dx
y_new = y0 - lr * df_dy

loss_before = f(x0, y0)
loss_after = f(x_new, y_new)

assert loss_after < loss_before, "Gradient descent step must decrease loss"
assert loss_before == 7.0
assert abs(loss_after - (1.6**2 + 3 * 0.4**2)) < 1e-4
print(f"Loss dropped from {loss_before} to {loss_after:.4f}")

# -------------------------------------------- 3. Univariate Chain Rule Verification
# y = (2x + 3)^2
def g(x): return 2 * x + 3
def f_sq(u): return u**2

x_val = 1.0
u_val = g(x_val)  # 5
df_du = 2 * u_val  # 10
dg_dx = 2          # 2
chain_deriv = df_du * dg_dx

assert chain_deriv == 20.0
assert abs(chain_deriv - 20.0) < 1e-6
print(f"Chain rule derivative of (2x + 3)^2 at x=1: {chain_deriv}")

print()
print("All checks passed.")
