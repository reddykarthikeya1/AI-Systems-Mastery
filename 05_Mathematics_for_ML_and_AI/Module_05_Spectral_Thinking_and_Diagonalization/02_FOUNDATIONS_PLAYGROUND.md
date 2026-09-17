# 🐣 Interactive Foundations Playground: Spectral Thinking and Diagonalization

> *"Eigenvectors are special directions where a matrix acts merely as a scalar scaling factor."*

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

## 1. The Eigenvalue Equation A*v = lambda*v

When a matrix multiplies an eigenvector, the output vector points along the exact same line, scaled by the eigenvalue $\lambda$.

```python
A = [[2.0, 0.0],
     [0.0, 5.0]]
v1 = [1.0, 0.0]  # Eigenvector corresponding to lambda=2
v2 = [0.0, 1.0]  # Eigenvector corresponding to lambda=5

def mat_vec(M, v):
    return [sum(M[r][c] * v[c] for c in range(len(v))) for r in range(len(M))]

Av1 = mat_vec(A, v1)
Av2 = mat_vec(A, v2)

assert Av1 == [2.0 * x for x in v1]
assert Av2 == [5.0 * x for x in v2]
print(f"Av1 = {Av1} (2*v1), Av2 = {Av2} (5*v2)")
```

---

## 2. Matrix Trace and Determinant Spectral Properties

The trace of a matrix strictly equals the sum of its eigenvalues, and the determinant equals the product of its eigenvalues.

```python
trace = A[0][0] + A[1][1]
det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
eig1, eig2 = 2.0, 5.0

assert trace == eig1 + eig2, "Trace must equal sum of eigenvalues"
assert det == eig1 * eig2, "Determinant must equal product of eigenvalues"
print(f"Trace: {trace} (2+5), Det: {det} (2*5)")
```

---

## 3. Matrix Power Acceleration via Diagonalization

Raising a diagonal matrix to power $k$ requires only exponentiating its diagonal elements: $D^k = \text{diag}(\lambda_1^k, \dots)$.

```python
k = 3
A_cubed = [[A[0][0]**k, 0.0],
           [0.0, A[1][1]**k]]

assert A_cubed[0][0] == 8.0, "2^3 = 8"
assert A_cubed[1][1] == 125.0, "5^3 = 125"
print(f"A^3 computed via spectral powers: {A_cubed}")
```

---
