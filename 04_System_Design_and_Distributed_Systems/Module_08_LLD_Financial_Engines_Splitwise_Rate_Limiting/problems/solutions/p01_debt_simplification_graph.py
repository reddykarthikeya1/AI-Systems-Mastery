"""Reference Solution — Problem 01: Debt Simplification Graph

Topic: 08 LLD Financial Engines Splitwise Rate Limiting
"""

from __future__ import annotations


def debt_simplification_graph(balances: dict[str, float]) -> list[tuple[str, str, float]]:
    debtors = []   # (amount, person) where amount > 0
    creditors = [] # (amount, person) where amount > 0
    for p, b in balances.items():
        if b < -0.001:
            debtors.append([-b, p])
        elif b > 0.001:
            creditors.append([b, p])
    res = []
    while debtors and creditors:
        debtors.sort(reverse=True)
        creditors.sort(reverse=True)
        debt_amt, d_person = debtors[0]
        cred_amt, c_person = creditors[0]
        settle = min(debt_amt, cred_amt)
        res.append((d_person, c_person, round(settle, 2)))
        debtors[0][0] -= settle
        creditors[0][0] -= settle
        if debtors[0][0] < 0.001:
            debtors.pop(0)
        if creditors[0][0] < 0.001:
            creditors.pop(0)
    return res
