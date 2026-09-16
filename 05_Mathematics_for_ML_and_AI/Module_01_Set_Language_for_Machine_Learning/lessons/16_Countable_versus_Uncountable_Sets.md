# Lesson 01.16 — Countable versus Uncountable Sets

> **Module 01:** Set Language for Machine Learning · Lesson 16 of 25

---

## What you will be able to do after this lesson

- [ ] Distinguish finite, countably infinite and uncountable sets, and place ℕ, ℤ, ℚ and ℝ correctly.
- [ ] Explain what 'same size' means for infinite sets and why it is defined by bijection.

## Prerequisites

- [Lesson 01.12](12_Injective_Surjective_and_Bijective_Maps.md) - bijections.

---

## 1. The idea

Two sets have the **same cardinality** when there is a bijection between them.
For finite sets that reproduces counting. For infinite sets it is the only
definition that works, and it produces conclusions that feel wrong at first.

A set is **countable** if it is finite or can be put in bijection with ℕ - that
is, its elements can be listed in a sequence `a_0, a_1, a_2, ...` that
eventually reaches every one of them. Otherwise it is **uncountable**.

The facts worth carrying:

| Set | Cardinality |
| :--- | :--- |
| ℕ, ℤ, ℚ | countably infinite |
| ℝ, any real interval, ℝⁿ | uncountable |
| ℤ × ℤ, finite unions and products of countable sets | countable |
| The power set of any infinite set | strictly larger |

ℤ being countable is already surprising: it looks twice the size of ℕ. But
`0, 1, -1, 2, -2, ...` lists every integer, and that listing *is* a bijection
with ℕ. "Half as many" has no meaning here; the only question is whether a
pairing exists.

Why an ML course cares: the set of floating-point numbers is **finite**, the set
of reals is uncountable, and the gap between them is where numerical error
lives. Your model's parameters do not range over ℝ - they range over about 2⁶⁴
values with wildly uneven spacing.

## 2. Worked example

**ℤ is countable.** Define `g : ℕ → ℤ` by

    g(n) = n/2        if n is even
    g(n) = -(n+1)/2   if n is odd

Then `g(0)=0, g(1)=-1, g(2)=1, g(3)=-2, g(4)=2, ...`. Every integer appears
exactly once, so g is a bijection and `|ℤ| = |ℕ|`.

**ℚ is countable.** Arrange the positive fractions `p/q` in a grid with p across
and q down, then walk the diagonals: `1/1, 1/2, 2/1, 1/3, 2/2, 3/1, ...`,
skipping any fraction already seen in lower terms. Every positive rational is
reached at a finite step. Interleave the negatives and zero as for ℤ.

**ℝ is not countable** - Cantor's diagonal argument, taken up in the next
lesson.

A finite check of the pairing idea: the first 6 naturals map to
`{0, -1, 1, -2, 2, -3}`, six distinct integers. Extend the range and you get a
distinct integer every time, never a repeat and never a gap.

## 3. Verify it in code

```python
def g(n):
    return n // 2 if n % 2 == 0 else -(n + 1) // 2

first = [g(n) for n in range(6)]
assert first == [0, -1, 1, -2, 2, -3]

# Injective on any prefix: no two naturals give the same integer.
values = [g(n) for n in range(2000)]
assert len(set(values)) == len(values)

# Surjective onto every integer in a range: nothing is skipped.
assert set(values) >= set(range(-500, 500))

# Countability of a product: pair up N x N by diagonals.
def diagonal_pairs(limit):
    out = []
    total = 0
    while len(out) < limit:
        out += [(i, total - i) for i in range(total + 1)]
        total += 1
    return out[:limit]

pairs = diagonal_pairs(500)
assert len(set(pairs)) == 500, "each pair listed once"
assert (3, 4) in diagonal_pairs(200), "and every pair is eventually reached"

# The set of float64 values is FINITE - unlike the reals it approximates.
import numpy as np
assert np.finfo(np.float64).bits == 64
assert np.nextafter(1.0, 2.0) > 1.0
gap = np.nextafter(1.0, 2.0) - 1.0
assert gap > 0, "there is a smallest step above 1.0; the reals have none"
assert np.nextafter(1e16, 2e16) - 1e16 > gap, "and the spacing is not uniform"
```

## 4. The mistake people actually make

**Reasoning about floating-point parameters as if they were real numbers.**

"The loss is continuous, so a small enough step always decreases it" is a
statement about ℝ. In float64 there is a smallest representable step near any
value, and near 1.0 it is about 2.2e-16 while near 1e16 it is 2. A gradient step
smaller than the local spacing changes nothing at all: `x + h == x`, and the
optimiser stalls with no error.

The same gap explains why `0.1 + 0.2 != 0.3`, why summing a million small
numbers loses accuracy unless you sum them in a good order, and why testing a
float for equality with zero is a question about one bit pattern out of 2⁶⁴
rather than about magnitude.

The practical habit: when a numerical method "stops improving", check whether
the step has fallen below the local spacing before concluding the method has
converged. Those are different things, and only one of them means you are done.

---

## Check yourself

1. Is the set of even integers countable? Give the bijection.
2. What does it mean for two infinite sets to have the same size?
3. Why is the spacing between representable float64 values not constant?

<details>
<summary>Answers</summary>

1. Yes. `n ↦ 2n` is a bijection from ℤ to the evens, and ℤ is countable, so the evens are too - despite being a proper subset.
2. That a bijection exists between them: a pairing that matches every element of one with exactly one element of the other, with nothing left over on either side.
3. Floating point stores a fixed number of significant bits and a separate exponent, so the absolute gap scales with magnitude. Near 1.0 it is about 2.2e-16; near 1e16 it is about 2.

</details>

---

## Lesson checklist

- [ ] Learning objectives are concrete and checkable
- [ ] Worked example has no skipped arithmetic
- [ ] Code block runs as written and asserts
- [ ] The common-mistake section names a specific failure
- [ ] Self-check questions have answers

---

[← Previous](15_Indexed_Families_and_Big_Unions.md) · [Module README](../README.md) · [Next →](17_Cardinality_and_Diagonal_Arguments.md)
