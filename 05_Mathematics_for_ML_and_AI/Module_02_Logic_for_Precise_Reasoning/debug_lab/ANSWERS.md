# Debug Lab 02 - Answers

Read only after writing your own diagnosis for every section.

---

## Defect 1 - De Morgan's law applied without flipping the connective

**Where:** `negate_and`.

```python
return (not a) and (not b)      # this is not (a or b)
```

De Morgan's law is:

    not (a and b)  ==  (not a) or (not b)
    not (a or b)   ==  (not a) and (not b)

The negation distributes over the operands **and flips the connective**. The
code distributes the negation and leaves the `and` alone, so it computes
`not (a or b)` instead.

The two agree on three of the four rows, which is exactly why it survives a
quick test: they differ only when one operand is true and the other false.

**The fix.**

```python
return (not a) or (not b)
```

**The general lesson.** "Distribute the negation" is a half-remembered rule.
The connective flips. When you are unsure, write the four-row table - it takes
thirty seconds and is not a matter of opinion.

---

## Defect 2 - implication implemented as conjunction

**Where:** `implies`.

```python
return p and q
```

An implication `p -> q` is false in exactly one case: `p` true and `q` false.
A promise is broken only when its condition was met and its consequence did not
follow. It is **vacuously true** whenever `p` is false, because nothing was
promised.

| p | q | `p and q` | `p -> q` |
| :--- | :--- | :--- | :--- |
| T | T | T | T |
| T | F | F | F |
| F | T | F | **T** |
| F | F | F | **T** |

**The fix.**

```python
return (not p) or q
```

**The general lesson.** Vacuous truth feels wrong the first time and is
load-bearing. "Every element of the empty set satisfies P" is true, and every
proof by induction and every `all([])` depends on it. If your validation logic
reports a violation when the precondition never held, this is the bug.

---

## Defect 3 - "for all" implemented as "there exists"

**Where:** `all_positive`.

```python
for value in values:
    if value > 0:
        return True     # returns on the first value that PASSES
return False
```

This returns True as soon as it finds one positive value - that is
`any(v > 0 for v in values)`, the existential quantifier.

A universal quantifier does the opposite: it returns False on the first
**counterexample**, and True only if it gets all the way through.

**The fix.**

```python
for value in values:
    if value <= 0:
        return False
return True
```

or simply `return all(v > 0 for v in values)`.

Note what the corrected version does with `[]`: it returns True. That is
vacuous truth again, and it is the same convention Python's built-in `all([])`
uses. The broken version returns False for the empty list - which happens to
look reasonable, and is inconsistent with everything else.

**The general lesson.** The shape of the loop tells you which quantifier you
wrote. Early-return-on-success is "there exists"; early-return-on-failure is
"for all". Getting this backwards passes any test whose lists are all-good or
all-bad, and fails on the mixed case that matters.
