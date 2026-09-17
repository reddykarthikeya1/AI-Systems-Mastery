# 🐣 Interactive Foundations Playground: Vector Spaces, Bases, and Rank

> *"A basis is the minimal set of reference directions needed to reach any destination in a vector space."*

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

## 1. Dot Product and Vector Length

The dot product measures directional alignment; the dot product of a vector with itself yields the squared Euclidean norm.

```python
def dot(u, v):
    return sum(a * b for a, b in zip(u, v))

def norm(u):
    return math.sqrt(dot(u, u))

a = [3.0, 4.0]
b = [4.0, -3.0]

assert dot(a, b) == 0.0, "Orthogonal vectors have dot product 0"
assert norm(a) == 5.0, "3-4-5 right triangle length"
print(f"Dot product: {dot(a, b)}, Norm of a: {norm(a)}")
```

---

## 2. Linear Independence Check in 2D

Two vectors in 2D are linearly dependent if one is a scalar multiple of another, meaning their determinant (cross-product) is zero.

```python
def is_linearly_independent_2d(u, v):
    det = u[0] * v[1] - u[1] * v[0]
    return abs(det) > 1e-9

v1 = [1.0, 2.0]
v2 = [2.0, 4.0]  # Dependent: 2 * v1
v3 = [0.0, 1.0]  # Independent

assert is_linearly_independent_2d(v1, v2) is False
assert is_linearly_independent_2d(v1, v3) is True
print("Linear independence tests validated in 2D.")
```

---

## 3. Matrix Rank and Column Space Dimension

The rank of a matrix represents the dimension of its column space (number of linearly independent columns).

```python
def rank_2x2(A):
    det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    if abs(det) > 1e-9:
        return 2
    if any(A[r][c] != 0 for r in range(2) for c in range(2)):
        return 1
    return 0

full_rank = [[1, 2], [3, 4]]
rank_1 = [[1, 2], [2, 4]]
assert rank_2x2(full_rank) == 2
assert rank_2x2(rank_1) == 1
print(f"Rank of full-rank matrix: {rank_2x2(full_rank)}, rank of dependent matrix: {rank_2x2(rank_1)}")
```

---
