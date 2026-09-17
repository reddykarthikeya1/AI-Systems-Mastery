"""Problem 01 — Debt Simplification Graph

Topic: 08 LLD Financial Engines Splitwise Rate Limiting
Target: Production-grade implementation

Minimize transactions among group expense balances.

Hints:
    Hint 1: Review module invariants.
    Hint 2: Handle edge cases, scale factors, and state transitions cleanly.
    Hint 3: Run pytest tests/ to verify.
"""

from __future__ import annotations


def debt_simplification_graph(balances: dict[str, float]) -> list[tuple[str, str, float]]:
    """balances: person -> net_balance (+ owes money, - is owed money).
    Match max debtor with max creditor greedily until all debts are settled to 0.00.
    Returns list of (debtor, creditor, amount) rounded to 2 decimal places.
    """
    raise NotImplementedError("Implement debt_simplification_graph")
