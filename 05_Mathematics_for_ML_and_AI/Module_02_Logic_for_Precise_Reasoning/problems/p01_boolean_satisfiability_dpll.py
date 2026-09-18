"""Problem 01 — Boolean Satisfiability Dpll

Topic: 02 Logic for Precise Reasoning
Target: Production-grade implementation

Evaluate boolean 2-SAT / CNF formula under given variable truth assignment.

Example:
    >>> boolean_satisfiability_dpll([[1, -2], [2, 3]], {1: True, 2: False, 3: True})
    True

Hints:
    Hint 1: A CNF formula is a conjunction (AND) of clauses, and each clause
        is a disjunction (OR) of literals — the whole formula is satisfied
        only if every single clause has at least one true literal.
    Hint 2: For each clause, walk its literals: a positive literal `+var` is
        satisfied when `assignment[var]` is True, a negative literal `-var`
        is satisfied when it is False. Short-circuit a clause to true as
        soon as one literal matches.
    Hint 3: A variable that never appears in `assignment` still needs a
        truth value — treat it as False via `assignment.get(var, False)`
        rather than raising a KeyError, and return False the moment any
        single clause has no satisfied literal.
"""

from __future__ import annotations


def boolean_satisfiability_dpll(clauses: list[list[int]], assignment: dict[int, bool]) -> bool:
    """clauses: list of clauses. Each literal is +var or -var.
    Clause is True if at least one literal is satisfied under assignment.
    Returns True if ALL clauses evaluate to True.
    """
    raise NotImplementedError("Implement boolean_satisfiability_dpll")
