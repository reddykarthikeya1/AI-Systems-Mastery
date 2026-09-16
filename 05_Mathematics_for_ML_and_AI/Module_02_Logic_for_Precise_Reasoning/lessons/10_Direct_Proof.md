# Lesson 02.10 — Direct Proof

> **Module 02:** Logic for Precise Reasoning · Lesson 10 of 19

---

## What you will be able to do after this lesson

- [ ] Write a direct proof of a simple universal implication.
- [ ] Say what a proof establishes that any number of tested cases does not.

## Prerequisites

- [Lesson 02.03](03_Implication_and_Its_Traps.md) - implication.

---

## 1. The idea

A **direct proof** of `∀x : (P(x) → Q(x))` has a fixed shape:

1. Take an arbitrary x satisfying P(x). *Arbitrary* is the load-bearing word:
   you may use only what P(x) gives you, nothing about a specific x.
2. Derive Q(x) by a chain of steps, each justified by a definition or an
   established result.
3. Conclude that the implication holds for every x, since x was arbitrary.

Step 1 is where proofs go wrong. If you assume x is positive, or an integer, or
non-zero, you have proved something narrower than you claimed - and the gap is
usually exactly where the interesting counterexample lives.

**What a proof buys over testing.** Tests check finitely many cases; a proof
covers all of them, including the ones nobody thought to generate. For an
infinite domain there is no amount of testing that substitutes.

This is not an argument against tests. Tests catch errors in *your
implementation*; proofs establish properties of *the mathematics*. The
implementation can be wrong while the theorem is right, which is why the code
blocks in these lessons assert on concrete values even when the statement is
proved.

## 2. Worked example

**Claim.** For all integers m and n, if m and n are both even, then `m + n` is
even.

**Proof.** Let m and n be arbitrary integers, and suppose both are even.

By the definition of even, there are integers j and k with `m = 2j` and
`n = 2k`. Then

    m + n = 2j + 2k = 2(j + k)

Since j and k are integers, `j + k` is an integer, so `m + n` is 2 times an
integer - that is, even. Since m and n were arbitrary, the claim holds for all
such pairs. ∎

Note what was used: only the definition of even and closure of the integers
under addition. Nothing about the size or sign of m and n, which is what makes
the argument cover every case.

A second: if `x > 2` then `x² > 4`. Suppose `x > 2`. Since `x > 2 > 0`,
multiplying both sides of `x > 2` by the positive number x preserves the
inequality: `x² > 2x`. And `2x > 4` because `x > 2`. Chaining, `x² > 4`. ∎

The positivity of x is used, and it follows from the hypothesis - it was not
assumed extra.

## 3. Verify it in code

```python
# The proof covers all integers; the test checks that our reading is right.
def even(n):
    return n % 2 == 0

for m in range(-50, 51):
    for n in range(-50, 51):
        if even(m) and even(n):
            assert even(m + n)

# The witness structure the proof used: m + n = 2(j + k).
m, n = 14, -8
j, k = m // 2, n // 2
assert m == 2 * j and n == 2 * k
assert m + n == 2 * (j + k)
assert even(m + n)

# Second claim: x > 2 implies x^2 > 4.
for x in [2.0001, 3, 10, 1e6]:
    assert x > 2 and x * x > 4

# The hypothesis is needed: without x > 2 the conclusion can fail.
assert (-3) ** 2 > 4 and not (-3 > 2), "conclusion can hold without the hypothesis"
assert 1.5 ** 2 < 4, "and fails when the hypothesis fails"

# Testing is finite; the proof is not. This loop proves nothing about 10**9.
tested = [(m, n) for m in range(-50, 51) for n in range(-50, 51)]
assert len(tested) == 101 * 101
assert even(10 ** 9 + 10 ** 9), "covered by the proof, not by the loop above"
```

## 4. The mistake people actually make

**Assuming more about the arbitrary object than the hypothesis provides.**

A proof that "for all real x, `√(x²) = x`" runs: let x be arbitrary, then
`√(x²) = x` because squaring and square-rooting undo each other. That silently
assumes `x ≥ 0`. For `x = -3` the left side is 3 and the right is -3, so the
claim is false and the correct statement is `√(x²) = |x|`.

The error is not in the algebra; it is in step 1, where an unstated assumption
entered.

The check: after writing a proof, list every property of x you used and confirm
each follows from the hypothesis. If one does not, either add it to the
hypothesis - narrowing the claim - or find the counterexample it was hiding.

In ML the same pattern appears as a derivation that assumes a matrix is
invertible, a distribution has finite variance, or a function is differentiable
everywhere. Each is a real assumption, and each is violated by cases that turn
up in practice.

---

## Check yourself

1. What makes the object in a direct proof 'arbitrary', and why does it matter?
2. Prove: if n is odd then n² is odd.
3. Why does testing a claim on a million random inputs not establish it?

<details>
<summary>Answers</summary>

1. That the argument uses only properties guaranteed by the hypothesis. It matters because that is what licenses the conclusion for *every* such object rather than for the particular one you pictured.
2. Let n be arbitrary and odd, so `n = 2k + 1` for some integer k. Then `n² = 4k² + 4k + 1 = 2(2k² + 2k) + 1`, which is 2 times an integer plus 1, hence odd. ∎
3. The domain is typically infinite, so any finite sample leaves cases unchecked - and counterexamples are often rare or structured, so random sampling is unlikely to find them. A proof covers every case at once.

</details>

---

## Lesson checklist

- [ ] Learning objectives are concrete and checkable
- [ ] Worked example has no skipped arithmetic
- [ ] Code block runs as written and asserts
- [ ] The common-mistake section names a specific failure
- [ ] Self-check questions have answers

---

[← Previous](09_Negating_Quantified_Statements.md) · [Module README](../README.md) · [Next →](11_Proof_by_Contrapositive.md)
