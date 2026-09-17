# Lesson 10.30 — The Categorical and Multinomial Distributions

> **Module 10:** Reasoning Under Uncertainty · Lesson 30 of 41

---

## What you will be able to do after this lesson

- [ ] Define Categorical(p) as multi-class generalization of Bernoulli.
- [ ] Define Multinomial(n, p) as sum of n Categorical trials.

## Prerequisites

- 10.19 Bernoulli and Binomial.

---

## 1. The idea

- **Categorical** ($K$ classes): single trial where outcome is one of $K$ categories with probabilities $\mathbf{p} = [p_1, \dots, p_K]^T$ ($\sum p_i = 1$). (Softmax layer output).
- **Multinomial($n, \mathbf{p}$)**: count vector $\mathbf{x} = [x_1, \dots, x_K]^T$ across $n$ independent trials: $P(\mathbf{x}) = \frac{n!}{\prod x_k!} \prod p_k^{x_k}$.

---

## 2. Worked example

Rolling die 6 times ($n=6, p_i = 1/6$): probability of rolling exactly one of each face is $\frac{6!}{1! \dots 1!} (1/6)^6 = 720 / 46656 \approx 0.0154$.

---

## 3. Verify it in code

```python
import numpy as np
from math import factorial
prob_each_face = factorial(6) * ((1.0 / 6.0)**6)
assert np.isclose(prob_each_face, 720.0 / 46656.0)
```

---

## 4. The mistake people actually make

Calling multi-class classification 'multinomial classification' when each example has only 1 label (it is Categorical classification).

---

## Check yourself

1. What is the relationship between Categorical and Multinomial distributions?
2. What layer in a neural network outputs Categorical parameters?

<details>
<summary>Answers</summary>

1. A Categorical distribution is a Multinomial distribution with n = 1 trial.
2. The Softmax output layer.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](31_The_Dirichlet_Distribution.md)
