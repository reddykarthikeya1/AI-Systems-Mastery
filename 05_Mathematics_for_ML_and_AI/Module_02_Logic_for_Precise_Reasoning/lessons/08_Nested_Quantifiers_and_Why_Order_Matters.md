# Lesson 02.08 — Nested Quantifiers and Why Order Matters

> **Module 02:** Logic for Precise Reasoning · Lesson 8 of 19

---

## What you will be able to do after this lesson

- [ ] Explain why `∀x ∃y` and `∃y ∀x` differ, with a concrete example of each.
- [ ] Identify which order a definition uses and what changes if the quantifiers are swapped.

## Prerequisites

- [Lesson 02.07](07_Universal_and_Existential_Quantifiers.md) - quantifiers.

---

## 1. The idea

**Quantifier order changes meaning.** This is the single most consequential piece
of notation in reading mathematics.

    ∀x ∃y : P(x, y)     for each x, some y works - y may depend on x
    ∃y ∀x : P(x, y)     one y works for all x - y is chosen first

The second is strictly stronger: `∃y ∀x` implies `∀x ∃y`, never the reverse.

The everyday version: "everyone has a mother" is `∀x ∃y`. "There is someone who
is everyone's mother" is `∃y ∀x`. Both use the same words in a different order,
and only the first is true.

Where it decides a definition: the epsilon-delta definition of **uniform**
continuity differs from ordinary continuity by exactly this swap.

    continuous:          ∀ε ∀x ∃δ    (δ may depend on x)
    uniformly continuous: ∀ε ∃δ ∀x    (one δ works everywhere)

`f(x) = x²` on ℝ is continuous and not uniformly continuous: as x grows the
function steepens, so any fixed δ eventually fails. That distinction is why some
convergence proofs need uniform bounds and others do not.

## 2. Worked example

Domain: integers. `P(x, y)` = "x + y = 0".

**`∀x ∃y : x + y = 0`** - for each x, pick `y = -x`. True. The choice of y
depends on x, which is permitted.

**`∃y ∀x : x + y = 0`** - one y making `x + y = 0` for *every* x. It would have
to satisfy `1 + y = 0` and `2 + y = 0` at once. False.

Same predicate, same domain, opposite answers.

The implication goes one way only. If some y works for all x, then certainly for
each x some y works - take that same one. So

    (∃y ∀x : P) → (∀x ∃y : P)

and the converse fails, as above.

For the continuity example, take `f(x) = x²` and `ε = 1`. Near x = 1, a δ of
about 0.3 keeps `|f(x) - f(1)| < 1`. Near x = 1000 the same δ gives a change of
roughly `2 · 1000 · 0.3 = 600`, far exceeding ε. A δ exists for each x, and no
single δ serves them all.

## 3. Verify it in code

```python
domain = range(-20, 21)

# For each x there is a y: true.
assert all(any(x + y == 0 for y in domain) for x in domain)

# There is a y for all x: false.
assert not any(all(x + y == 0 for x in domain) for y in domain)

# The one-way implication, checked on a predicate where both happen to hold.
Q = lambda x, y: (x * y) % 1 == 0          # true for all integer pairs
assert any(all(Q(x, y) for x in domain) for y in domain)
assert all(any(Q(x, y) for y in domain) for x in domain)

# x^2 is continuous but not uniformly continuous: no single delta works.
def max_change(x, delta):
    return abs((x + delta) ** 2 - x ** 2)

epsilon = 1.0
# Near x = 1 a modest delta suffices...
assert max_change(1.0, 0.3) < epsilon
# ...and the same delta fails badly far out.
assert max_change(1000.0, 0.3) > epsilon
assert max_change(1000.0, 0.3) > 500

# For each x a delta exists (continuity).
for x in (1.0, 10.0, 1000.0):
    delta = epsilon / (2 * abs(x) + 1)
    assert max_change(x, delta) < epsilon
```

## 4. The mistake people actually make

**Reading `∀ε ∃δ ∀x` as if the δ could depend on x.**

Uniform continuity, uniform convergence, and uniform bounds in generalisation
theory all hinge on one quantifier moving. A bound of the form

    ∃N ∀f ∈ F : error(f) ≤ N

says one N covers the whole function class - which is what makes a
generalisation guarantee useful. The weaker

    ∀f ∈ F ∃N : error(f) ≤ N

says each function has some bound, which is nearly vacuous: it does not stop the
bounds from growing without limit across the class.

Papers state the strong form, and the proof is hard for exactly that reason. If
you find yourself thinking a bound is obvious, check whether you have silently
read the quantifiers in the weak order.

The tell in prose: the words "uniformly", "there exists a constant C such that
for all", and "independent of x" all signal that a quantifier has been pulled to
the front, and that is where the content is.

---

## Check yourself

1. Which is stronger, `∀x ∃y P(x,y)` or `∃y ∀x P(x,y)`? Why?
2. Give a predicate where `∀x ∃y` holds and `∃y ∀x` fails.
3. What exactly does 'uniformly' signal in a theorem statement?

<details>
<summary>Answers</summary>

1. The second. A single y serving every x also serves each x individually, so it implies the first. The converse fails, because the first permits y to change with x.
2. 'x + y = 0' over the integers. For each x take y = -x; but no single y satisfies it for every x, since it would need to equal both -1 and -2.
3. That an existential quantifier has been moved in front of a universal - one choice works for every case, rather than a different choice per case. It is almost always the substantive part of the claim.

</details>

---

## Lesson checklist

- [ ] Learning objectives are concrete and checkable
- [ ] Worked example has no skipped arithmetic
- [ ] Code block runs as written and asserts
- [ ] The common-mistake section names a specific failure
- [ ] Self-check questions have answers

---

[← Previous](07_Universal_and_Existential_Quantifiers.md) · [Module README](../README.md) · [Next →](09_Negating_Quantified_Statements.md)
