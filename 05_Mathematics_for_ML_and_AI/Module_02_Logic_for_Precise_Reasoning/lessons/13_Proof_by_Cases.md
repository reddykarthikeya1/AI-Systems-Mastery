# Lesson 02.13 — Proof by Cases

> **Module 02:** Logic for Precise Reasoning · Lesson 13 of 19

---

## What you will be able to do after this lesson

- [ ] Structure a proof by cases and verify the cases are exhaustive.
- [ ] Identify the failure mode of a case analysis that misses a case.

## Prerequisites

- [Lesson 02.10](10_Direct_Proof.md) - direct proof.

---

## 1. The idea

**Proof by cases** splits the domain into a finite number of situations, proves
the claim in each, and concludes it for all.

The obligation people forget is the first one: the cases must be **exhaustive**.
If they are, and each case is proved, the claim follows. They may overlap - that
costs only effort, not validity.

    S₁ ∪ S₂ ∪ ... ∪ Sₙ = D          (exhaustive - required)
    Sᵢ ∩ Sⱼ = ∅                      (disjoint - convenient, not required)

The natural split points are where a definition changes behaviour: the sign of a
number, whether an integer is even or odd, whether a matrix is singular, whether
a list is empty.

Exhaustiveness is a partition question - Module 01's material doing work again.
And it is the same obligation as a `match` statement needing a default branch, or
an `if/elif` chain needing a final `else`: a case analysis with no fallthrough is
a proof with a hole in it.

## 2. Worked example

**Claim.** For every real x, `|x| ≥ x`.

**Proof by cases** on the sign of x. The cases `x ≥ 0` and `x < 0` are
exhaustive, since every real satisfies exactly one.

- **Case 1: `x ≥ 0`.** Then `|x| = x`, so `|x| ≥ x` holds with equality.
- **Case 2: `x < 0`.** Then `|x| = -x`, which is positive, while x is negative.
  So `|x| > 0 > x`. ✓

Both cases hold and they cover ℝ, so the claim holds for all real x. ∎

**A claim where a case is easy to miss.** "For every integer n, `n² ≥ n`."

Split on `n ≤ 0` and `n ≥ 1`:

- `n ≤ 0`: `n²` is non-negative and n is non-positive, so `n² ≥ 0 ≥ n` ✓
- `n ≥ 1`: multiplying `n ≥ 1` by the positive n gives `n² ≥ n` ✓

Exhaustive over the integers, so the claim holds. But note it is **false over
the reals**: `n = 0.5` gives `0.25 < 0.5`. The integer case analysis is valid
precisely because there is no integer strictly between 0 and 1 - and that gap is
doing silent work.

## 3. Verify it in code

```python
# |x| >= x, both cases.
vals = [i / 4 for i in range(-40, 41)]
for x in vals:
    if x >= 0:
        assert abs(x) == x
    else:
        assert abs(x) == -x and abs(x) > x
assert all(abs(x) >= x for x in vals)

# n^2 >= n over the integers.
for n in range(-100, 101):
    assert n * n >= n
    if n <= 0:
        assert n * n >= 0 >= n
    else:
        assert n >= 1 and n * n >= n

# ...and the case analysis does NOT transfer to the reals.
assert 0.5 ** 2 < 0.5, "the missing region is 0 < x < 1"
assert not all(x * x >= x for x in vals)

# Exhaustiveness is a partition check.
def covered(x):
    return (x >= 0) or (x < 0)
assert all(covered(x) for x in vals)

# A case analysis with a gap: this misses 0 < n < 1 entirely.
def buggy_cases(x):
    if x <= 0:
        return True
    if x >= 1:
        return True
    return None                    # the uncovered region
assert buggy_cases(0.5) is None, "the gap is visible only if you look for it"
```

## 4. The mistake people actually make

**Case analysis with a gap nobody notices because the gap is empty in testing.**

Splitting on `x < 0` and `x > 0` omits `x = 0`. Over the integers tested in a
loop from -10 to 10 the omission is visible; over floats arising from a
computation, zero may simply never occur in the sample, and the proof - or the
code - looks complete.

The cost in code is an `if/elif` with no `else`, returning `None` implicitly.
That `None` then flows onward and fails somewhere unrelated, which is why the
bug is expensive to find rather than merely present.

The discipline: write the union of the cases and confirm it equals the domain
before proving anything. For a proof that is one line; for code it is a final
`else: raise`, which converts a silent gap into an immediate, located failure.

Overlap, by contrast, is harmless. Proving the claim twice for `x = 0` because
both cases include it wastes a line and endangers nothing.

---

## Check yourself

1. What is the one requirement on the cases in a proof by cases?
2. Prove `|xy| = |x||y|` by cases on the signs.
3. Why does the integer proof of `n² ≥ n` not extend to the reals?

<details>
<summary>Answers</summary>

1. They must be exhaustive - their union is the whole domain. Disjointness is convenient but not required; overlapping cases only duplicate work.
2. Four cases. Both non-negative: `|xy| = xy = |x||y|`. x ≥ 0, y < 0: `xy ≤ 0` so `|xy| = -xy = x(-y) = |x||y|`. Symmetrically for x < 0, y ≥ 0. Both negative: `xy > 0` so `|xy| = xy = (-x)(-y) = |x||y|`. The four cover every pair of signs.
3. It splits on `n ≤ 0` and `n ≥ 1`, which is exhaustive over the integers because none lie strictly between. Over the reals the interval `(0,1)` is uncovered, and the claim is false there - `0.5² = 0.25 < 0.5`.

</details>

---

## Lesson checklist

- [ ] Learning objectives are concrete and checkable
- [ ] Worked example has no skipped arithmetic
- [ ] Code block runs as written and asserts
- [ ] The common-mistake section names a specific failure
- [ ] Self-check questions have answers

---

[← Previous](12_Proof_by_Contradiction.md) · [Module README](../README.md) · [Next →](14_Mathematical_Induction.md)
