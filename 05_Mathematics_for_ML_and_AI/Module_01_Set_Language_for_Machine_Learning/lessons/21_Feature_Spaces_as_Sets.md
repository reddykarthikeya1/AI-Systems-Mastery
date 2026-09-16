# Lesson 01.21 — Feature Spaces as Sets

> **Module 01:** Set Language for Machine Learning · Lesson 21 of 25

---

## What you will be able to do after this lesson

- [ ] Describe a feature space as a product of per-feature value sets and identify its dimension.
- [ ] Explain why volume concentrates at the boundary in high dimensions, with a computed figure.

## Prerequisites

- [Lesson 01.08](08_Cartesian_Products_and_Tuples.md) - Cartesian products.
- [Lesson 01.18](18_Intervals_and_Regions_in_Rn.md) - regions in ℝⁿ.

---

## 1. The idea

A **feature space** is the set of all possible feature vectors: the Cartesian
product of each feature's value set. A dataset is a finite subset of it, and a
model is a function defined on it.

With three numeric features scaled to `[0,1]`, the space is `[0,1]³` - the unit
cube. Add a categorical feature with 4 levels and it becomes
`[0,1]³ × {a,b,c,d}`.

The dimension is the number of features, and high dimension behaves in ways
low-dimensional intuition does not predict. Two facts with concrete numbers:

**Volume flees to the corners.** The ball inscribed in the unit cube occupies
about 52% of it in 3 dimensions, 0.25% in 10 dimensions, and around 10⁻¹⁴ in
50. Nearly all the cube's volume is in the corners - the regions far from the
centre in at least one coordinate.

**Everything becomes equidistant.** For points drawn uniformly in a
high-dimensional cube, the ratio of the farthest to the nearest distance from a
query point approaches 1. "Nearest neighbour" stops being a meaningful
distinction, which is why k-NN degrades in high dimensions and why dimensionality
reduction is not merely an efficiency measure.

These are collectively the **curse of dimensionality**, and both are facts about
the *set*, before any model is fitted.

## 2. Worked example

**Fraction of the cube inside the inscribed ball.** The ball of radius 1/2 in
`[0,1]ⁿ` has volume `π^(n/2) / (Γ(n/2 + 1) · 2ⁿ)`; the cube has volume 1. The
ratios:

| n | fraction inside the ball |
| ---: | ---: |
| 2 | 0.785 |
| 3 | 0.524 |
| 5 | 0.164 |
| 10 | 0.0025 |
| 20 | 2.5 × 10⁻⁸ |

By dimension 10, 99.75% of the cube is outside its own inscribed ball.

**Distance concentration.** Draw 1,000 points uniformly from `[0,1]ⁿ` and measure
distances from a query point:

| n | nearest | farthest | ratio |
| ---: | ---: | ---: | ---: |
| 2 | ~0.02 | ~1.1 | ~55 |
| 100 | ~3.3 | ~5.1 | ~1.5 |

In 2 dimensions the farthest point is 55 times the distance of the nearest; in
100 dimensions it is only about 1.5 times. The notion of "close" has almost
stopped discriminating.

## 3. Verify it in code

```python
import numpy as np
from math import gamma, pi

def ball_fraction(n):
    return pi ** (n / 2) / (gamma(n / 2 + 1) * 2 ** n)

assert abs(ball_fraction(2) - 0.7853981) < 1e-6
assert abs(ball_fraction(3) - 0.5235987) < 1e-6
assert ball_fraction(10) < 0.003
assert ball_fraction(20) < 1e-7
# The fraction falls monotonically once past n = 1.
fractions = [ball_fraction(n) for n in range(2, 25)]
assert all(a > b for a, b in zip(fractions, fractions[1:]))

# A feature space is a product; a dataset is a finite subset of it.
from itertools import product
levels = [{0, 1}, {"a", "b", "c"}, {"S", "M"}]
space = set(product(*levels))
assert len(space) == 2 * 3 * 2 == 12
dataset = [(0, "a", "S"), (1, "c", "M")]
assert all(row in space for row in dataset)

# Distance concentration.
rng = np.random.default_rng(21)

def distance_ratio(n, points=1000):
    data = rng.uniform(0, 1, size=(points, n))
    query = rng.uniform(0, 1, size=n)
    d = np.linalg.norm(data - query, axis=1)
    return float(d.max() / d.min())

low, high = distance_ratio(2), distance_ratio(100)
assert low > 10, f"in 2D the farthest is far more distant than the nearest ({low:.1f}x)"
assert high < 3, f"in 100D they are nearly the same ({high:.2f}x)"
assert high < low
```

## 4. The mistake people actually make

**Assuming more features can only help, because a model can ignore the useless ones.**

In principle a model can zero out an irrelevant feature. In practice each added
dimension spreads the same number of training points over an exponentially
larger space, so the local neighbourhood any method relies on becomes empty.

The number that makes it concrete: to keep the same *density* of samples as you
add a dimension, you need to multiply the dataset size by the number of bins per
axis. Ten bins per axis and 5 features is 100,000 cells; at 10 features it is
10¹⁰ cells - vastly more cells than you will ever have rows, so almost every
cell is empty regardless of how much data you collect.

The symptom is a model whose training accuracy is excellent and whose test
accuracy falls as features are added. It gets diagnosed as overfitting, which is
correct, but the cause is geometric rather than a failure of regularisation
strength - and no amount of tuning recovers the missing density.

---

## Check yourself

1. Three numeric features in [0,1] and one categorical with 5 levels. Describe the feature space.
2. What fraction of the unit cube in 10 dimensions lies inside its inscribed ball, roughly?
3. Why does k-nearest-neighbours degrade in high dimensions even with plenty of data?

<details>
<summary>Answers</summary>

1. `[0,1]³ × {1,...,5}` - the Cartesian product of the three unit intervals with the 5-element level set. It is 3-dimensional continuously, with 5 discrete sheets.
2. About 0.25%. Nearly all the volume of a high-dimensional cube is in its corners, away from the inscribed ball.
3. Distances concentrate: the ratio of farthest to nearest distance approaches 1, so the 'nearest' neighbours are barely nearer than the farthest points, and the neighbourhood carries little information about the query.

</details>

---

## Lesson checklist

- [ ] Learning objectives are concrete and checkable
- [ ] Worked example has no skipped arithmetic
- [ ] Code block runs as written and asserts
- [ ] The common-mistake section names a specific failure
- [ ] Self-check questions have answers

---

[← Previous](20_Convex_Sets_and_Why_ML_Cares.md) · [Module README](../README.md) · [Next →](22_Label_Sets_and_OneHot_Encoding.md)
