# Lesson 11.03 — Conditional Expectation

> **Module 11:** Joint Distributions and Covariance · Lesson 13 of 29

---

## What you will be able to do after this lesson

- [ ] Define conditional expectation E[Y | X=x] = sum y P(y | x).
- [ ] Recognize E[Y | X] as the minimum mean squared error (MMSE) regression function.

## Prerequisites

- 11.03 Conditional Distributions.

---

## 1. The idea

The **conditional expectation** $\mathbb{E}[Y \mid X = x] = \int y f_{Y|X}(y \mid x) dy$ is a function of $x$, denoted $g(X) = \mathbb{E}[Y \mid X]$. A foundational theorem of statistical learning proves that $\mathbb{E}[Y \mid X]$ is the unique function $f(X)$ that minimizes expected squared prediction error $\mathbb{E}[(Y - f(X))^2]$.

---

## 2. Worked example

If $Y = 3X + \epsilon$ where $\mathbb{E}[\epsilon \mid X] = 0$, then $\mathbb{E}[Y \mid X = 2] = 3(2) + 0 = 6$.

---

## 3. Verify it in code

```python
import numpy as np
np.random.seed(42)
x = np.random.uniform(0, 10, 10000)
noise = np.random.normal(0, 1, 10000)
y = 3.0 * x + noise

# Conditional expectation around x = 2
mask = np.abs(x - 2.0) < 0.2
e_y_given_x2 = np.mean(y[mask])
assert np.isclose(e_y_given_x2, 6.0, atol=0.1)
```

---

## 4. The mistake people actually make

Treating E[Y | X] as a single number. E[Y | X = x] is a number, but E[Y | X] is a random variable that depends on X.

---

## Check yourself

1. What predictor minimizes mean squared error E[(Y - f(X))^2]?
2. Is E[Y | X] a constant or a random variable?

<details>
<summary>Answers</summary>

1. The conditional expectation E[Y | X].
2. It is a random variable (a function of the random variable X).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](14_The_Tower_Property.md)
