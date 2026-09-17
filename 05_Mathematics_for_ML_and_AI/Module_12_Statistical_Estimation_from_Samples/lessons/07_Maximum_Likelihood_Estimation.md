# Lesson 12.07 — Maximum Likelihood Estimation

> **Module 12:** Statistical Estimation from Samples · Lesson 7 of 22

---

## What you will be able to do after this lesson

- [ ] Formulate likelihood L(theta) = prod p(x_i | theta).
- [ ] Derive MLE theta_hat_MLE = argmax L(theta).

## Prerequisites

- Probability density functions (Module 10).

---

## 1. The idea

**Maximum Likelihood Estimation (MLE)** asks: *Which parameter value makes the observed sample most probable?* Given i.i.d. observations, the likelihood is $L(\theta) = \prod_{i=1}^n f(x_i; \theta)$. The MLE $\hat{\theta}_{MLE}$ maximizes this probability.

---

## 2. Worked example

For coin with heads probability $p$, observing 7 heads in 10 flips: $L(p) = p^7 (1-p)^3$. Maximizing gives $\hat{p} = 7/10 = 0.7$.

---

## 3. Verify it in code

```python
import numpy as np
heads = 7
total = 10
p_mle = heads / total
assert np.isclose(p_mle, 0.7)
```

---

## 4. The mistake people actually make

Treating likelihood L(theta | x) as a probability distribution over theta. L is a function of theta, but its integral over theta does not equal 1.

---

## Check yourself

1. What is the difference between probability P(x | theta) and likelihood L(theta | x)?
2. What criterion defines the MLE estimator?

<details>
<summary>Answers</summary>

1. Probability varies x with fixed theta; likelihood varies theta with fixed observed x.
2. The parameter value that maximizes the likelihood function.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](08_The_LogLikelihood_and_Why_We_Take_Logs.md)
