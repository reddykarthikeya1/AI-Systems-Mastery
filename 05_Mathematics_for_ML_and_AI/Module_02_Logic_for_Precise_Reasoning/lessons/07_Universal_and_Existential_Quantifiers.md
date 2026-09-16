# Lesson 02.07 — Universal and Existential Quantifiers

> **Module 02:** Logic for Precise Reasoning · Lesson 7 of 19

---

## What you will be able to do after this lesson

- [ ] Translate an English claim into `∀` and `∃` notation with the correct domain.
- [ ] Explain why `∀` over an empty domain is true and `∃` is false.

## Prerequisites

- [Lesson 02.03](03_Implication_and_Its_Traps.md) - implication and vacuous truth.

---

## 1. The idea

A **predicate** `P(x)` becomes a proposition once x is bound - by a value, or by
a quantifier.

    ∀x ∈ D : P(x)      for every x in D, P(x) holds
    ∃x ∈ D : P(x)      there is at least one x in D with P(x)

The **domain** D is part of the statement. "All models overfit" is meaningless
until you say all models *of what kind*, and changing the domain changes the
truth value.

How each is settled:

| | Proved by | Refuted by |
| :--- | :--- | :--- |
| `∀x : P(x)` | an argument covering every x | **one** counterexample |
| `∃x : P(x)` | **one** witness | an argument covering every x |

The asymmetry is the practical content: a universal claim is cheap to refute and
expensive to establish; an existential is the reverse.

Over an **empty domain**, `∀` is true (no x can violate it) and `∃` is false (no
x can witness it). Python agrees: `all([])` is True, `any([])` is False. This is
the vacuous truth of Lesson 02.03 wearing quantifier notation.

## 2. Worked example

Domain: the models in a registry. `A(m)` = "m has accuracy above 0.9".

    ∀m : A(m)     every model is above 0.9
    ∃m : A(m)     at least one is
    ¬∃m : A(m)    none is
    ∃m : ¬A(m)    at least one is not

Take a registry of three models with accuracies 0.95, 0.88, 0.93.

- `∀m : A(m)` is **false** - the model at 0.88 is a counterexample, and one is
  enough.
- `∃m : A(m)` is **true** - 0.95 witnesses it, and one is enough.

Now empty the registry. `∀m : A(m)` becomes **true** - there is no model to
violate it - and `∃m : A(m)` becomes **false**. A dashboard reporting "all
models meet the accuracy bar" when the registry is empty is stating something
true and useless.

Loop shapes follow directly: return `False` on the first counterexample for
`∀`, return `True` on the first witness for `∃`.

## 3. Verify it in code

```python
accuracies = [0.95, 0.88, 0.93]
above = lambda a: a > 0.9

assert all(above(a) for a in accuracies) is False
assert any(above(a) for a in accuracies) is True

# One counterexample refutes a universal; one witness establishes an existential.
counterexample = next(a for a in accuracies if not above(a))
assert counterexample == 0.88
witness = next(a for a in accuracies if above(a))
assert witness == 0.95

# The empty domain.
assert all(above(a) for a in []) is True, "nothing can violate it"
assert any(above(a) for a in []) is False, "nothing can witness it"

# The loop shapes differ: forall exits on failure, exists exits on success.
def for_all(values, predicate):
    for v in values:
        if not predicate(v):
            return False
    return True

def there_exists(values, predicate):
    for v in values:
        if predicate(v):
            return True
    return False

assert for_all(accuracies, above) is False
assert there_exists(accuracies, above) is True
assert for_all([], above) is True and there_exists([], above) is False

# The domain is part of the claim: restrict it and the answer changes.
production = [0.95, 0.93]
assert for_all(production, above) is True
```

## 4. The mistake people actually make

**Writing "for all" with the loop shape of "there exists".**

```python
for value in values:
    if predicate(value):
        return True      # this is "there exists"
return False
```

Returning `True` on the first *success* implements the existential. A universal
returns `False` on the first *failure*. The two agree whenever the collection is
uniform - all passing or all failing - which is exactly what hand-written test
data looks like, so the bug survives.

The second error is leaving the domain implicit. "All our models are calibrated"
means something different for the production registry than for every
experimental checkpoint, and the claim is often made about one while the
evidence was gathered on the other. Naming the domain forces the question.

And do not let the empty case pass silently. "All zero rows passed validation"
is true; whether it should count as success is a decision you have to make, and
the quantifier will not make it for you.

---

## Check yourself

1. Translate 'some layer has no parameters' into quantifier notation.
2. What is `∀x ∈ ∅ : P(x)` and `∃x ∈ ∅ : P(x)`?
3. Why do a correct `∀` loop and an incorrect one that returns True on the first success often agree in tests?

<details>
<summary>Answers</summary>

1. `∃l ∈ layers : count(l) = 0`. It is established by exhibiting one such layer.
2. True and false respectively. Nothing can violate the universal, and nothing can witness the existential.
3. They differ only on mixed collections. Test data that is entirely passing or entirely failing gives the same answer under both, so the mistake only appears on realistic mixed input.

</details>

---

## Lesson checklist

- [ ] Learning objectives are concrete and checkable
- [ ] Worked example has no skipped arithmetic
- [ ] Code block runs as written and asserts
- [ ] The common-mistake section names a specific failure
- [ ] Self-check questions have answers

---

[← Previous](06_Truth_Tables_and_Tautologies.md) · [Module README](../README.md) · [Next →](08_Nested_Quantifiers_and_Why_Order_Matters.md)
