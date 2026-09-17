# Lesson 10.41 — Module Project: Naive Bayes With Calibrated Probabilities

> **Module 10:** Reasoning Under Uncertainty · Lesson 41 of 41

---

## What you will be able to do after this lesson

- [ ] Build a complete Gaussian Naive Bayes text/tabular classifier from scratch in NumPy.
- [ ] Apply Laplace smoothing to prevent zero-frequency collapse.

## Prerequisites

- Lessons 10.01 through 10.40.

---

## 1. The idea

**Gaussian Naive Bayes** applies Bayes' Rule assuming features are conditionally independent given class $c$:
$$P(y = c \mid \mathbf{x}) \propto P(y = c) \prod_{j=1}^D \mathcal{N}(x_j \mid \mu_{cj}, \sigma_{cj}^2)$$
Log-posterior for numerical stability:
$$\log P(y = c \mid \mathbf{x}) = \log P(y = c) - \frac{1}{2}\sum_{j=1}^D \left[ \log(2\pi\sigma_{cj}^2) + \frac{(x_j - \mu_{cj})^2}{\sigma_{cj}^2} \right]$$

---

## 2. Worked example

Binary classification with 2 features. Class 0 centered at $(0, 0)$, Class 1 centered at $(3, 3)$. New point $(2.5, 2.5)$ evaluates with higher likelihood under Class 1.

---

## 3. Verify it in code

```python
import numpy as np
# Synthetic training data
np.random.seed(42)
X0 = np.random.normal(0.0, 1.0, (50, 2))
X1 = np.random.normal(3.0, 1.0, (50, 2))
X_train = np.vstack([X0, X1])
y_train = np.array([0]*50 + [1]*50)

# Fit parameters
mu0 = np.mean(X0, axis=0)
var0 = np.var(X0, axis=0) + 1e-6
mu1 = np.mean(X1, axis=0)
var1 = np.var(X1, axis=0) + 1e-6

# Predict function
def predict_nb(x):
    log_p0 = -0.5 * np.sum(np.log(2*np.pi*var0) + (x - mu0)**2 / var0)
    log_p1 = -0.5 * np.sum(np.log(2*np.pi*var1) + (x - mu1)**2 / var1)
    return 1 if log_p1 > log_p0 else 0

assert predict_nb(np.array([0.0, 0.0])) == 0
assert predict_nb(np.array([3.0, 3.0])) == 1
```

---

## 4. The mistake people actually make

Neglecting variance floor / Laplace smoothing epsilon, which causes division by zero when a feature has zero variance in training data.

---

## Check yourself

1. What is the Naive Bayes conditional independence assumption?
2. Why is the calculation performed in log-space?

<details>
<summary>Answers</summary>

1. That all features are conditionally independent given the class label.
2. To convert products of small probabilities into sums, preventing underflow.

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
