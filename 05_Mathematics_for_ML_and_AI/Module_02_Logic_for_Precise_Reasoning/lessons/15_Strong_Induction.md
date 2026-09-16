# Lesson 02.15 — Strong Induction

> **Module 02:** Logic for Precise Reasoning · Lesson 15 of 19

---

## What you will be able to do after this lesson

- [ ] Apply strong induction and say how its hypothesis differs from ordinary induction.
- [ ] Recognise a claim where ordinary induction is insufficient.

## Prerequisites

- [Lesson 02.14](14_Mathematical_Induction.md) - ordinary induction.

---

## 1. The idea

**Strong induction** assumes the statement for *all* values below `k+1`, not
just for k:

    ordinary: P(k) → P(k+1)
    strong:   (P(n₀) ∧ ... ∧ P(k)) → P(k+1)

The two are equivalent in power - each can simulate the other - but strong
induction is the natural fit whenever `P(k+1)` depends on a value further back
than k, or on a value you cannot predict in advance.

The tell: your argument decomposes the case `k+1` into *two smaller pieces of
unknown size*. Factorisation splits n into `a·b` with both smaller than n but
neither necessarily `n-1`. A divide-and-conquer recurrence splits into halves.
Ordinary induction hands you only `P(k)`, which is not enough.

Strong induction often needs **no separate base case** beyond the smallest
value, because the implication `(everything below) → P(k+1)` is vacuously
available at the bottom. That is elegant and a trap: it makes it easy to forget
to check the smallest case at all, and the smallest case is where arguments
about "splitting into smaller parts" break down.

## 2. Worked example

**Claim.** Every integer `n ≥ 2` has a prime factorisation.

**Proof by strong induction.** Let `n ≥ 2` and assume every integer m with
`2 ≤ m < n` has a prime factorisation.

Two cases, exhaustive:

- **n is prime.** Then n is its own factorisation. ✓
- **n is composite.** Then `n = a·b` with `2 ≤ a, b < n`. Both a and b are
  strictly below n, so the inductive hypothesis applies to each and gives
  factorisations of both. Concatenating them factorises n. ✓

Base case `n = 2`: 2 is prime, handled by the first case. ∎

Ordinary induction cannot do this. Knowing `P(n-1)` says nothing useful about n:
the factors a and b are generally nowhere near `n-1`. The hypothesis must cover
everything below.

**A second.** Every amount of postage `n ≥ 8` can be made from 3p and 5p stamps.
Base cases 8 = 3+5, 9 = 3+3+3, 10 = 5+5. Step for `n ≥ 11`: since `n-3 ≥ 8`, the
hypothesis gives a way to make `n-3`; add one 3p stamp. This needs `P(n-3)`, not
`P(n-1)` - so three base cases are required, and checking only one would leave
a gap.

## 3. Verify it in code

```python
from math import isqrt

def factorise(n):
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors

def is_prime(n):
    return n >= 2 and all(n % d for d in range(2, isqrt(n) + 1))

for n in range(2, 2000):
    fs = factorise(n)
    assert all(is_prime(f) for f in fs), "every factor is prime"
    product = 1
    for f in fs:
        product *= f
    assert product == n

# The composite case really does split into two strictly smaller pieces.
for n in range(4, 500):
    if not is_prime(n):
        a = next(d for d in range(2, n) if n % d == 0)
        b = n // a
        assert 2 <= a < n and 2 <= b < n

# Postage: needs P(n-3), so THREE base cases.
def makeable(n, memo={8: True, 9: True, 10: True}):
    if n in memo:
        return memo[n]
    if n < 8:
        return False
    memo[n] = makeable(n - 3)
    return memo[n]

assert all(makeable(n) for n in (8, 9, 10)), "base cases"
assert all(makeable(n) for n in range(8, 200))
assert not makeable(7), "and 7 genuinely cannot be made"
```

## 4. The mistake people actually make

**Using one base case when the step reaches back further than one.**

If the inductive step derives `P(n)` from `P(n-3)`, you need base cases for
`n₀`, `n₀+1` and `n₀+2` - because the chain from a single base only reaches
every third value. Prove only `P(8)` and the argument establishes 8, 11, 14, ...
and says nothing about 9 or 10.

The rule: **the number of base cases must match the depth the step reaches
back.** A step using `P(n-1)` and `P(n-2)` - as in the Fibonacci recurrence -
needs two.

This is the same obligation as a recursive function needing a base case for
every branch that can terminate. A `fib(n)` recursing on `n-1` and `n-2` with a
guard only for `n == 0` recurses forever on odd inputs, which is the programming
version of the identical gap.

---

## Check yourself

1. How does the strong inductive hypothesis differ from the ordinary one?
2. Why can ordinary induction not prove that every n ≥ 2 has a prime factorisation?
3. A step derives `P(n)` from `P(n-2)`. How many base cases are needed?

<details>
<summary>Answers</summary>

1. Ordinary assumes `P(k)` alone; strong assumes `P(m)` for every m from the base up to k. Strong is the natural choice when the step decomposes into pieces whose size you do not control.
2. The step factors n as `a·b` where a and b are smaller than n but generally not equal to `n-1`. The hypothesis `P(n-1)` says nothing about them; you need the hypothesis to cover all smaller values.
3. Two - for `n₀` and `n₀+1`. A single base case would only reach every other value, leaving the opposite parity unproved.

</details>

---

## Lesson checklist

- [ ] Learning objectives are concrete and checkable
- [ ] Worked example has no skipped arithmetic
- [ ] Code block runs as written and asserts
- [ ] The common-mistake section names a specific failure
- [ ] Self-check questions have answers

---

[← Previous](14_Mathematical_Induction.md) · [Module README](../README.md) · [Next →](16_Counterexamples_and_Disproof.md)
