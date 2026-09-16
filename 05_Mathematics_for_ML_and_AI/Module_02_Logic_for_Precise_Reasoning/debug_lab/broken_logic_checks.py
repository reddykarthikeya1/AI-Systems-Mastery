"""A rule engine with three planted defects.

It runs to completion, raises nothing and exits 0. Every verdict it prints is
plausible. Three of them are wrong.
"""
from __future__ import annotations


def negate_and(a, b):
    """not (a and b)"""
    return (not a) and (not b)


def implies(p, q):
    """p implies q"""
    return p and q


def all_positive(values):
    """Every value is positive."""
    for value in values:
        if value > 0:
            return True
    return False


def truth_table(fn, name):
    rows = []
    for a in (True, False):
        for b in (True, False):
            rows.append((a, b, fn(a, b)))
    print(f"    {name}")
    for a, b, result in rows:
        print(f"      a={str(a):<5} b={str(b):<5} -> {result}")
    return rows


def main():
    print("=" * 66)
    print("RULE ENGINE - logic verification report")
    print("=" * 66)

    print()
    print("[1] De Morgan: not (a and b) should equal (not a) or (not b)")
    ours = truth_table(negate_and, "negate_and(a, b)")
    reference = [(a, b, not (a and b)) for a in (True, False) for b in (True, False)]
    print(f"    matches the definition on all four rows: {ours == reference}")

    print()
    print("[2] Implication: 'if it rains, the ground is wet'")
    truth_table(implies, "implies(p, q)")
    print("    checking the case where it does NOT rain:")
    print(f"      rain=False, wet=False -> {implies(False, False)}")
    print("    (a promise about rain says nothing about a dry day)")

    print()
    print("[3] Quantifier: 'all values are positive'")
    cases = [[1, 2, 3], [1, -2, 3], [-1, -2, -3], []]
    for values in cases:
        print(f"      all_positive({values}) -> {all_positive(values)}")

    print()
    print("=" * 66)
    print("Report complete. Exit status 0.")
    print("=" * 66)


if __name__ == "__main__":
    main()
