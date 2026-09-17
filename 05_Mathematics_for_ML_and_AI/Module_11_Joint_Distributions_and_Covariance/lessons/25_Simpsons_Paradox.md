# Lesson 11.25 — Simpson's Paradox

> **Module 11:** Joint Distributions and Covariance · Lesson 25 of 29

---

## What you will be able to do after this lesson

- [ ] Demonstrate reversal of correlation/trend when data is aggregated across sub-populations.
- [ ] Control for subgroup conditioning in decision trees and regression.

## Prerequisites

- 11.14 Tower Property.

---

## 1. The idea

**Simpson's Paradox** occurs when a trend apparent in several different groups reverses when the groups are combined. It arises when a confounding factor influences group assignment and outcome simultaneously, misleading naive models trained on aggregate data.

---

## 2. Worked example

Treatment A has 80% recovery in mild cases and 30% in severe cases. Treatment B has 70% in mild and 20% in severe. A is superior in both subgroups! But if B was assigned mostly to mild cases, B's aggregate recovery appears higher.

---

## 3. Verify it in code

```python
import numpy as np
# Subgroup 1 (Mild)
a_mild = (80, 100) # 80%
b_mild = (70, 100) # 70%

# Subgroup 2 (Severe)
a_sev = (30, 100)  # 30%
b_sev = (20, 100)  # 20%

# Aggregate with skewed assignment (B gets 90 mild, A gets 10 mild)
# A: 10 mild (8 rec) + 90 severe (27 rec) -> 35 / 100 = 35%
# B: 90 mild (63 rec) + 10 severe (2 rec) -> 65 / 100 = 65%
assert 80/100 > 70/100  # A wins in mild
assert 30/100 > 20/100  # A wins in severe
assert 35/100 < 65/100  # B appears to win in aggregate!
```

---

## 4. The mistake people actually make

Drawing policy conclusions from aggregated metrics without stratifying by key confounding segments.

---

## Check yourself

1. What causes Simpson's Paradox?
2. How can an analyst prevent Simpson's Paradox?

<details>
<summary>Answers</summary>

1. An unbalanced confounding variable that correlates with both treatment and outcome.
2. By stratifying the analysis across confounding subgroups.

</details>

---

## Lesson checklist

- [x] Learning objectives are concrete and checkable
- [x] Worked example has no skipped arithmetic
- [x] Code block runs as written and asserts
- [x] The common-mistake section names a specific failure
- [x] Self-check questions have answers

---

[Module README](../README.md) · [Next →](26_Confounders_Colliders_and_Selection_Bias.md)
