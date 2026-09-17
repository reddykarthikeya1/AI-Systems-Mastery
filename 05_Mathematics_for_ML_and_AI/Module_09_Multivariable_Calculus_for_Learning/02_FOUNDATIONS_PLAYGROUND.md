# 🐣 Interactive Foundations Playground: Multivariable Calculus for Learning

> *"Gradients are compass needles pointing directly uphill on the error landscape."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 03_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python
import math
```

---

## 1. Numerical Finite Difference Gradient Estimation

Estimating partial derivatives using symmetric differences: $\frac{\partial f}{\partial x} \approx \frac{f(x + h) - f(x - h)}{2h}$.

```python
def f(x, y):
    return x**2 + 3 * y**2

h = 1e-5
x0, y0 = 2.0, 1.0
df_dx = (f(x0 + h, y0) - f(x0 - h, y0)) / (2 * h)
df_dy = (f(x0, y0 + h) - f(x0, y0 - h)) / (2 * h)

assert abs(df_dx - 4.0) < 1e-4, "Analytical df/dx = 2x = 4"
assert abs(df_dy - 6.0) < 1e-4, "Analytical df/dy = 6y = 6"
print(f"Numerical gradient at (2, 1): [{df_dx:.3f}, {df_dy:.3f}]")
```

---

## 2. Gradient Descent Step Decreases Loss

Stepping in the direction of the negative gradient $-\eta \nabla f$ is guaranteed to reduce the loss for sufficiently small learning rate $\eta$.

```python
lr = 0.1
x_new = x0 - lr * df_dx
y_new = y0 - lr * df_dy

loss_before = f(x0, y0)
loss_after = f(x_new, y_new)

assert loss_after < loss_before, "Gradient descent step must decrease loss"
assert loss_before == 7.0
assert abs(loss_after - (1.6**2 + 3 * 0.4**2)) < 1e-4
print(f"Loss dropped from {loss_before} to {loss_after:.4f}")
```

---

## 3. Univariate Chain Rule Verification

The derivative of composed functions $f(g(x))$ is $f'(g(x)) \cdot g'(x)$.

```python
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
```

---
