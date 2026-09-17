"""Reference Solution — Problem 01: reconcile_vector_clocks

Topic: LLD Financial Engines Splitwise Rate Limiting
"""

from __future__ import annotations

def reconcile_vector_clocks(vc_a: dict[str, int], vc_b: dict[str, int]) -> str:
    all_keys = set(vc_a.keys()) | set(vc_b.keys())
    a_dominates = False
    b_dominates = False
    for k in all_keys:
        val_a = vc_a.get(k, 0)
        val_b = vc_b.get(k, 0)
        if val_a > val_b:
            a_dominates = True
        elif val_b > val_a:
            b_dominates = True
    if a_dominates and not b_dominates:
        return "A_HAPPENED_BEFORE_B"
    elif b_dominates and not a_dominates:
        return "B_HAPPENED_BEFORE_A"
    elif not a_dominates and not b_dominates:
        return "IDENTICAL"
    else:
        return "CONCURRENT"

