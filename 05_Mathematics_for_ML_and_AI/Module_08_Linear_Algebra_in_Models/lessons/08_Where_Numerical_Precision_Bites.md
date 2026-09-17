# Lesson 08.08 — Where Numerical Precision Bites

> **Module 08:** Linear Algebra in Models · Lesson 8 of 9

---

## What you will be able to do after this lesson

- [ ] Identify catastrophic cancellation, underflow, and overflow in floating point linear algebra.
- [ ] Implement numerically stable log-sum-exp and numerically safe vector normalization.

## Prerequisites

- Linear algebra operations and floating point representation.

---

## 1. The idea

In floating point arithmetic, computing softmax directly overflows when logits are large.
The **Log-Sum-Exp trick** stabilizes this by shifting logits by their maximum:
$$\log \sum_{i=1}^n e^{x_i} = c + \log \sum_{i=1}^n e^{x_i - c}, \quad \text{where } c = \max_j x_j$$

---

## 2. Worked example

Let logits x = [1000.0, 1001.0, 999.0].
Directly computing e^1000 overflows to inf in float32.
Shifting by c = 1001.0 gives [-1.0, 0.0, -2.0].
Exponentials are [0.3679, 1.0, 0.1353], sum = 1.5032.
The softmax probabilities are safely computed as [0.2447, 0.6652, 0.0900].

---

## 3. Verify it in code

```python
import numpy as np

logits = np.array([1000.0, 1001.0, 999.0])
c = np.max(logits)
shifted_exp = np.exp(logits - c)
stable_softmax = shifted_exp / np.sum(shifted_exp)

assert not np.isnan(stable_softmax).any()
assert np.isclose(np.sum(stable_softmax), 1.0)
assert np.allclose(stable_softmax, [0.24472847, 0.66524096, 0.09003057], atol=1e-5)
```

---

## 4. The mistake people actually make

**Evaluating cross-entropy loss by computing log(softmax(x)) in two separate calls.**

Small probabilities underflow to 0.0, and log(0.0) produces -inf, generating NaN gradients.

---

## Check yourself

1. Why does subtracting max(x) from all elements not alter the softmax probability distribution?
2. What happens when dividing by norm(x) when x is the zero vector?

<details>
<summary>Answers</summary>

1. Because e^(x_i - c) / sum(e^(x_j - c)) = (e^x_i * e^-c) / (e^-c * sum(e^x_j)) = e^x_i / sum(e^x_j). The e^-c factor cancels exactly.
2. Division by zero occurs, producing NaN or inf. Adding a small epsilon (e.g. 1e-8) prevents numerical instability.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](09_Module_Project_A_Forward_Pass_With_Only_NumPy.md)
