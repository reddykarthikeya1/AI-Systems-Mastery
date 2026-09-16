# Lesson 02.11 — Proof by Contrapositive

> **Module 02:** Logic for Precise Reasoning · Lesson 11 of 19

---

## What you will be able to do after this lesson

- [ ] Prove a statement by proving its contrapositive, and say when that is the easier route.
- [ ] Recognise the signal in a claim that makes contraposition worth trying.

## Prerequisites

- [Lesson 02.04](04_Converse_Inverse_and_Contrapositive.md) - contrapositive.

---

## 1. The idea

Since `p → q` is equivalent to `¬q → ¬p`, proving the second proves the first.

When it helps: when the **negation of the conclusion is more concrete than the
hypothesis**. The signal to look for is a conclusion containing *not*,
*irrational*, *not divisible*, *distinct* - anything whose negation gives you
something to work with.

Compare. To show directly that `n² even → n even`, you start from "n² is even",
so `n² = 2k`, and now you need to extract information about n from a statement
about its square - which requires a detour through prime factorisation.

Contrapositive: show `n odd → n² odd`. Now you start from `n = 2j + 1`, which is
an explicit handle, and the algebra is immediate.

The proofs are equally valid. One is three lines and the other is not, and the
difference is entirely which end you start from.

## 2. Worked example

**Claim.** For every integer n, if `n²` is even then n is even.

**Proof by contrapositive.** We prove: if n is odd then `n²` is odd.

Let n be an arbitrary odd integer, so `n = 2j + 1` for some integer j. Then

    n² = (2j + 1)² = 4j² + 4j + 1 = 2(2j² + 2j) + 1

Since `2j² + 2j` is an integer, `n²` is 2 times an integer plus 1, hence odd.

We have shown `n odd → n² odd`, which is the contrapositive of the claim, so the
claim holds. ∎

**A second.** If `x + y ≥ 10` then `x ≥ 5` or `y ≥ 5`.

Contrapositive: if `x < 5` and `y < 5` then `x + y < 10`. (Note De Morgan turned
the "or" into an "and" when negated.) That is immediate: adding two numbers each
below 5 gives a sum below 10. ∎

The direct version would require case analysis on which of x, y is larger. The
contrapositive has no cases at all.

## 3. Verify it in code

```python
# The contrapositive we actually proved.
for j in range(-200, 201):
    n = 2 * j + 1
    assert n % 2 == 1
    assert (n * n) % 2 == 1, "odd squared is odd"

# Which gives the original claim.
for n in range(-200, 201):
    if (n * n) % 2 == 0:
        assert n % 2 == 0, "n^2 even implies n even"

# The algebraic identity the proof used.
j = 7
n = 2 * j + 1
assert n * n == 2 * (2 * j * j + 2 * j) + 1

# Second claim, via its contrapositive.
def claim(x, y):
    return (not (x + y >= 10)) or (x >= 5 or y >= 5)

def contrapositive(x, y):
    return (not (x < 5 and y < 5)) or (x + y < 10)

vals = [i / 2 for i in range(-10, 40)]
assert all(claim(x, y) for x in vals for y in vals)
assert all(contrapositive(x, y) for x in vals for y in vals)

# De Morgan is what turns the "or" conclusion into an "and" hypothesis.
assert all((not (a or b)) == ((not a) and (not b))
           for a in (True, False) for b in (True, False))
```

## 4. The mistake people actually make

**Proving the converse and believing you proved the contrapositive.**

For `p → q`, the contrapositive is `¬q → ¬p`. The converse is `q → p`. They are
different statements and only the first is equivalent.

Concretely, for "if `n²` is even then n is even":

- contrapositive: if n is odd then `n²` is odd ✓ proves the claim
- converse: if n is even then `n²` is even ✓ true, and proves nothing about the
  original

Both are true here, which is what makes the error invisible: you prove
something true, and it is the wrong true thing. The claim you were asked about
remains unproved.

The check is mechanical. Write down p and q explicitly, then write `¬q → ¬p`
and confirm that is what your proof establishes. If your proof starts by
assuming p, it is not a proof by contrapositive.

---

## Check yourself

1. Give the contrapositive of 'if a function is differentiable, it is continuous'.
2. When is contraposition the easier route?
3. Why is proving 'n even → n² even' not a proof that 'n² even → n even'?

<details>
<summary>Answers</summary>

1. 'If a function is not continuous, it is not differentiable.' Equivalent to the original, and often the more useful direction in practice.
2. When negating the conclusion gives you a concrete object to work with and the hypothesis does not. 'n is odd' hands you `n = 2j+1`; 'n² is even' hands you a fact about the square that needs unpacking.
3. That is the converse, not the contrapositive. The contrapositive is 'n odd → n² odd'. The converse is a separate statement that happens to also be true, and proving it leaves the original unestablished.

</details>

---

## Lesson checklist

- [ ] Learning objectives are concrete and checkable
- [ ] Worked example has no skipped arithmetic
- [ ] Code block runs as written and asserts
- [ ] The common-mistake section names a specific failure
- [ ] Self-check questions have answers

---

[← Previous](10_Direct_Proof.md) · [Module README](../README.md) · [Next →](12_Proof_by_Contradiction.md)
