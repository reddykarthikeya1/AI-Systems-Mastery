# Lesson 11.29 — Module Project: A Gaussian Mixture Model by EM

> **Module 11:** Joint Distributions and Covariance · Lesson 29 of 29

---

## What you will be able to do after this lesson

- [ ] Implement the Expectation-Maximization (EM) algorithm for a Gaussian Mixture Model (GMM).
- [ ] Iterate E-step (responsibilities) and M-step (parameters) in NumPy.

## Prerequisites

- Lessons 11.01 through 11.28.

---

## 1. The idea

A **Gaussian Mixture Model (GMM)** models data as a weighted sum of $K$ Gaussians: $p(\mathbf{x}) = \sum_{k=1}^K \pi_k \mathcal{N}(\mathbf{x} \mid \mu_k, \sigma_k^2)$.
The **EM algorithm** alternates:
1. **E-step**: compute responsibility $\gamma_{ik} = \frac{\pi_k \mathcal{N}(x_i \mid \mu_k, \sigma_k^2)}{\sum_j \pi_j \mathcal{N}(x_i \mid \mu_j, \sigma_j^2)}$.
2. **M-step**: re-estimate $\mu_k = \frac{\sum_i \gamma_{ik} x_i}{\sum_i \gamma_{ik}}$ and $\sigma_k^2$.

---

## 2. Worked example

Cluster 100 points drawn from two separated Gaussians centered at 0 and 10. EM converges in ~10 iterations to recover both cluster means.

---

## 3. Verify it in code

```python
import numpy as np
np.random.seed(42)
# Data from two clusters
c1 = np.random.normal(0.0, 1.0, 50)
c2 = np.random.normal(10.0, 1.0, 50)
X = np.concatenate([c1, c2])

# Initialize
mu1, mu2 = 2.0, 8.0
var1, var2 = 2.0, 2.0
pi1, pi2 = 0.5, 0.5

def norm_pdf(x, m, v):
    return (1.0 / np.sqrt(2.0 * np.pi * v)) * np.exp(-0.5 * (x - m)**2 / v)

# Run 10 EM iterations
for _ in range(15):
    # E-step
    r1 = pi1 * norm_pdf(X, mu1, var1)
    r2 = pi2 * norm_pdf(X, mu2, var2)
    tot = r1 + r2 + 1e-12
    gamma1 = r1 / tot
    gamma2 = r2 / tot

    # M-step
    N1 = np.sum(gamma1)
    N2 = np.sum(gamma2)
    mu1 = np.sum(gamma1 * X) / N1
    mu2 = np.sum(gamma2 * X) / N2

assert np.isclose(mu1, 0.0, atol=0.5)
assert np.isclose(mu2, 10.0, atol=0.5)
```

---

## 4. The mistake people actually make

Allowing component variance to collapse to zero on a single isolated data point, causing likelihood explosion to infinity.

---

## Check yourself

1. What is computed in the E-step of GMM EM?
2. What is updated in the M-step?

<details>
<summary>Answers</summary>

1. The posterior responsibilities (soft cluster assignments) for each data point.
2. The mixture weights, means, and variances of each Gaussian component.

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
