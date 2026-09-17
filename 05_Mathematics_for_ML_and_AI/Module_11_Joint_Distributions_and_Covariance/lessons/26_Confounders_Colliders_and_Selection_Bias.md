# Lesson 11.26 — Confounders, Colliders and Selection Bias

> **Module 11:** Joint Distributions and Covariance · Lesson 26 of 29

---

## What you will be able to do after this lesson

- [ ] Distinguish Confounders (forks X <- Z -> Y) from Colliders (inverted forks X -> Z <- Y).
- [ ] Explain why conditioning on a collider induces spurious negative correlation (Berkson's bias).

## Prerequisites

- 11.08 Correlation Is Not Causation.

---

## 1. The idea

In Judea Pearl's causal calculus:
- **Confounder** $X \leftarrow Z \to Y$: conditioning on $Z$ **eliminates** bias.
- **Collider** $X \to Z \leftarrow Y$: $X$ and $Y$ are independent, but conditioning on $Z$ **creates spurious correlation** (collider bias / Berkson's paradox)!

---

## 2. Worked example

Let Talent ($X$) and Beauty ($Y$) be independent in the general population. Hollywood fame ($Z$) requires high talent OR high beauty ($Z = X + Y > c$). Among famous actors ($Z=1$), talent and beauty are negatively correlated!

---

## 3. Verify it in code

```python
import numpy as np
np.random.seed(42)
N = 10000
talent = np.random.normal(0, 1, N)
beauty = np.random.normal(0, 1, N)

# Independent initially
assert abs(np.corrcoef(talent, beauty)[0, 1]) < 0.05

# Collider: conditioning on being selected (top 10% of talent + beauty)
selected = (talent + beauty) > 2.0
corr_selected = np.corrcoef(talent[selected], beauty[selected])[0, 1]

# Negative spurious correlation created by conditioning on collider!
assert corr_selected < -0.4
```

---

## 4. The mistake people actually make

Controlling for every available variable in regression models without checking if any are colliders or post-treatment variables.

---

## Check yourself

1. What happens when you condition on a collider Z where X -> Z <- Y?
2. Should you control for a confounder Z where X <- Z -> Y?

<details>
<summary>Answers</summary>

1. It creates a spurious correlation between previously independent variables X and Y.
2. Yes, conditioning on confounders removes confounding bias.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](27_Markov_Chains_and_the_Transition_Matrix.md)
