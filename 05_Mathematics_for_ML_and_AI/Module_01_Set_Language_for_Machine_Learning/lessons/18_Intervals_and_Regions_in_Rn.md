# Lesson 01.18 — Intervals and Regions in R^n

> **Module 01:** Set Language for Machine Learning · Lesson 18 of 25

---

## What you will be able to do after this lesson

- [ ] Write intervals in ℝ and boxes in ℝⁿ in set-builder notation, and distinguish open from closed.
- [ ] Describe a norm ball and say which norm produces which shape.

## Prerequisites

- [Lesson 01.08](08_Cartesian_Products_and_Tuples.md) - Cartesian products.

---

## 1. The idea

The regions you constrain models with are sets, and the notation is worth
having.

**Intervals in ℝ.** Square bracket includes, round bracket excludes:

    [a, b] = {x : a ≤ x ≤ b}     closed
    (a, b) = {x : a < x < b}     open
    [a, b) = {x : a ≤ x < b}     half-open

Half-open is the workhorse in code: `range(a, b)` and array slicing are both
`[a, b)`, which is why consecutive slices tile without overlap or gap.

**Boxes in ℝⁿ** are products of intervals: `[0,1] × [0,1]` is the unit square.
A per-feature min/max constraint is exactly a box.

**Norm balls.** The set of points within radius r of the origin, where "within"
depends on the norm:

| Norm | Definition | Unit ball shape in ℝ² |
| :--- | :--- | :--- |
| `L¹` | `\|x\|₁ = Σ\|xᵢ\|` | diamond |
| `L²` | `\|x\|₂ = √(Σxᵢ²)` | circle |
| `L∞` | `\|x\|∞ = maxᵢ\|xᵢ\|` | square |

This is not decoration. L¹ regularisation produces sparse solutions because the
L¹ ball has **corners on the axes**, and a corner is where a coordinate is
exactly zero. The L² ball is smooth, so it has no such preferred points. The
geometry of these sets is the whole explanation for why lasso zeroes
coefficients and ridge does not.

## 2. Worked example

Is `x = 0.5` in `[0, 0.5)`? The right end is excluded, so no. In `[0, 0.5]`?
Yes.

**Why half-open tiles cleanly.** Split `[0, 1)` into three bins
`[0, 1/3)`, `[1/3, 2/3)`, `[2/3, 1)`. The point `1/3` belongs to exactly the
second. With closed intervals `[0, 1/3]` and `[1/3, 2/3]` it would belong to
both, and a histogram would double-count it.

**Norm balls at radius 1 in ℝ².** Test the point `(0.6, 0.6)`:

    L¹: 0.6 + 0.6 = 1.2 > 1   -> outside the diamond
    L²: √(0.36+0.36) = 0.849  -> inside the circle
    L∞: max(0.6, 0.6) = 0.6   -> inside the square

And `(0.9, 0.9)`: L¹ gives 1.8, L² gives 1.27, L∞ gives 0.9. Outside the first
two, inside the square. The nesting is general:

    L¹ ball ⊆ L² ball ⊆ L∞ ball

## 3. Verify it in code

```python
import numpy as np

# Half-open intervals tile without overlap or gap.
edges = [0.0, 1 / 3, 2 / 3, 1.0]
def bin_of(x):
    return next(i for i in range(3) if edges[i] <= x < edges[i + 1])

assert bin_of(1 / 3) == 1, "the boundary belongs to exactly one bin"
assert bin_of(0.0) == 0
assert [bin_of(x) for x in (0.1, 0.4, 0.9)] == [0, 1, 2]

# Membership of intervals.
assert not (0 <= 0.5 < 0.5)      # 0.5 not in [0, 0.5)
assert 0 <= 0.5 <= 0.5           # but it is in [0, 0.5]

# Norm balls, radius 1.
def in_ball(v, p):
    v = np.asarray(v, dtype=float)
    if p == 1:
        return float(np.abs(v).sum()) <= 1
    if p == 2:
        return float(np.sqrt((v ** 2).sum())) <= 1
    return float(np.abs(v).max()) <= 1

assert not in_ball((0.6, 0.6), 1)
assert in_ball((0.6, 0.6), 2)
assert in_ball((0.6, 0.6), "inf")

# The balls nest: L1 inside L2 inside Linf.
rng = np.random.default_rng(18)
pts = rng.uniform(-1.5, 1.5, size=(4000, 2))
for v in pts:
    if in_ball(v, 1):
        assert in_ball(v, 2)
    if in_ball(v, 2):
        assert in_ball(v, "inf")

# The L1 ball has corners exactly on the axes; the L2 ball does not.
assert in_ball((1.0, 0.0), 1) and not in_ball((0.71, 0.71), 1)
assert in_ball((1.0, 0.0), 2) and in_ball((0.70, 0.70), 2)
```

## 4. The mistake people actually make

**Mixing closed and half-open bins when bucketing.**

Histogram edges defined as `[0,1]`, `[1,2]`, `[2,3]` put the value 1 in two
buckets. Whether it is counted twice, or assigned to whichever comparison runs
first, depends on the implementation - so two libraries give different
histograms for the same data and nobody can say which is right.

NumPy's `histogram` uses half-open bins `[a, b)` except for the last, which is
closed on both ends so the maximum value is not dropped. That exception is
documented and is a frequent surprise: the final bin behaves differently from
all the others.

The symptom is a bin count that is off by a small amount, only for data landing
exactly on an edge - which is common when values are rounded to the same
precision as the edges. Define bins half-open, decide explicitly what happens at
the top end, and test with a value sitting exactly on a boundary.

---

## Check yourself

1. Is 1 in `[0, 1)`? Is it in `(0, 1]`?
2. Which norm ball has corners on the coordinate axes, and what does that cause in regularisation?
3. Why does `range(a, b)` exclude `b`?

<details>
<summary>Answers</summary>

1. Not in the first - the right end is excluded. Yes in the second - the right end is included.
2. The L¹ ball. Its corners sit where all but one coordinate is zero, so the constrained optimum tends to land on them, producing exactly-zero coefficients - the sparsity of lasso. The L² ball is smooth and has no such preferred points.
3. So consecutive ranges tile without overlap or gap: `range(0,3)` and `range(3,6)` cover 0-5 exactly once each, and the length is simply `b - a`.

</details>

---

## Lesson checklist

- [ ] Learning objectives are concrete and checkable
- [ ] Worked example has no skipped arithmetic
- [ ] Code block runs as written and asserts
- [ ] The common-mistake section names a specific failure
- [ ] Self-check questions have answers

---

[← Previous](17_Cardinality_and_Diagonal_Arguments.md) · [Module README](../README.md) · [Next →](19_Open_Closed_and_Bounded_Sets.md)
