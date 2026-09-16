# Lesson 01.20 — Convex Sets and Why ML Cares

> **Module 01:** Set Language for Machine Learning · Lesson 20 of 25

---

## What you will be able to do after this lesson

- [ ] Test whether a set is convex using the segment definition.
- [ ] State what convexity of the feasible set and the objective together guarantee about local minima.

## Prerequisites

- [Lesson 01.19](19_Open_Closed_and_Bounded_Sets.md) - closed and bounded sets.

---

## 1. The idea

A set `C` is **convex** when, for any two of its points, the whole straight
segment between them stays inside:

    x, y ∈ C  and  0 ≤ t ≤ 1   ⟹   t·x + (1-t)·y ∈ C

The expression `t·x + (1-t)·y` is a **convex combination**; as t sweeps 0 to 1 it
traces the segment from y to x.

Convex: intervals, boxes, all norm balls, half-spaces, ℝⁿ, the probability
simplex. Not convex: a set with a hole or a dent, the union of two disjoint
boxes, the surface of a sphere.

Two closure properties that let you build convex sets confidently:

- The **intersection** of any family of convex sets is convex. So a system of
  linear inequality constraints - each a half-space - always carves out a convex
  region.
- The **union** of convex sets generally is not. Two disjoint intervals are the
  standard counterexample.

Why it is the central concept in optimisation:

> If the feasible set is convex **and** the objective is convex, then every
> local minimum is a global minimum.

That is the property that makes linear regression, ridge, lasso, SVMs and
logistic regression reliably solvable, and its absence is why neural network
training has no such guarantee.

## 2. Worked example

**A disc is convex.** Take `‖x‖ ≤ 1` and `‖y‖ ≤ 1`. By the triangle inequality,

    ‖t·x + (1-t)·y‖ ≤ t‖x‖ + (1-t)‖y‖ ≤ t + (1-t) = 1

so the combination is in the disc. The argument used only the triangle
inequality and homogeneity, so it works for *every* norm - which is why all norm
balls are convex.

**An annulus is not.** Let `C = {x : 1 ≤ ‖x‖ ≤ 2}`. Take `x = (1.5, 0)` and
`y = (-1.5, 0)`, both in C. Their midpoint is `(0, 0)`, whose norm is 0 < 1, so
it is outside. One counterexample settles it.

**Two disjoint intervals.** `[0,1] ∪ [2,3]`: take 1 and 2, both members. Their
midpoint 1.5 is in neither. Not convex.

**The simplex is convex.** `{p : pᵢ ≥ 0, Σpᵢ = 1}`. If p and q both qualify then
`t·p + (1-t)·q` has non-negative entries, and its sum is
`t·1 + (1-t)·1 = 1` ✓. This is why averaging two probability distributions gives
a probability distribution.

## 3. Verify it in code

```python
import numpy as np

rng = np.random.default_rng(20)

def segment_stays_inside(member, samples, steps=25):
    for _ in range(samples):
        x, y = rng.uniform(-2, 2, 2), rng.uniform(-2, 2, 2)
        if not (member(x) and member(y)):
            continue
        for t in np.linspace(0, 1, steps):
            if not member(t * x + (1 - t) * y):
                return False, (x, y, t)
    return True, None

disc = lambda v: float(np.linalg.norm(v)) <= 1
ok, _ = segment_stays_inside(disc, 400)
assert ok, "a norm ball is convex"

annulus = lambda v: 1 <= float(np.linalg.norm(v)) <= 2
x, y = np.array([1.5, 0.0]), np.array([-1.5, 0.0])
assert annulus(x) and annulus(y)
assert not annulus(0.5 * x + 0.5 * y), "the midpoint falls in the hole"

# Union of disjoint intervals is not convex.
two = lambda s: (0 <= s <= 1) or (2 <= s <= 3)
assert two(1) and two(2) and not two(1.5)

# Intersection of convex sets is convex; half-spaces give a convex polytope.
box = lambda v: bool(np.all(v >= 0) and np.all(v <= 1))
half = lambda v: float(v[0] + v[1]) <= 1
both = lambda v: box(v) and half(v)
ok, witness = segment_stays_inside(both, 400)
assert ok, witness

# The probability simplex is convex: averaging distributions gives a distribution.
p = np.array([0.2, 0.3, 0.5])
q = np.array([0.7, 0.1, 0.2])
for t in np.linspace(0, 1, 11):
    mix = t * p + (1 - t) * q
    assert np.all(mix >= 0)
    assert abs(mix.sum() - 1.0) < 1e-12
```

## 4. The mistake people actually make

**Assuming a local minimum is global because the objective is convex.**

Convexity of the *objective* is only half the condition. The feasible *set* must
be convex too, and constraints routinely break it.

The clearest case is a cardinality constraint: "use at most k of the features".
The set of vectors with at most k non-zeros is a union of coordinate subspaces -
convex in each piece, and not convex as a whole, because averaging two sparse
vectors with different support gives a denser one. Best-subset selection is
NP-hard for exactly this reason.

Lasso is the standard response: replace the non-convex cardinality constraint
with an L¹ ball, which is convex and whose corners still encourage sparsity. You
get a solvable problem and an approximation to the one you wanted, and knowing
it is an approximation is the point.

Integer constraints break convexity the same way. "This count must be a whole
number" makes the feasible set a lattice of isolated points, and no segment
between two of them stays inside.

---

## Check yourself

1. Is the set `{(x,y) : x² + y² = 1}` - the circle itself, not the disc - convex?
2. Prove the intersection of two convex sets is convex.
3. Why is 'at most k non-zero coefficients' not a convex constraint?

<details>
<summary>Answers</summary>

1. No. Take `(1,0)` and `(-1,0)`, both on the circle. Their midpoint is the origin, whose distance from the centre is 0, not 1, so it is not on the circle.
2. Let x, y be in `C ∩ D`. Since both are in C and C is convex, the segment lies in C; the same argument puts it in D. So the segment lies in the intersection.
3. Averaging two vectors with different supports produces a vector whose support is the union, which can exceed k. The feasible set is a union of subspaces, and a union of convex sets is generally not convex.

</details>

---

## Lesson checklist

- [ ] Learning objectives are concrete and checkable
- [ ] Worked example has no skipped arithmetic
- [ ] Code block runs as written and asserts
- [ ] The common-mistake section names a specific failure
- [ ] Self-check questions have answers

---

[← Previous](19_Open_Closed_and_Bounded_Sets.md) · [Module README](../README.md) · [Next →](21_Feature_Spaces_as_Sets.md)
