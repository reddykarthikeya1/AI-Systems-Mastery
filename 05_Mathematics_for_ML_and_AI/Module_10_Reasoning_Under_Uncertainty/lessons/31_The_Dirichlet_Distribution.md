# Lesson 10.31 — The Dirichlet Distribution

> **Module 10:** Reasoning Under Uncertainty · Lesson 31 of 41

---

## What you will be able to do after this lesson

- [ ] Define Dirichlet(alpha) over probability simplex sum p_i = 1.
- [ ] Recognize Dirichlet as the conjugate prior for Categorical/Multinomial distributions (LDA).

## Prerequisites

- 10.28 Beta Distribution and 10.30 Categorical Distribution.

---

## 1. The idea

The **Dirichlet distribution** is the multivariate generalization of the Beta distribution, defining probability density over the probability simplex $\Delta^{K-1} = \{\mathbf{p} : p_i \ge 0, \sum p_i = 1\}$. It is the conjugate prior for Categorical and Multinomial distributions, forming the foundation of Latent Dirichlet Allocation (LDA).

---

## 2. Worked example

For $K=3$, $\boldsymbol{\alpha} = [1, 1, 1]$ is the uniform distribution over the 2D triangular simplex.

---

## 3. Verify it in code

```python
import numpy as np
alpha = np.array([1.0, 1.0, 1.0])
# Expected probability vector
expected_p = alpha / np.sum(alpha)
assert np.allclose(expected_p, [1.0/3.0, 1.0/3.0, 1.0/3.0])
```

---

## 4. The mistake people actually make

Generating Dirichlet samples without normalizing Gamma samples.

---

## Check yourself

1. What is the support space of a K-dimensional Dirichlet distribution?
2. What does Dirichlet(1, 1, ..., 1) represent?

<details>
<summary>Answers</summary>

1. The probability simplex Delta^(K-1) where entries sum to 1.
2. A uniform distribution over the probability simplex.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](32_Transformations_of_Random_Variables.md)
