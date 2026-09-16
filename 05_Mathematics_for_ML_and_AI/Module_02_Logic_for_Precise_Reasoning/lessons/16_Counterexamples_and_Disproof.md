# Lesson 02.16 — Counterexamples and Disproof

> **Module 02:** Logic for Precise Reasoning · Lesson 16 of 19

---

## What you will be able to do after this lesson

- [ ] Disprove a universal claim by constructing a single counterexample.
- [ ] Search a bounded space for a counterexample and state what an empty search does and does not show.

## Prerequisites

- [Lesson 02.09](09_Negating_Quantified_Statements.md) - negation of quantifiers.

---

## 1. The idea

To disprove `∀x : P(x)`, exhibit one x with `¬P(x)`. That is the whole
obligation - the negation rule from Lesson 02.09 says the negation *is* an
existential, so one witness settles it.

This asymmetry is worth exploiting. Refuting a universal claim is often far
cheaper than proving it, so when you meet a claim you doubt, look for the
counterexample before attempting a proof. A short search either resolves the
question or tells you the claim is probably true and worth proving properly.

**Where to look.** Counterexamples cluster at the boundaries:

| Try | Because |
| :--- | :--- |
| 0, 1, -1 | identities and sign changes |
| the empty collection | vacuous cases, division by size |
| a single element | anything comparing pairs |
| equal values | tie-breaking and strictness |
| the largest representable value | overflow and saturation |
| negative values | anything assuming positivity |

**What a failed search proves: nothing.** Not finding a counterexample in a
bounded region leaves the claim unproved. It may be true, or the counterexample
may be outside the range, or rare. Absence of a witness is not a proof - it is
an absence of a witness.

## 2. Worked example

**Claim.** For all real x, `√(x²) = x`.

Try `x = -3`. Then `√((-3)²) = √9 = 3`, and `3 ≠ -3`. Disproved. The correct
statement is `√(x²) = |x|`.

**Claim.** For all sets A, B: `f(A ∩ B) = f(A) ∩ f(B)`.

Take `f(x) = x²` on `{-1, 1}`, `A = {1}`, `B = {-1}`. Then `A ∩ B = ∅`, so the
left side is `∅`. But `f(A) = {1}` and `f(B) = {1}`, so the right side is `{1}`.
Disproved - and this is Lesson 01.14's asymmetry, found by searching the
boundary case "disjoint inputs".

**Claim.** For all integers `n ≥ 0`, `n² + n + 41` is prime.

It holds for n = 0 through 39 - forty consecutive successes. At `n = 40`:

    40² + 40 + 41 = 1681 = 41²

not prime. Forty confirming cases and the claim is false, which is the sharpest
possible illustration that testing is not proving.

## 3. Verify it in code

```python
from math import isqrt

# sqrt(x^2) = x is false for negative x.
assert (abs(-3) ** 2) ** 0.5 == 3.0
assert 3.0 != -3.0
assert all(((x * x) ** 0.5) == abs(x) for x in [-5.0, -1.0, 0.0, 2.5])

# Image does not commute with intersection.
f = lambda x: x * x
A, B = {1}, {-1}
assert A & B == set()
assert {f(x) for x in A & B} == set()
assert {f(x) for x in A} & {f(x) for x in B} == {1}

# n^2 + n + 41: prime for 0..39, composite at 40.
def is_prime(n):
    return n >= 2 and all(n % d for d in range(2, isqrt(n) + 1))

assert all(is_prime(n * n + n + 41) for n in range(40))
assert not is_prime(40 * 40 + 40 + 41)
assert 40 * 40 + 40 + 41 == 1681 == 41 * 41

# A bounded search that finds nothing proves nothing.
claim = lambda n: n * n + n + 41
searched = [n for n in range(40) if not is_prime(claim(n))]
assert searched == [], "no counterexample below 40..."
assert not is_prime(claim(40)), "...and one at 40"
```

## 4. The mistake people actually make

**Reporting "no counterexample found" as "the claim is true".**

A search over `n = 0..39` of `n² + n + 41` finds forty primes and no
counterexample. The claim is false, and the smallest counterexample is one step
past where the search stopped.

That is not a contrived example. Search ranges are chosen for convenience, and
the interesting behaviour is frequently just outside them - because whatever
made the claim plausible is also what made the small cases work.

State the result honestly: "no counterexample in the range tested" is a
different and much weaker statement than "the claim holds". Both are useful; only
one of them licenses building on the claim.

The complementary error is searching only the easy region. Random positive
integers will never find a counterexample that requires a negative value, an
empty collection or a tie. Search the boundaries deliberately rather than hoping
a uniform sample lands on one.

---

## Check yourself

1. What is needed to disprove `∀x : P(x)`?
2. Disprove: 'for all sets A and B, `|A ∪ B| = |A| + |B|`'.
3. A search over a million inputs finds no counterexample. What have you established?

<details>
<summary>Answers</summary>

1. A single x with `¬P(x)`. The negation of a universal is an existential, so one witness is both necessary and sufficient.
2. Take `A = B = {1}`. Then `|A ∪ B| = 1` while `|A| + |B| = 2`. The identity holds only when the sets are disjoint.
3. That no counterexample exists in the region searched. The claim remains unproved: the counterexample may lie outside the range, or be too rare for the sampling used.

</details>

---

## Lesson checklist

- [ ] Learning objectives are concrete and checkable
- [ ] Worked example has no skipped arithmetic
- [ ] Code block runs as written and asserts
- [ ] The common-mistake section names a specific failure
- [ ] Self-check questions have answers

---

[← Previous](15_Strong_Induction.md) · [Module README](../README.md) · [Next →](17_Reading_a_Theorem_Statement_in_a_Paper.md)
