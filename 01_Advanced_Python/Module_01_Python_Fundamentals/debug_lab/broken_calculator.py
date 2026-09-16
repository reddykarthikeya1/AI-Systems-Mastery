#!/usr/bin/env python3
"""Broken Financial Settlement Engine demonstrating precision and identity traps."""

def verify_accounts_settled(credit: float, debit: float, target: float) -> bool:
    return (credit + debit) == target

def calculate_tier_bonus(account_id_a: int, account_id_b: int) -> bool:
    # Works for -5..256 due to CPython small integer caching, breaks for >= 257!
    return account_id_a is account_id_b

def compute_installments(total_amount: float, months: int) -> list[float]:
    installments = []
    monthly = round(total_amount / months, 2)
    for _ in range(1, months):
        installments.append(monthly)
    return installments

if __name__ == "__main__":
    print("Testing settlements:")
    res = verify_accounts_settled(0.1, 0.2, 0.3)
    print(f"0.1 + 0.2 == 0.3: {res} (Expected: True)")

    id1 = 1000
    id2 = int("1000")
    print(f"ID matching with 'is': {calculate_tier_bonus(id1, id2)} (Expected: True)")

    payments = compute_installments(1200.0, 12)
    print(f"Generated {len(payments)} installments (Expected: 12)")
