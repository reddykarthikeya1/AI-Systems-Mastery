# 🐣 Interactive Foundations Playground: Logic for Precise Reasoning

> *"Boolean logic is the switchboard of computation: every complex decision breaks down to AND, OR, NOT, and implication."*

> 💡 **Try It in the Live Runner:** You can run and modify any snippet in this playground directly in your browser! Click the **`▶ Run`** button in the header of any code block to test it instantly on the side, or toggle **`Live Runner`** in the top navigation bar to experiment with Python, PowerShell, and CLI commands while reading.

**Brand new to this topic? Start here, not with the README.**

Everything on this page is plain Python from the standard library. No Docker, no server, no `pip install`, no account to sign up for. You can read it in ten minutes and run it in one:

```bash
python 03_try_it_yourself.py
```

That script is this page, in order, with the assertions left in. If it prints `All checks passed`, every claim below just proved itself on your machine.

---

## 0. Everything this page needs

Nothing here is installed. These all ship with Python.

```python

```

---

## 1. Boolean Truth Tables and Operators

Conjunction (AND), disjunction (OR), and negation (NOT) define discrete decision boundaries in rule-based classifiers.

```python
def logical_and(p, q): return p and q
def logical_or(p, q): return p or q
def logical_not(p): return not p

assert logical_and(True, False) is False
assert logical_or(True, False) is True
assert logical_not(False) is True
print("Basic boolean operations verified.")
```

---

## 2. Material Implication (P implies Q)

In formal logic, $P \implies Q$ is logically equivalent to $\neg P \lor Q$. It is only false when a true premise leads to a false conclusion.

```python
def implies(p, q):
    return (not p) or q

assert implies(True, True) is True
assert implies(True, False) is False
assert implies(False, True) is True, "Vacuous truth"
assert implies(False, False) is True
print("Material implication truth table verified.")
```

---

## 3. De Morgan's Laws Verification

De Morgan's laws state that $\neg(P \land Q) \iff (\neg P \lor \neg Q)$ and $\neg(P \lor Q) \iff (\neg P \land \neg Q)$.

```python
for p in [True, False]:
    for q in [True, False]:
        lhs1 = not (p and q)
        rhs1 = (not p) or (not q)
        assert lhs1 == rhs1, "De Morgan Law 1 failed"
        lhs2 = not (p or q)
        rhs2 = (not p) and (not q)
        assert lhs2 == rhs2, "De Morgan Law 2 failed"

print("De Morgan's laws verified across all input valuations.")
```

---
