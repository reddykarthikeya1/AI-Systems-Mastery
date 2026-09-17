"""Beginner playground for Module 02 - Logic for Precise Reasoning.

    python 03_try_it_yourself.py

Standard library only. Every block here also appears in 02_FOUNDATIONS_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

# -------------------------------------------- 1. Boolean Truth Tables and Operators
def logical_and(p, q): return p and q
def logical_or(p, q): return p or q
def logical_not(p): return not p

assert logical_and(True, False) is False
assert logical_or(True, False) is True
assert logical_not(False) is True
print("Basic boolean operations verified.")

# -------------------------------------------- 2. Material Implication (P implies Q)
def implies(p, q):
    return (not p) or q

assert implies(True, True) is True
assert implies(True, False) is False
assert implies(False, True) is True, "Vacuous truth"
assert implies(False, False) is True
print("Material implication truth table verified.")

# -------------------------------------------- 3. De Morgan's Laws Verification
for p in [True, False]:
    for q in [True, False]:
        lhs1 = not (p and q)
        rhs1 = (not p) or (not q)
        assert lhs1 == rhs1, "De Morgan Law 1 failed"
        lhs2 = not (p or q)
        rhs2 = (not p) and (not q)
        assert lhs2 == rhs2, "De Morgan Law 2 failed"

print("De Morgan's laws verified across all input valuations.")

print()
print("All checks passed.")
