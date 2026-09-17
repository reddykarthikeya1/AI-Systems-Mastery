# Lesson 10.11 — Random Variables

> **Module 10:** Reasoning Under Uncertainty · Lesson 11 of 41

---

## What you will be able to do after this lesson

- [ ] Define random variable X: Omega -> R as a deterministic function mapping sample space outcomes to real numbers.
- [ ] Compute pre-images X^(-1)(A).

## Prerequisites

- 10.02 Sample Spaces and Events.

---

## 1. The idea

A **random variable** $X$ is neither random nor a variable: it is a deterministic mathematical function $X: \Omega \to \mathbb{R}$ that assigns a numerical value to each outcome in the sample space. $P(X \le x)$ is shorthand for $P(\{\omega \in \Omega : X(\omega) \le x\})$.

---

## 2. Worked example

Flipping 2 coins: $\Omega = \{HH, HT, TH, TT\}$. Let $X$ be the number of heads. $X(HH)=2, X(HT)=1, X(TH)=1, X(TT)=0$. $P(X=1) = 2/4 = 0.5$.

---

## 3. Verify it in code

```python
import numpy as np
omega = ['HH', 'HT', 'TH', 'TT']
X = {'HH': 2, 'HT': 1, 'TH': 1, 'TT': 0}
p_X_1 = sum(1 for w in omega if X[w] == 1) / len(omega)
assert np.isclose(p_X_1, 0.5)
```

---

## 4. The mistake people actually make

Thinking a random variable changes its value unpredictably. The randomness lies in which outcome omega is drawn from Omega.

---

## Check yourself

1. What is a random variable mathematically?
2. What does P(X = k) represent?

<details>
<summary>Answers</summary>

1. A deterministic function from the sample space Omega to the real numbers R.
2. The probability measure of all outcomes omega in Omega where X(omega) = k.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](12_Discrete_Distributions_and_the_PMF.md)
