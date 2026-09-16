# Lesson 02.14 — Mathematical Induction

> **Module 02:** Logic for Precise Reasoning · Lesson 14 of 19

---

## What you will be able to do after this lesson

- [ ] Write a proof by induction with an explicit base case and inductive step.
- [ ] Identify where an induction proof breaks when the base case or the step fails.

## Prerequisites

- [Lesson 02.10](10_Direct_Proof.md) - direct proof.

---

## 1. The idea

To prove `P(n)` for all integers `n ≥ n₀`:

1. **Base case.** Prove `P(n₀)`.
2. **Inductive step.** Prove `P(k) → P(k+1)` for an arbitrary `k ≥ n₀`.

Then `P(n)` holds for every `n ≥ n₀`. The picture is a line of dominoes: the base
case topples the first, the step guarantees each topples the next.

Both parts are load-bearing and they fail differently:

- **No base case:** the step may be perfectly valid and nothing ever starts.
  "All horses are the same colour" has a correct-looking step and a broken base.
- **Step fails at one k:** everything past that k is unproved, even though the
  base and most steps are fine.

The inductive hypothesis `P(k)` is an *assumption about an arbitrary k*, not a
circular assumption of what you are proving. You are proving an implication, and
assuming its antecedent is exactly how implications are proved.

Induction is how you reason about recursion, loops with invariants, and anything
defined by a recurrence - which is most algorithm analysis.

## 2. Worked example

**Claim.** For all `n ≥ 1`: `1 + 2 + ... + n = n(n+1)/2`.

**Base case, n = 1.** Left side is 1. Right side is `1·2/2 = 1`. ✓

**Inductive step.** Assume the formula holds for some `k ≥ 1`:

    1 + 2 + ... + k = k(k+1)/2

Add `k+1` to both sides:

    1 + ... + k + (k+1) = k(k+1)/2 + (k+1)
                        = (k+1) · (k/2 + 1)
                        = (k+1)(k+2)/2

which is the formula with `k+1` in place of k. ✓

Base and step both hold, so the formula holds for every `n ≥ 1`. ∎

**Where a broken base case hides.** Consider "`P(n)`: `n = n + 1`". The step is
valid - assuming `k = k + 1` and adding 1 to both sides gives `k+1 = k+2` - and
the statement is false for every n, because no base case holds. A step that
works proves nothing on its own.

## 3. Verify it in code

```python
def formula(n):
    return n * (n + 1) // 2

# Base case.
assert sum(range(1, 2)) == formula(1) == 1

# The inductive step, as an identity: formula(k) + (k+1) == formula(k+1).
for k in range(1, 500):
    assert formula(k) + (k + 1) == formula(k + 1)

# Together these give the claim; spot-check it directly.
for n in range(1, 300):
    assert sum(range(1, n + 1)) == formula(n)

# A valid-looking step with no base case proves nothing.
# P(n): n == n + 1.  Step: assume k == k+1, then k+1 == k+2.
k = 5
step_is_valid = (k == k + 1) <= (k + 1 == k + 2)   # False implies anything
assert step_is_valid, "the implication holds vacuously"
assert not (1 == 2), "and the statement is false for every n"

# A second induction: 2^n > n for all n >= 1.
assert 2 ** 1 > 1
for k in range(1, 40):
    assert 2 ** k > k
    assert 2 ** (k + 1) == 2 * (2 ** k) > 2 * k >= k + 1
```

## 4. The mistake people actually make

**Omitting the base case because the inductive step looks convincing.**

The classic illustration is "all horses are the same colour". The step argues
that in any group of `k+1` horses, removing one leaves k of the same colour,
removing a different one leaves k of the same colour, and the overlap forces all
`k+1` to match. The step is wrong precisely at `k = 1`, where the two subgroups
of size 1 do not overlap - and the failure is invisible unless you check the
small case.

The lesson generalises: **check the step at the smallest k, not a typical one.**
Arguments that manipulate "the rest of the elements" often assume there are some,
and at the boundary there are none.

In algorithm analysis the same error appears as a recurrence solved without
checking the base: `T(n) = 2T(n/2) + n` gives `O(n log n)` for `n ≥ 2`, and says
nothing about `T(1)`, which is where the recursion actually terminates and where
an off-by-one in the base case changes the constant or loops forever.

---

## Check yourself

1. What are the two obligations in a proof by induction?
2. Why is assuming `P(k)` not circular?
3. Prove by induction that `2ⁿ > n` for all `n ≥ 1`.

<details>
<summary>Answers</summary>

1. Prove the base case `P(n₀)`, and prove the implication `P(k) → P(k+1)` for arbitrary `k ≥ n₀`. Both are required; either alone proves nothing.
2. Because the goal of the step is the implication `P(k) → P(k+1)`, and the standard way to prove an implication is to assume its antecedent. You are not assuming the conclusion you ultimately want.
3. Base: `2¹ = 2 > 1` ✓. Step: assume `2ᵏ > k`. Then `2^(k+1) = 2·2ᵏ > 2k = k + k ≥ k + 1` since `k ≥ 1`. ∎

</details>

---

## Lesson checklist

- [ ] Learning objectives are concrete and checkable
- [ ] Worked example has no skipped arithmetic
- [ ] Code block runs as written and asserts
- [ ] The common-mistake section names a specific failure
- [ ] Self-check questions have answers

---

[← Previous](13_Proof_by_Cases.md) · [Module README](../README.md) · [Next →](15_Strong_Induction.md)
