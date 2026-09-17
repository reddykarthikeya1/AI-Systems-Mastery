# Lesson 12.08 — The Log-Likelihood and Why We Take Logs

> **Module 12:** Statistical Estimation from Samples · Lesson 8 of 22

---

## What you will be able to do after this lesson

- [ ] Convert product of probabilities into sum of log-probabilities.
- [ ] Explain why log-transform eliminates floating-point underflow.

## Prerequisites

- 12.07 Maximum Likelihood Estimation.

---

## 1. The idea

Multiplying $n$ probabilities underflows to 0.0 in floating-point arithmetic for $n > 50$. Because $\log$ is strictly monotonically increasing, $\text{argmax} L(\theta) = \text{argmax} \log L(\theta) = \text{argmax} \sum_{i=1}^n \log f(x_i; \theta)$. Addition replaces multiplication, derivatives decouple, and numerical stability is preserved.

---

## 2. Worked example

Multiplying 100 probabilities of $0.01$ gives $10^{-200}$ (underflows float32). Summing logs gives $100 \times (-4.605) = -460.5$, completely stable.

---

## 3. Verify it in code

```python
import numpy as np
probs = np.full(100, 0.01)
log_lik = np.sum(np.log(probs))
assert np.isclose(log_lik, 100 * np.log(0.01))
assert not np.isnan(log_lik)
```

---

## 4. The mistake people actually make

Maximizing raw likelihood directly in optimizer routines, triggering floating point underflow to zero.

---

## Check yourself

1. Why does maximizing log L(theta) give the exact same result as maximizing L(theta)?
2. What mathematical benefit does taking log provide for i.i.d. data?

<details>
<summary>Answers</summary>

1. Because log is a strictly monotonic increasing function.
2. It converts products into sums, simplifying derivatives and preventing underflow.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](09_MLE_for_the_Normal_and_Bernoulli.md)
