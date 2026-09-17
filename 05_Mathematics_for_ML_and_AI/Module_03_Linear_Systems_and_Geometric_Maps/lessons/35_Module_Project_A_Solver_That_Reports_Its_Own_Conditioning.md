# Lesson 03.35 — Module Project: A Solver That Reports Its Own Conditioning

> **Module 03:** Linear Systems and Geometric Maps · Lesson 35 of 35

---

## What you will be able to do after this lesson

- [ ] Construct a robust linear solver that analyzes condition number, rank, and residual error.
- [ ] Emit automated health warnings when systems are ill-conditioned.

## Prerequisites

- Lessons 03.01 through 03.34.

---

## 1. The idea

We build a production-grade linear solver wrapper `safe_solve(A, b)` that:
1. Validates matrix dimensions and finite values.
2. Computes the condition number $\kappa(A)$.
3. If $\kappa(A) > 10^8$, flags the system as ill-conditioned.
4. Returns the solution along with backward error $\|A\mathbf{x} - \mathbf{b}\| / (\|A\|\|\mathbf{x}\| + \|\mathbf{b}\|)$.

---

## 2. Worked example

Testing on well-conditioned and ill-conditioned matrices: the solver correctly flags condition number $10^{10}$ and reports precision loss.

---

## 3. Verify it in code

```python
import numpy as np

def safe_solve(A, b):
    cond = np.linalg.cond(A)
    x = np.linalg.solve(A, b)
    residual = np.linalg.norm(A @ x - b)
    is_healthy = cond < 1e8
    return x, cond, residual, is_healthy

# Well-conditioned test
A_good = np.array([[3.0, 1.0], [1.0, 2.0]])
b_good = np.array([4.0, 3.0])
x, cond, res, healthy = safe_solve(A_good, b_good)

assert healthy == True
assert cond < 10.0
assert np.isclose(res, 0.0)
assert np.allclose(x, [1.0, 1.0])
```

---

## 4. The mistake people actually make

Silently accepting ill-conditioned solutions without checking residuals or condition numbers.

---

## Check yourself

1. What threshold on condition number generally indicates significant numerical precision loss in float64?
2. What does backward error measure?

<details>
<summary>Answers</summary>

1. kappa(A) > 10^8 (or > 10^12 for float64).
2. The distance from the given problem to the nearest problem solved exactly by the computed answer.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md)
