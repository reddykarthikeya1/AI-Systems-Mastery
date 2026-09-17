# 🐣 Interactive Foundations Playground: PyTorch Fundamentals & Computational Graphs

> *"A computational graph is a recipe: each operation remembers its ingredients to compute the backward chain."*

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

## 1. Forward Graph Evaluation

Tracking intermediate node activations allows automatic differentiation engines to compute gradients by unrolling the chain rule.

```python
# Graph: z = (x + y) * w
x, y, w = 2.0, 3.0, 4.0
u = x + y   # Node 1: 5.0
z = u * w   # Node 2: 20.0

assert u == 5.0
assert z == 20.0
print(f"Forward graph evaluated: z={z}")
```

---

## 2. Manual Backpropagation (Autograd Simulation)

Reverse-mode autodiff walks backwards from output $z$, multiplying incoming adjoints by local Jacobian gradients.

```python
dz_dz = 1.0
dz_dw = u * dz_dz       # 5.0
dz_du = w * dz_dz       # 4.0
dz_dx = 1.0 * dz_du     # 4.0
dz_dy = 1.0 * dz_du     # 4.0

assert dz_dw == 5.0
assert dz_dx == 4.0
assert dz_dy == 4.0
print(f"Gradients computed: dz/dw={dz_dw}, dz/dx={dz_dx}, dz/dy={dz_dy}")
```

---

## 3. Accumulation of Gradients Invariant

When a node fans out to multiple downstream branches, its incoming gradients sum linearly (multivariable chain rule).

```python
# x used in two branches: z = 2*x + 3*x
grad_branch1 = 2.0
grad_branch2 = 3.0
total_dx = grad_branch1 + grad_branch2

assert total_dx == 5.0
assert total_dx == 2.0 + 3.0
print(f"Accumulated gradient across multiple paths: {total_dx}")
```

---
