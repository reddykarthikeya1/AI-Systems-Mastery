# 🐣 Interactive Foundations Playground: Orthogonality and Projections

> *"Projection is dropping a perpendicular shadow onto a subspace: the shortest distance to approximation."*

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

## 1. Orthogonal Vector Zero Dot Product

Two non-zero vectors are perpendicular if and only if their inner product is identically zero.

```python
u = [1.0, 2.0, 3.0]
v = [2.0, -1.0, 0.0]

dot_prod = sum(a * b for a, b in zip(u, v))
assert dot_prod == 0.0, "1*2 + 2*(-1) + 3*0 = 0"
print(f"Vectors u and v are orthogonal: dot product = {dot_prod}")
```

---

## 2. Vector Projection onto a Line

The projection of vector $y$ onto vector $x$ is $\text{proj}_x(y) = \frac{y \cdot x}{x \cdot x} x$.

```python
x = [1.0, 0.0]
y = [3.0, 4.0]

scalar_comp = sum(a * b for a, b in zip(y, x)) / sum(a * a for a in x)
proj = [scalar_comp * a for a in x]

assert proj == [3.0, 0.0]
residual = [y[i] - proj[i] for i in range(2)]
assert residual == [0.0, 4.0]
assert sum(a * b for a, b in zip(proj, residual)) == 0.0, "Projection and residual must be orthogonal"
print(f"Projection of (3, 4) onto x-axis: {proj}, residual shadow: {residual}")
```

---

## 3. Pythagorean Theorem for Orthogonal Decompositions

For any projection, $\|y\|^2 = \|\text{proj}(y)\|^2 + \|y - \text{proj}(y)\|^2$.

```python
norm_y_sq = sum(a**2 for a in y)
norm_proj_sq = sum(a**2 for a in proj)
norm_res_sq = sum(a**2 for a in residual)

assert abs(norm_y_sq - (norm_proj_sq + norm_res_sq)) < 1e-6
assert norm_y_sq == 25.0  # 3^2 + 4^2 = 25
print(f"Pythagorean theorem satisfied: {norm_y_sq} == {norm_proj_sq} + {norm_res_sq}")
```

---
