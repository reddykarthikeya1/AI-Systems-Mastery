# Lesson 01.19 — Open, Closed and Bounded Sets

> **Module 01:** Set Language for Machine Learning · Lesson 19 of 25

---

## What you will be able to do after this lesson

- [ ] Decide whether a given set is open, closed, both, or neither.
- [ ] State why a continuous function on a closed and bounded set attains its maximum, and why that fails on an open set.

## Prerequisites

- [Lesson 01.18](18_Intervals_and_Regions_in_Rn.md) - intervals and regions.

---

## 1. The idea

Three properties of a subset of ℝⁿ, and one theorem that makes them matter.

**Open.** Every point has some room around it that is still inside the set. The
interval `(0,1)` is open: whatever point you pick, there is a small ball around
it still inside.

**Closed.** The complement is open. Equivalently, the set contains all its
limit points - a sequence inside it cannot converge to something outside.
`[0,1]` is closed.

**Bounded.** The set fits inside some ball of finite radius.

Open and closed are not opposites. `[0,1)` is neither. `∅` and `ℝⁿ` are both.

The reason this appears in an ML course is one theorem:

> **Extreme Value Theorem.** A continuous function on a set that is closed
> *and* bounded attains its maximum and minimum somewhere in the set.

Drop either condition and it fails. On `(0,1)`, the function `f(x) = x` has
supremum 1 and never attains it - the candidate maximiser is exactly the point
the set excludes. On the unbounded `[0,∞)`, `f(x) = x` has no maximum at all.

So "does a best parameter exist" is a question about the *shape of the feasible
set*, before any optimisation algorithm is chosen.

## 2. Worked example

Classify a few subsets of ℝ.

| Set | Open? | Closed? | Bounded? |
| :--- | :--- | :--- | :--- |
| `(0,1)` | yes | no | yes |
| `[0,1]` | no | yes | yes |
| `[0,1)` | no | no | yes |
| `[0,∞)` | no | yes | no |
| `ℝ` | yes | yes | no |
| `∅` | yes | yes | yes |

**Why `[0,1)` is not closed:** the sequence `0.9, 0.99, 0.999, ...` lies inside
it and converges to 1, which is outside. A closed set must contain such limits.

**Why `[0,1)` is not open:** the point 0 has no room to its left - every ball
around 0 contains negative numbers, which are outside.

**The maximum failing.** `f(x) = x` on `(0,1)`: values get arbitrarily close to
1, so the supremum is 1, but `f(x) = 1` has no solution with `x ∈ (0,1)`. The
sequence `1 - 1/n` climbs toward it forever without arriving. Close the interval
and the maximum exists immediately, at `x = 1`.

## 3. Verify it in code

```python
import numpy as np

# [0,1) is not closed: a sequence inside converges to a point outside.
seq = [1 - 10 ** -k for k in range(1, 12)]
assert all(0 <= x < 1 for x in seq)
assert abs(seq[-1] - 1.0) < 1e-10
assert not (0 <= 1.0 < 1), "the limit is outside the set"

# [0,1) is not open either: 0 has no room to its left.
eps = 1e-12
assert not (0 <= 0 - eps < 1)

# Maximum of f(x) = x on (0,1): approached, never attained.
best = max(seq)
assert best < 1.0
assert 1.0 - best < 1e-10, "arbitrarily close"
assert all(x < 1.0 for x in seq), "and never equal"

# On the closed interval the maximiser is a member of the set.
closed_pts = np.linspace(0.0, 1.0, 1001)
arg = closed_pts[int(np.argmax(closed_pts))]
assert arg == 1.0
assert 0.0 <= arg <= 1.0, "the maximiser is IN the feasible set"

# Boundedness matters too: no maximum on [0, inf).
growing = [float(x) for x in range(1, 10_000)]
assert max(growing) < float(max(growing) + 1), "always something larger"

# Both empty set and R^n are open and closed simultaneously.
assert set() == set()
```

## 4. The mistake people actually make

**Writing a strict inequality constraint and expecting an optimum to exist.**

A constraint like `weight > 0` defines an open set. If the objective is
minimised as the weight approaches 0, there is no minimiser: every feasible
point has a better feasible point closer to the boundary.

An optimiser handed this does not report "no solution". It marches toward the
boundary and returns whatever it had when the iteration limit or tolerance
stopped it - a number that depends on the step size and the stopping rule rather
than on the problem. Run it twice with different settings and get different
"optima".

The fix is to close the set: use `weight >= 1e-8` rather than `weight > 0`, and
choose the bound deliberately. That converts "no minimiser exists" into "the
minimiser is at the bound", which is a fact you can see and reason about.

The same issue explains why unregularised logistic regression on perfectly
separable data has no finite optimum: the likelihood increases without bound as
the coefficients grow, the feasible set is unbounded, and the fit only stops
because the iteration limit did.

---

## Check yourself

1. Classify `(0, 5]` as open, closed, both or neither, and justify.
2. Why does `f(x) = x` have no maximum on `(0,1)` but does on `[0,1]`?
3. A colleague constrains a parameter with `p > 0` and gets different optima from different random seeds. What is the structural cause?

<details>
<summary>Answers</summary>

1. Neither. Not open, because 5 has no room to its right inside the set. Not closed, because the sequence 1/n lies inside and converges to 0, which is excluded.
2. The supremum is 1 in both cases. On `(0,1)` the point 1 is not in the set, so the value is approached but never attained. On `[0,1]` the point 1 is a member, so the maximum is attained there.
3. The feasible set is open, so if the objective improves as p approaches 0 there is no minimiser. The returned value is determined by where the iteration happened to stop, not by the problem. Closing the constraint to `p >= ε` gives a well-posed problem.

</details>

---

## Lesson checklist

- [ ] Learning objectives are concrete and checkable
- [ ] Worked example has no skipped arithmetic
- [ ] Code block runs as written and asserts
- [ ] The common-mistake section names a specific failure
- [ ] Self-check questions have answers

---

[← Previous](18_Intervals_and_Regions_in_Rn.md) · [Module README](../README.md) · [Next →](20_Convex_Sets_and_Why_ML_Cares.md)
