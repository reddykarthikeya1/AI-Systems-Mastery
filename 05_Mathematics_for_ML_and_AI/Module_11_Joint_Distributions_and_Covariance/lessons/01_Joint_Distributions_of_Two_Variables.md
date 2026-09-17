# Lesson 11.01 — Joint Distributions of Two Variables

> **Module 11:** Joint Distributions and Covariance · Lesson 1 of 29

---

## What you will be able to do after this lesson

- [ ] Represent joint probability tables P(X = x, Y = y).
- [ ] Verify total probability normalization sum_{x, y} P(x, y) = 1 in NumPy.

## Prerequisites

- Discrete probability (Module 10).

---

## 1. The idea

The **joint distribution** $P(X = x, Y = y)$ assigns probabilities to simultaneous outcomes of two random variables. It captures both individual behavior and the dependencies between them. Normalization requires $\sum_x \sum_y P(X=x, Y=y) = 1$.

---

## 2. Worked example

Let $X, Y \in \{0, 1\}$. Probabilities: $P(0, 0) = 0.4, P(0, 1) = 0.2, P(1, 0) = 0.1, P(1, 1) = 0.3$. Sum is $0.4 + 0.2 + 0.1 + 0.3 = 1.0$.

---

## 3. Verify it in code

```python
import numpy as np
joint = np.array([[0.4, 0.2], [0.1, 0.3]])
assert np.isclose(np.sum(joint), 1.0)
assert np.all(joint >= 0.0)
```

---

## 4. The mistake people actually make

Summing joint probabilities across rows only and forgetting that normalization applies to the entire 2D table.

---

## Check yourself

1. What must the sum of all elements in a joint probability table equal?
2. Can any joint probability entry be negative?

<details>
<summary>Answers</summary>

1. Exactly 1.0.
2. No, probabilities must be non-negative.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](02_Marginal_Distributions.md)
