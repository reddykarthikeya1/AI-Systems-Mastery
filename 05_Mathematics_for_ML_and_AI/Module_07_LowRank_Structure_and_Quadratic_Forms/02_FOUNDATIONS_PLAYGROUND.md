# 🐣 Interactive Foundations Playground: Low-Rank Structure and Quadratic Forms

> *"Low-rank approximation compresses giant matrices into compact factorized representations without losing dominant patterns."*

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

## 1. Outer Product Rank-1 Matrix Construction

Multiplying column vector $u$ by row vector $v^T$ forms a rank-1 matrix where every column is a scalar multiple of $u$.

```python
u = [1.0, 2.0, 3.0]
v = [4.0, 5.0]

M = [[u[i] * v[j] for j in range(len(v))] for i in range(len(u))]
assert len(M) == 3 and len(M[0]) == 2
assert M[0] == [4.0, 5.0]
assert M[1] == [8.0, 10.0]  # Exactly 2 * row 0
print(f"Rank-1 matrix outer product row 0: {M[0]}, row 1: {M[1]}")
```

---

## 2. Evaluating a Quadratic Form x^T A x

A quadratic form $x^T A x = \sum_i \sum_j A_{ij} x_i x_j$ computes an energy or loss curvature scalar.

```python
A = [[2.0, 0.0],
     [0.0, 3.0]]
x = [2.0, 1.0]

val = sum(x[i] * A[i][j] * x[j] for i in range(2) for j in range(2))
assert val == 2.0 * (2.0**2) + 3.0 * (1.0**2)
assert val == 11.0
print(f"Quadratic form value for x=[2, 1]: {val}")
```

---

## 3. Positive Definiteness Verification

A symmetric matrix is positive definite if $x^T A x > 0$ for all non-zero vectors $x$, ensuring convex loss functions with unique minima.

```python
test_vectors = [[1.0, 0.0], [0.0, 1.0], [1.0, 1.0], [-2.0, 3.0]]
is_pd = all(sum(v[i] * A[i][j] * v[j] for i in range(2) for j in range(2)) > 0 for v in test_vectors)
assert is_pd is True
print("Matrix A confirmed positive-definite across test vectors.")
```

---
