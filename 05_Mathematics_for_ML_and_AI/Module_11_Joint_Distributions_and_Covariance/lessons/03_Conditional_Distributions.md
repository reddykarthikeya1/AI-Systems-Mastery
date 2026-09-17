# Lesson 11.03 — Conditional Distributions

> **Module 11:** Joint Distributions and Covariance · Lesson 3 of 29

---

## What you will be able to do after this lesson

- [ ] Compute conditional probability P(Y=y | X=x) = P(x, y) / P(x).
- [ ] Normalize rows of joint probability matrices into conditional stochastic matrices.

## Prerequisites

- 11.02 Marginal Distributions.

---

## 1. The idea

The **conditional distribution** $P(Y = y \mid X = x) = \frac{P(X = x, Y = y)}{P(X = x)}$ slices the joint distribution along the condition $X = x$ and renormalizes so the sum equals 1.

---

## 2. Worked example

Given $P(X=0, Y=1) = 0.2$ and $P(X=0) = 0.6$: $P(Y=1 \mid X=0) = 0.2 / 0.6 = 1/3 \approx 0.333$.

---

## 3. Verify it in code

```python
import numpy as np
joint = np.array([[0.4, 0.2], [0.1, 0.3]])
p_x = np.sum(joint, axis=1, keepdims=True)
cond_y_given_x = joint / p_x

assert np.isclose(cond_y_given_x[0, 1], 0.2 / 0.6)
assert np.allclose(np.sum(cond_y_given_x, axis=1), [1.0, 1.0])
```

---

## 4. The mistake people actually make

Dividing by the joint probability instead of the marginal conditioning probability.

---

## Check yourself

1. What must sum_y P(Y=y | X=x) equal for any fixed x?
2. When is P(Y | X) undefined?

<details>
<summary>Answers</summary>

1. Exactly 1.0.
2. When P(X=x) = 0 (division by zero).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](04_Independence_in_Terms_of_Joints.md)
