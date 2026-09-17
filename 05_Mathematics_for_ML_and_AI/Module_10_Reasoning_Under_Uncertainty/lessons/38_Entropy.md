# Lesson 10.38 — Entropy

> **Module 10:** Reasoning Under Uncertainty · Lesson 38 of 41

---

## What you will be able to do after this lesson

- [ ] Compute Shannon Entropy H(X) = -sum p(x) log2 p(x).
- [ ] Interpret entropy as average information content / uncertainty in bits.

## Prerequisites

- 10.12 Discrete PMF.

---

## 1. The idea

**Shannon Entropy** $H(X) = -\sum_{i=1}^n p(x_i) \log_2 p(x_i)$ measures the expected information content (uncertainty) of a random variable. A deterministic event has $H = 0$ (no surprise). A uniform distribution over $n$ outcomes achieves maximum entropy $H = \log_2 n$.

---

## 2. Worked example

Fair coin: $H = -2 \times (0.5 \log_2 0.5) = -2(0.5)(-1) = 1.0 \text{ bit}$. Biased coin with $p=1.0$: $H = -(1 \log_2 1 + 0 \log_2 0) = 0 \text{ bits}$.

---

## 3. Verify it in code

```python
import numpy as np
p_fair = np.array([0.5, 0.5])
h_fair = -np.sum(p_fair * np.log2(p_fair))
assert np.isclose(h_fair, 1.0)

p_deterministic = np.array([1.0, 0.0])
# Convention 0 log 0 = 0
h_det = -np.sum([p * np.log2(p) for p in p_deterministic if p > 0])
assert np.isclose(h_det, 0.0)
```

---

## 4. The mistake people actually make

Evaluating 0 * log(0) as NaN or error in code without masking zero-probability states (lim_{p->0} p log p = 0).

---

## Check yourself

1. What is the entropy of a completely deterministic variable?
2. What base of logarithm measures entropy in bits?

<details>
<summary>Answers</summary>

1. Zero bits.
2. Base 2.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](39_CrossEntropy_and_KL_Divergence.md)
