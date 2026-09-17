# Lesson 10.16 — Linearity of Expectation

> **Module 10:** Reasoning Under Uncertainty · Lesson 16 of 41

---

## What you will be able to do after this lesson

- [ ] Apply universal property E[a X + b Y] = a E[X] + b E[Y].
- [ ] Prove linearity holds unconditionally without requiring independence.

## Prerequisites

- 10.15 Expected Value.

---

## 1. The idea

**Linearity of Expectation** is the most powerful algebraic weapon in probability:
$$\mathbb{E}[aX + bY + c] = a\mathbb{E}[X] + b\mathbb{E}[Y] + c$$
It holds **unconditionally**, whether $X$ and $Y$ are independent, correlated, or adversarial!

---

## 2. Worked example

Sum of 10 dice: expected value of each is $3.5$. Expected sum is $10 \times 3.5 = 35$, even if dice are magnetic and strongly correlated.

---

## 3. Verify it in code

```python
import numpy as np
# Even for correlated X and Y
x = np.array([1.0, 2.0, 3.0])
y = x**2
e_x = np.mean(x)
e_y = np.mean(y)
e_comb = np.mean(2.0 * x + 3.0 * y)
assert np.isclose(e_comb, 2.0 * e_x + 3.0 * e_y)
```

---

## 4. The mistake people actually make

Assuming variables must be independent to use E[X + Y] = E[X] + E[Y]. Linearity requires no independence at all.

---

## Check yourself

1. Must X and Y be independent for E[X + Y] = E[X] + E[Y] to hold?
2. What is E[c] for constant c?

<details>
<summary>Answers</summary>

1. No, linearity holds for any random variables whatsoever.
2. c.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](17_Variance_and_Standard_Deviation.md)
