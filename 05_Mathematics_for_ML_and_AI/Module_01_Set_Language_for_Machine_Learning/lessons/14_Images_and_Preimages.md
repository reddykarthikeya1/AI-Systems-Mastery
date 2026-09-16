# Lesson 01.14 — Images and Preimages

> **Module 01:** Set Language for Machine Learning · Lesson 14 of 25

---

## What you will be able to do after this lesson

- [ ] Compute the image of a set and the preimage of a set under a given function.
- [ ] Explain why the preimage behaves better than the image under intersection, and use that when filtering.

## Prerequisites

- [Lesson 01.11](11_Functions_as_Special_Relations.md) - functions.

---

## 1. The idea

Two ways to push a *set* through a function `f : A → B`.

**Image.** For `S ⊆ A`, the image is what S maps to:

    f(S) = { f(x) : x ∈ S }     a subset of B

**Preimage.** For `T ⊆ B`, the preimage is everything that lands in T:

    f⁻¹(T) = { x ∈ A : f(x) ∈ T }     a subset of A

The notation `f⁻¹` here does **not** mean the inverse function. The preimage is
defined for every function, invertible or not - it is a set operation, and it
always makes sense.

The asymmetry between them is the useful part:

| | Image | Preimage |
| :--- | :--- | :--- |
| Union | `f(S ∪ S') = f(S) ∪ f(S')` | `f⁻¹(T ∪ T') = f⁻¹(T) ∪ f⁻¹(T')` |
| Intersection | `f(S ∩ S') ⊆ f(S) ∩ f(S')` only | `f⁻¹(T ∩ T') = f⁻¹(T) ∩ f⁻¹(T')` |
| Complement | no clean law | `f⁻¹(Tᶜ) = f⁻¹(T)ᶜ` |

**The preimage commutes with everything; the image does not.** That is why
filtering by a computed column behaves predictably: `WHERE f(x) IN T` is a
preimage, and combining such conditions with AND and OR does what you expect.

## 2. Worked example

`f : {1,2,3,4} → {0,1}` with `f(x) = x mod 2`.

**Images.** `f({1,2}) = {1, 0}`, `f({1,3}) = {1}`, `f({2,4}) = {0}`.

**Preimages.** `f⁻¹({0}) = {2, 4}` (the evens), `f⁻¹({1}) = {1, 3}`,
`f⁻¹({0,1}) = {1,2,3,4}` - the whole domain, and `f⁻¹(∅) = ∅`.

Now the failure of the image under intersection. Take `S = {1, 2}` and
`S' = {3, 4}`.

    S ∩ S' = ∅,          so  f(S ∩ S') = ∅
    f(S) = {1, 0},  f(S') = {1, 0},   so  f(S) ∩ f(S') = {0, 1}

So `f(S ∩ S') = ∅` is a *strict* subset of `{0,1}`. The two sets share no
elements, yet their images share both. Only `⊆` holds, and equality requires f
to be injective.

The preimage has no such problem: `f⁻¹({0} ∩ {1}) = f⁻¹(∅) = ∅`, and
`f⁻¹({0}) ∩ f⁻¹({1}) = {2,4} ∩ {1,3} = ∅` ✓.

## 3. Verify it in code

```python
A = {1, 2, 3, 4}
f = lambda x: x % 2

def image(fn, S):
    return {fn(x) for x in S}

def preimage(fn, T, domain):
    return {x for x in domain if fn(x) in T}

assert image(f, {1, 2}) == {0, 1}
assert image(f, {1, 3}) == {1}
assert preimage(f, {0}, A) == {2, 4}
assert preimage(f, {1}, A) == {1, 3}
assert preimage(f, {0, 1}, A) == A
assert preimage(f, set(), A) == set()

# Image only gives containment under intersection.
S, S2 = {1, 2}, {3, 4}
assert S & S2 == set()
assert image(f, S & S2) == set()
assert image(f, S) & image(f, S2) == {0, 1}
assert image(f, S & S2) < image(f, S) & image(f, S2), "strict subset"

# Preimage commutes with intersection, union and complement.
T, T2 = {0}, {1}
assert preimage(f, T & T2, A) == preimage(f, T, A) & preimage(f, T2, A)
assert preimage(f, T | T2, A) == preimage(f, T, A) | preimage(f, T2, A)
codomain = {0, 1}
assert preimage(f, codomain - T, A) == A - preimage(f, T, A)

# Image DOES commute with union, always.
assert image(f, S | S2) == image(f, S) | image(f, S2)
```

## 4. The mistake people actually make

**Assuming `f(S ∩ S') = f(S) ∩ f(S')` when deduplicating or joining.**

Concretely: you hash records to bucket them, then reason that two buckets
sharing a hash must contain overlapping records. They need not. Distinct
records collide into the same bucket, so the images overlap while the original
sets are disjoint.

This is the image failing under intersection, and it is the formal reason a
hash match must always be confirmed by comparing the originals - the same fact
that makes an unverified Rabin-Karp search report matches that are not there.

The direction of the error is fixed and worth remembering: `f(S ∩ S')` is a
*subset* of `f(S) ∩ f(S')`. So the intersection of images is an over-estimate -
it produces false positives, never false negatives. That is what makes it
usable as a cheap pre-filter, provided you verify afterwards.

Equality holds exactly when f is injective, which is precisely when no two
distinct inputs can collide.

---

## Check yourself

1. `f(x) = x²` on the integers. What is `f⁻¹({4})`?
2. Why is `f⁻¹` well defined even when f has no inverse function?
3. Give sets S, S' and a function where `f(S ∩ S')` is strictly smaller than `f(S) ∩ f(S')`.

<details>
<summary>Answers</summary>

1. `{2, -2}`. The preimage collects every input mapping into the set, and both square to 4.
2. Because the preimage is a set operation: it collects all inputs landing in the target set, and that collection always exists - it may be empty or contain many elements. An inverse *function* would have to return exactly one input, which is what fails.
3. `f(x) = x mod 2`, `S = {1,2}`, `S' = {3,4}`. The intersection of S and S' is empty so its image is empty, but both images are `{0,1}`, so the intersection of images is `{0,1}`.

</details>

---

## Lesson checklist

- [ ] Learning objectives are concrete and checkable
- [ ] Worked example has no skipped arithmetic
- [ ] Code block runs as written and asserts
- [ ] The common-mistake section names a specific failure
- [ ] Self-check questions have answers

---

[← Previous](13_Composition_and_Inverse_Functions.md) · [Module README](../README.md) · [Next →](15_Indexed_Families_and_Big_Unions.md)
