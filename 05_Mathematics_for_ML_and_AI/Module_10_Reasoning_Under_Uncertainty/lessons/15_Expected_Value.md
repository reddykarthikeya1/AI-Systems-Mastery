# Lesson 10.15 — Expected Value

> **Module 10:** Reasoning Under Uncertainty · Lesson 15 of 41

---

## What you will be able to do after this lesson

- [ ] Compute expected value E[X] = sum x p(x) and integral x f(x) dx.
- [ ] Interpret expectation as the center of mass of the probability distribution.

## Prerequisites

- 10.12 PMF and 10.13 PDF.

---

## 1. The idea

The **expected value** $\mathbb{E}[X]$ is the probability-weighted average of all possible values, representing the physical center of mass of the distribution:
$$\mathbb{E}[X] = \sum_x x p(x) \quad (\text{discrete}), \quad \mathbb{E}[X] = \int_{-\infty}^\infty x f(x) dx \quad (\text{continuous})$$

---

## 2. Worked example

Fair die roll: $\mathbb{E}[X] = \frac{1}{6}(1 + 2 + 3 + 4 + 5 + 6) = 21/6 = 3.5$. Notice $3.5$ is not an outcome on the die.

---

## 3. Verify it in code

```python
import numpy as np
faces = np.arange(1, 7)
probs = np.full(6, 1.0 / 6.0)
expected_val = np.sum(faces * probs)
assert np.isclose(expected_val, 3.5)
```

---

## 4. The mistake people actually make

Expecting the expected value to be an outcome that can actually be observed in a single trial (e.g. 3.5 on a die).

---

## Check yourself

1. Must E[X] be a possible value that X can take?
2. What does E[X] represent physically?

<details>
<summary>Answers</summary>

1. No (e.g. average heads is 3.5 on a die).
2. The center of mass (balance point) of the probability distribution.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](16_Linearity_of_Expectation.md)
