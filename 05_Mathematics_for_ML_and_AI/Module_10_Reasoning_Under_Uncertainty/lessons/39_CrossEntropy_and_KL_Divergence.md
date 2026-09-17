# Lesson 10.39 — Cross-Entropy and KL Divergence

> **Module 10:** Reasoning Under Uncertainty · Lesson 39 of 41

---

## What you will be able to do after this lesson

- [ ] Compute KL Divergence D_KL(P || Q) = sum p(x) log(p(x) / q(x)) >= 0.
- [ ] Prove Cross-Entropy H(P, Q) = H(P) + D_KL(P || Q).

## Prerequisites

- 10.38 Entropy.

---

## 1. The idea

**Kullback-Leibler (KL) Divergence** $D_{KL}(P \parallel Q) = \sum p(x) \log \frac{p(x)}{q(x)}$ measures the relative entropy / information lost when approximating true distribution $P$ with model $Q$. By Gibbs' inequality, $D_{KL}(P \parallel Q) \ge 0$, with equality iff $P = Q$.
**Cross-Entropy**:
$$H(P, Q) = -\sum p(x) \log q(x) = H(P) + D_{KL}(P \parallel Q)$$

---

## 2. Worked example

When $Q = P$, $D_{KL} = 0$, and cross-entropy equals the true entropy $H(P)$. When $Q$ diverges from $P$, cross-entropy increases strictly.

---

## 3. Verify it in code

```python
import numpy as np
P = np.array([0.7, 0.3])
Q = np.array([0.5, 0.5])

kl = np.sum(P * np.log(P / Q))
cross_entropy = -np.sum(P * np.log(Q))
entropy_p = -np.sum(P * np.log(P))

assert kl >= 0.0
assert np.isclose(cross_entropy, entropy_p + kl)
```

---

## 4. The mistake people actually make

Treating KL divergence as a symmetric distance metric. D_KL(P || Q) != D_KL(Q || P)!

---

## Check yourself

1. Is KL divergence symmetric: D_KL(P || Q) == D_KL(Q || P)?
2. What is the minimum possible value of KL divergence?

<details>
<summary>Answers</summary>

1. No, it is an asymmetric divergence.
2. Zero (attained if and only if P = Q).

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](40_Why_CrossEntropy_Is_the_Classification_Loss.md)
