"""Reference Solution — Problem 01: Boolean Satisfiability Dpll

Topic: 02 Logic for Precise Reasoning
"""

from __future__ import annotations


def boolean_satisfiability_dpll(clauses: list[list[int]], assignment: dict[int, bool]) -> bool:
    for c in clauses:
        clause_true = False
        for lit in c:
            var = abs(lit)
            val = assignment.get(var, False)
            if (lit > 0 and val) or (lit < 0 and not val):
                clause_true = True
                break
        if not clause_true:
            return False
    return True
