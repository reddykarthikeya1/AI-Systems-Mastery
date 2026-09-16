# Debug Lab 02 - Symptoms

> A rule engine that validates records against logical conditions. Each rule is almost right.
>
> It runs to completion, raises nothing, and **exits 0**. Every wrong number it
> prints is also plausible.
>
> Work from the output. Do **not** open `ANSWERS.md` until you have written a
> diagnosis for each symptom - the reasoning is the transferable skill, and
> reading the answer first skips exactly the part worth practising.

```bash
cd debug_lab
python broken_logic_checks.py
echo "exit=$?"
```

There are **3** sections below. Not all of them contain a defect; deciding
which are sound is part of the exercise.

---

## Section 1 - The De Morgan check disagrees with the definition

```
    negate_and(a, b)
      a=True  b=True  -> False
      a=True  b=False -> False
      a=False b=True  -> False
      a=False b=False -> True
    matches the definition on all four rows: False
```

The last line says the four rows do not all match. Find the row or rows that differ, and write down what the function returned versus what `not (a and b)` returns.

**Ask yourself:** when you push a negation through an `and`, what happens to the connective itself?

---

## Section 2 - Implication returns False when nothing was promised

```
    implies(p, q)
      a=True  b=True  -> True
      a=True  b=False -> False
      a=False b=True  -> False
      a=False b=False -> False
    checking the case where it does NOT rain:
      rain=False, wet=False -> False
    (a promise about rain says nothing about a dry day)
```

The rule is *if it rains, the ground is wet*. Today it did not rain and the ground is dry. The rule has not been broken - nothing was promised about dry days - yet the engine reports `False`.

**Ask yourself:** an implication is only *violated* in one of the four cases. Which one? And what should the other three return?

---

## Section 3 - 'All positive' accepts a list containing a negative

```
      all_positive([1, 2, 3]) -> True
      all_positive([1, -2, 3]) -> True
      all_positive([-1, -2, -3]) -> False
      all_positive([]) -> False
```

`[1, -2, 3]` is reported as all-positive. Look at the loop: it returns as soon as it finds a value it likes.

Note the empty list too. Whatever you think the answer should be, decide it deliberately - the convention is not arbitrary.

**Ask yourself:** which quantifier does this loop actually implement, and what does the correct one return the moment it finds a counterexample?

---
