# Lesson 02.01 — Propositions, Truth Values and Notation

> **Module 02:** Logic for Precise Reasoning · Lesson 1 of 19

---

## What you will be able to do after this lesson

- [ ] Distinguish a proposition from an expression that has no truth value.
- [ ] Write a compound claim in symbols and evaluate it for given truth values.

## Prerequisites

- None. This is the entry point for the module.

---

## 1. The idea

A **proposition** is a statement that is either true or false - not both, not
neither. "The model has 12 layers" is a proposition. "How many layers?" is not.
Neither is "this model is good", until *good* is given a criterion.

That last case is the one worth dwelling on. Most disagreements about a result
are not disagreements about facts; they are cases where the claim was not a
proposition yet, so there was nothing to check.

Notation:

| Symbol | Name | Read |
| :--- | :--- | :--- |
| `p`, `q`, `r` | propositional variables | stand-ins for claims |
| `¬p` | negation | not p |
| `p ∧ q` | conjunction | p and q |
| `p ∨ q` | disjunction | p or q (inclusive) |
| `p → q` | implication | if p then q |
| `p ↔ q` | biconditional | p if and only if q |

`∨` is **inclusive**: `p ∨ q` is true when both are true. English "or" is
often exclusive ("tea or coffee"), and that mismatch causes real errors when
translating a requirement into a filter.

## 2. Worked example

Take `p` = "accuracy exceeds 0.9" and `q` = "latency is under 50 ms".

A release rule: "ship if accuracy exceeds 0.9 and latency is under 50 ms" is
`p ∧ q`.

Suppose a candidate has accuracy 0.93 and latency 60 ms. Then `p` is true and
`q` is false, so:

    p ∧ q  = T ∧ F = F      do not ship
    p ∨ q  = T ∨ F = T      at least one criterion met
    ¬q     = T              latency is not under 50 ms
    p ∧ ¬q = T              fast enough on accuracy, too slow

The last line is the useful diagnostic: it isolates *which* criterion failed,
which `p ∧ q = F` alone does not tell you.

Now a non-proposition: "the model is production-ready". Until that is defined as
a conjunction of checkable claims, it has no truth value and cannot appear in a
release rule.

## 3. Verify it in code

```python
p = True    # accuracy > 0.9
q = False   # latency < 50 ms

assert (p and q) is False, "ship only if both hold"
assert (p or q) is True
assert (not q) is True
assert (p and not q) is True, "isolates which criterion failed"

# Inclusive or: true when BOTH are true.
assert (True or True) is True

# Exclusive or is a different connective.
assert (True != True) is False
assert (True != False) is True

# A proposition has exactly one truth value; enumerate all assignments.
from itertools import product
rows = [(a, b, a and b) for a, b in product([True, False], repeat=2)]
assert len(rows) == 4
assert sum(1 for _, _, value in rows if value) == 1, "conjunction is true once"

ors = [(a, b, a or b) for a, b in product([True, False], repeat=2)]
assert sum(1 for _, _, value in ors if value) == 3, "disjunction is false once"
```

## 4. The mistake people actually make

**Writing a release criterion that is not a proposition.**

"Ship when the model is good enough" cannot be evaluated, so it is settled by
whoever argues longest. The fix is not more discussion - it is turning the claim
into a conjunction of propositions, each with a threshold and a measurement
procedure.

The second, narrower error: translating English "or" as exclusive. "Alert if
latency is high or the error rate is high" means alert when *either or both*
hold - inclusive. Implementing it as exclusive-or silently suppresses the alarm
in exactly the worst case, when both go wrong at once.

That is a real outage pattern, and it is invisible in testing because tests
usually exercise one failure at a time.

---

## Check yourself

1. Is 'x > 5' a proposition?
2. Translate: 'alert unless both replicas are healthy'.
3. Why is implementing 'or' as exclusive-or dangerous in an alerting rule?

<details>
<summary>Answers</summary>

1. Not on its own - its truth depends on x. It is a *predicate*, which becomes a proposition once x is given a value or a quantifier is applied.
2. `¬(h₁ ∧ h₂)`, equivalently `¬h₁ ∨ ¬h₂` by De Morgan - alert when at least one replica is unhealthy.
3. Exclusive-or is false when both conditions hold, so the alert is suppressed precisely when two things have gone wrong simultaneously - the case you most need to hear about.

</details>

---

## Lesson checklist

- [ ] Learning objectives are concrete and checkable
- [ ] Worked example has no skipped arithmetic
- [ ] Code block runs as written and asserts
- [ ] The common-mistake section names a specific failure
- [ ] Self-check questions have answers

---

[Module README](../README.md) · [Next →](02_Conjunction_Disjunction_and_Negation.md)
