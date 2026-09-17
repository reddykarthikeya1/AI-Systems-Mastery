# Lesson 11.02 — Marginal Distributions

> **Module 11:** Joint Distributions and Covariance · Lesson 2 of 29

---

## What you will be able to do after this lesson

- [ ] Compute marginal distributions by summing out nuisance variables: P(X=x) = sum_y P(x, y).
- [ ] Perform axis summation in NumPy.

## Prerequisites

- 11.01 Joint Distributions.

---

## 1. The idea

**Marginalization** collapses a joint distribution onto one variable by summing over all possible states of the other: $P(X = x) = \sum_y P(X = x, Y = y)$. In machine learning, marginalization removes unobserved latent variables.

---

## 2. Worked example

Using the joint table: $P(X=0) = 0.4 + 0.2 = 0.6$. $P(X=1) = 0.1 + 0.3 = 0.4$. Note $0.6 + 0.4 = 1.0$.

---

## 3. Verify it in code

```python
import numpy as np
joint = np.array([[0.4, 0.2], [0.1, 0.3]])
# Marginal of X (sum across columns)
p_x = np.sum(joint, axis=1)
# Marginal of Y (sum across rows)
p_y = np.sum(joint, axis=0)

assert np.allclose(p_x, [0.6, 0.4])
assert np.allclose(p_y, [0.5, 0.5])
assert np.isclose(np.sum(p_x), 1.0)
```

---

## 4. The mistake people actually make

Summing along the wrong NumPy axis (axis=0 vs axis=1) when computing marginals.

---

## Check yourself

1. How is P(X=x) obtained from the joint distribution P(X=x, Y=y)?
2. What is the sum of a marginal distribution?

<details>
<summary>Answers</summary>

1. By summing out y over all its possible values.
2. Exactly 1.0.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](03_Conditional_Distributions.md)
