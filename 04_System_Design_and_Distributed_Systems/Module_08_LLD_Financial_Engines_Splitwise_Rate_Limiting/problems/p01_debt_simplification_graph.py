"""Problem 01 — Debt Simplification Graph

Topic: 08 LLD Financial Engines Splitwise Rate Limiting
Target: Production-grade implementation

Minimize transactions among group expense balances.

Example:
    >>> debt_simplification_graph({'Alice': 50.0, 'Bob': -30.0, 'Charlie': -20.0})
    [('Bob', 'Alice', 30.0), ('Charlie', 'Alice', 20.0)]

Hints:
    Hint 1: Minimizing the transaction count is a greedy matching problem
        — always settle the single biggest debtor against the single
        biggest creditor first, not balances in input order.
    Hint 2: Maintain two lists of (amount, person) — debtors and
        creditors — and repeatedly re-sort and take the largest of each,
        settling `min(debt_amt, cred_amt)` between that pair.
    Hint 3: Use an epsilon tolerance (e.g. 0.001) when comparing balances
        or remaining amounts to zero, since floating-point subtraction
        leaves tiny residues that would otherwise create phantom
        leftover entries; round every settled amount to 2 decimal places
        before appending it to the result.
"""

from __future__ import annotations


def debt_simplification_graph(balances: dict[str, float]) -> list[tuple[str, str, float]]:
    """balances: person -> net_balance (+ owes money, - is owed money).
    Match max debtor with max creditor greedily until all debts are settled to 0.00.
    Returns list of (debtor, creditor, amount) rounded to 2 decimal places.
    """
    raise NotImplementedError("Implement debt_simplification_graph")
