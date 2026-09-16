# Lesson 02.12 — Proof by Contradiction

> **Module 02:** Logic for Precise Reasoning · Lesson 12 of 19

---

## What you will be able to do after this lesson

- [ ] Structure a proof by contradiction and identify the contradiction reached.
- [ ] Say when contradiction is the right tool and when it is an unnecessary detour.

## Prerequisites

- [Lesson 02.11](11_Proof_by_Contrapositive.md) - contrapositive.

---

## 1. The idea

To prove a statement S by **contradiction**: assume `¬S`, derive something
impossible, and conclude that `¬S` is false - so S holds.

The structure:

1. Suppose, for contradiction, `¬S`.
2. Reason to a statement of the form `R ∧ ¬R`.
3. Therefore `¬S` is untenable, so S.

It is the natural tool for **non-existence** and **irrationality** claims -
statements where there is no object to construct and the only handle is what an
object would have to look like.

A caution that matters for clarity of writing: many proofs presented as
contradiction are really contrapositive proofs in disguise. If you assume `¬S`
and immediately derive `¬(hypothesis)` without using any other machinery, you
proved the contrapositive and wrapped it in unnecessary framing. The direct or
contrapositive version is shorter and easier to check.

Use contradiction when the impossibility is genuinely global - "this number
would have to be both even and odd", "this set would have to be both finite and
infinite" - not merely the negation of an assumption you started with.

## 2. Worked example

**Claim.** `√2` is irrational.

**Proof.** Suppose not: `√2 = a/b` for integers a, b with `b ≠ 0`, in lowest
terms - so a and b share no common factor.

Squaring: `2 = a²/b²`, hence `a² = 2b²`. So `a²` is even, and by Lesson 02.11,
a is even. Write `a = 2k`.

Substituting: `(2k)² = 2b²`, so `4k² = 2b²`, so `b² = 2k²`. Then `b²` is even,
so b is even.

But now a and b are both even, contradicting that the fraction was in lowest
terms. The assumption fails, so `√2` is irrational. ∎

Notice where the contradiction lives: not in the algebra, which is fine
throughout, but in the collision with "lowest terms" - a condition we were free
to impose at the start and which the derivation then violated.

**Claim.** There are infinitely many primes.

**Proof.** Suppose there are finitely many: `p₁, ..., pₙ`. Let
`N = p₁p₂...pₙ + 1`. N leaves remainder 1 on division by each `pᵢ`, so no `pᵢ`
divides it. But every integer greater than 1 has a prime factor, so N has one,
and it is not in our list - contradicting that the list was all of them. ∎

## 3. Verify it in code

```python
from math import gcd, isqrt

# sqrt(2) is irrational: no fraction in lowest terms squares to 2.
found = None
for b in range(1, 2000):
    for a in range(1, 2 * b + 1):
        if gcd(a, b) == 1 and a * a == 2 * b * b:
            found = (a, b)
assert found is None, "no reduced fraction squares to exactly 2"

# The step the proof turns on: a^2 even implies a even.
for a in range(1, 500):
    if (a * a) % 2 == 0:
        assert a % 2 == 0

# Euclid's construction, checked concretely.
def primes_up_to(n):
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, isqrt(n) + 1):
        if sieve[i]:
            for j in range(i * i, n + 1, i):
                sieve[j] = False
    return [i for i, ok in enumerate(sieve) if ok]

for k in range(1, 8):
    listed = primes_up_to(50)[:k]
    N = 1
    for p in listed:
        N *= p
    N += 1
    assert all(N % p == 1 for p in listed), "N leaves remainder 1 on each"
    assert all(N % p != 0 for p in listed), "so none of them divides N"
    # N therefore has a prime factor outside the list.
    factor = next(p for p in primes_up_to(N) if N % p == 0)
    assert factor not in listed
```

## 4. The mistake people actually make

**Dressing a direct proof as a contradiction.**

"Suppose n is even and, for contradiction, `n²` is odd. But `n = 2k` gives
`n² = 4k²`, which is even. Contradiction." The contradiction adds nothing: the
argument computed `n²` from n and found it even, which is a direct proof.

The cost is not correctness but reviewability. A reader of a contradiction proof
must hold `¬S` in mind throughout and check that every step is legitimate under
a false assumption. If the assumption was never used, that effort was wasted and
the reader may miss a real gap elsewhere.

The test: after finishing, check whether the assumption `¬S` appeared anywhere
in the derivation. If it did not, delete it and you have a direct proof.

The second error is stopping at a *surprising* conclusion rather than an
impossible one. "This would mean the model has 4.7 layers" is odd; it is a
contradiction only once you have stated that layer counts are integers. The
contradiction must be `R ∧ ¬R` for an explicitly established R.

---

## Check yourself

1. What is the contradiction in the `√2` proof?
2. When is contradiction the right tool rather than a direct proof?
3. How can you tell a contradiction proof is really a direct proof in disguise?

<details>
<summary>Answers</summary>

1. That a and b are both even, which contradicts the assumption that `a/b` was in lowest terms. The algebra itself is consistent throughout.
2. For non-existence and irrationality claims, where there is no object to construct and the only available handle is what a hypothetical object would have to satisfy.
3. Check whether the assumption `¬S` was used anywhere in the derivation. If the argument only ever reasons forward from the hypothesis, the assumption is decorative and can be deleted.

</details>

---

## Lesson checklist

- [ ] Learning objectives are concrete and checkable
- [ ] Worked example has no skipped arithmetic
- [ ] Code block runs as written and asserts
- [ ] The common-mistake section names a specific failure
- [ ] Self-check questions have answers

---

[← Previous](11_Proof_by_Contrapositive.md) · [Module README](../README.md) · [Next →](13_Proof_by_Cases.md)
