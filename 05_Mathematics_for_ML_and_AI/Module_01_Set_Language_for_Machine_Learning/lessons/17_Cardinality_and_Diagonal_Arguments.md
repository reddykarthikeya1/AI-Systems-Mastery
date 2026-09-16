# Lesson 01.17 — Cardinality and Diagonal Arguments

> **Module 01:** Set Language for Machine Learning · Lesson 17 of 25

---

## What you will be able to do after this lesson

- [ ] Reproduce Cantor's diagonal argument and say precisely which step produces the contradiction.
- [ ] Recognise the same argument pattern when it appears as an impossibility result.

## Prerequisites

- [Lesson 01.16](16_Countable_versus_Uncountable_Sets.md) - countability.

---

## 1. The idea

**Cantor's theorem:** the interval `(0,1)` is uncountable. There is no listing
of the reals in it that reaches every one.

The proof is by contradiction and is worth knowing in full, because the pattern
recurs across computer science.

Suppose such a list exists: `r_1, r_2, r_3, ...`, each written as an infinite
decimal. Build a new number d by choosing its k-th digit to *differ* from the
k-th digit of `r_k`. Say: if the k-th digit of `r_k` is 5, use 4; otherwise
use 5.

Now ask where d appears in the list. It cannot be `r_1`, because it differs in
the first digit. It cannot be `r_2`, because it differs in the second. For every
k, `d ≠ r_k` because they differ at position k **by construction**.

So d is in (0,1) and not in the list. The list was assumed to contain every real
in (0,1). Contradiction - no such list exists.

The same **diagonalisation** proves the halting problem undecidable, proves
`|P(A)| > |A|` for every set, and underlies Gödel's incompleteness theorems. The
shape is always: assume an enumeration of all objects of a kind, construct an
object that differs from the n-th in the n-th place, observe it was omitted.

## 2. Worked example

Take a candidate list of four numbers and build the diagonal number.

    r_1 = 0.**1**234...
    r_2 = 0.5**6**78...
    r_3 = 0.11**1**1...
    r_4 = 0.999**9**...

The diagonal digits, in bold, are 1, 6, 1, 9. Apply the rule "5 if the digit is
not 5, else 4":

    d = 0.5555...

Check: `d ≠ r_1` since digit 1 is 5 and not 1 ✓. `d ≠ r_2` since digit 2 is 5
and not 6 ✓. `d ≠ r_3` at digit 3 ✓. `d ≠ r_4` at digit 4 ✓.

Extending the list changes nothing: whatever `r_5` is, d's fifth digit was
chosen to differ from it.

One technical point the argument must handle. Some reals have two decimal
expansions - `0.4999... = 0.5000...` - so "differs in a digit" does not
immediately give "is a different number". Restricting the constructed digits to
`{4, 5}`, as above, avoids every such pair, because the ambiguous expansions all
involve a trailing run of 0s or 9s.

## 3. Verify it in code

```python
def diagonal_digit(d):
    return 4 if d == 5 else 5

# Any finite list can be beaten.
listing = ["1234", "5678", "1111", "9999"]
d = "".join(str(diagonal_digit(int(row[k]))) for k, row in enumerate(listing))
assert d == "5555"

# d differs from EVERY listed number at its own index.
for k, row in enumerate(listing):
    assert d[k] != row[k], f"differs from r_{k+1} at position {k+1}"
assert d not in listing

# The construction works for any list, including a random one.
import random
random.seed(17)
for trial in range(50):
    rows = ["".join(random.choice("0123456789") for _ in range(30))
            for _ in range(30)]
    built = "".join(str(diagonal_digit(int(r[k]))) for k, r in enumerate(rows))
    assert all(built[k] != rows[k][k] for k in range(30))
    assert built not in rows

# Only digits 4 and 5 are used, so no 0.4999... = 0.5000... ambiguity arises.
assert set(d) <= {"4", "5"}

# The same argument gives |P(A)| > |A| for every finite A, and for all A.
from itertools import chain, combinations
A = set(range(5))
power = list(chain.from_iterable(combinations(A, n) for n in range(len(A) + 1)))
assert len(power) == 2 ** len(A) > len(A)
```

## 4. The mistake people actually make

**Thinking the argument fails because you could just add d to the list.**

This is the most common objection and it misreads the structure of the proof.
The claim being refuted is "*this* list contains every real in (0,1)".
Constructing d refutes it. Adding d produces a *different* list, and the
construction applies again to that one, producing a new number it also omits.

The proof is not a process you run; it is a demonstration that the assumption is
false for any list whatsoever. No repair is possible because the repair is
itself a list.

The second slip is believing uncountability means "very big". It is a
statement about *pairing*, not size in any everyday sense: ℚ is dense in ℝ -
between any two reals there is a rational - and ℚ is still countable. Density
and cardinality are unrelated.

---

## Check yourself

1. Where exactly does the diagonal argument produce its contradiction?
2. Why restrict the constructed digits to 4 and 5 rather than any digit?
3. Name another result proved by the same diagonalisation pattern.

<details>
<summary>Answers</summary>

1. At the assumption that the list is exhaustive. d is constructed to differ from the k-th entry at position k for every k, so it is in (0,1) and absent from a list that was assumed to contain everything in (0,1).
2. To avoid the dual-expansion problem: `0.4999... = 0.5000...`. Two numbers can differ digit-by-digit and still be equal if one ends in all 9s. Using only 4 and 5 never creates such a pair.
3. The undecidability of the halting problem, and Cantor's theorem that `|P(A)| > |A|` for every set. Both assume an enumeration and construct an object differing from the n-th in the n-th place.

</details>

---

## Lesson checklist

- [ ] Learning objectives are concrete and checkable
- [ ] Worked example has no skipped arithmetic
- [ ] Code block runs as written and asserts
- [ ] The common-mistake section names a specific failure
- [ ] Self-check questions have answers

---

[← Previous](16_Countable_versus_Uncountable_Sets.md) · [Module README](../README.md) · [Next →](18_Intervals_and_Regions_in_Rn.md)
