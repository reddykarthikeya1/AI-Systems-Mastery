# 🐣 Interactive Foundations Playground: Linear Systems and Geometric Maps

> *"A matrix is a geometric transformation that stretches, rotates, and shears coordinate space."*

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

## 1. Vector Addition and Scalar Scaling

Vectors represent directed arrows in space; scalar multiplication stretches their magnitude while preserving orientation.

```python
v1 = [2.0, 3.0]
v2 = [4.0, -1.0]

v_sum = [a + b for a, b in zip(v1, v2)]
scaled = [2.5 * x for x in v1]

assert v_sum == [6.0, 2.0]
assert scaled == [5.0, 7.5]
print(f"v1 + v2 = {v_sum}, 2.5 * v1 = {scaled}")
```

---

## 2. Matrix-Vector Multiplication as Linear Map

Multiplying a $2 \times 2$ matrix by a $2 \times 1$ vector maps the point to new coordinates through dot products of rows with the input vector.

```python
A = [[2.0, 1.0],
     [0.0, 3.0]]
x = [3.0, 2.0]

Ax = [sum(row[i] * x[i] for i in range(len(x))) for row in A]

assert Ax == [8.0, 6.0], "Row 0: 2*3+1*2=8; Row 1: 0*3+3*2=6"
assert len(Ax) == 2
print(f"Matrix A applied to vector x yields: {Ax}")
```

---

## 3. 2D Rotation Matrix Invariant

A rotation matrix $R(\theta)$ rotates a vector counter-clockwise by $\theta$ while strictly preserving its Euclidean length (norm).

```python
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
```

---
