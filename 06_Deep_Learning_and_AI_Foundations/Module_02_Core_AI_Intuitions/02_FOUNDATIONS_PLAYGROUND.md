# 🐣 Interactive Foundations Playground: Core AI Intuitions & Gradient Descent

> *"Gradient descent is hiking down a foggy mountain by following the steepest slope under your boots."*

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

## 1. 1D Gradient Descent Iteration

Iteratively subtracting the learning rate times derivative of the loss function drives the parameter toward the local minimum.

```python
# Minimize L(w) = (w - 4)^2; derivative is 2*(w - 4)
w = 0.0
lr = 0.2
for _ in range(10):
    grad = 2.0 * (w - 4.0)
    w -= lr * grad

assert abs(w - 4.0) < 0.1, "Weight must converge near 4.0"
print(f"Converged weight after 10 steps: {w:.4f} (target: 4.0)")
```

---

## 2. Learning Rate Stability Bounds

If learning rate is too large ($\eta > 2/L$), gradient descent overshoots and diverges to infinity.

```python
w_divergent = 0.0
bad_lr = 1.1  # For loss with curvature 2, lr > 1.0 diverges
for _ in range(3):
    grad = 2.0 * (w_divergent - 4.0)
    w_divergent -= bad_lr * grad

assert abs(w_divergent - 4.0) > 4.0, "Divergence creates expanding oscillations"
print(f"Divergent weight after unstable learning rate: {w_divergent:.2f}")
```

---

## 3. Loss Function Monotonic Reduction

With an appropriate step size, every gradient step monotonically decreases the objective value.

```python
def loss(val): return (val - 4.0)**2
w_step = 0.0
l1 = loss(w_step)
w_step -= 0.1 * 2.0 * (w_step - 4.0)
l2 = loss(w_step)
assert l2 < l1
assert l1 == 16.0
print(f"Loss decreased from {l1} to {l2}")
```

---
