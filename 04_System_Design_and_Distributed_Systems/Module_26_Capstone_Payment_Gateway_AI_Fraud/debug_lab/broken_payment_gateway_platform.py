#!/usr/bin/env python3
"""DEBUG LAB: Accounting Discrepancy from Unbalanced Double-Entry Ledger Posting

THIS SCRIPT CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and verify the fix.
"""

import sys

def post_ledger_entry(debit_amount: int, credit_amount: int):
    if debit_amount != credit_amount:
        raise ValueError(f'Accounting discrepancy! Debit ({debit_amount}) != Credit ({credit_amount})')


def reproduce_defect():
    print("Executing defective simulation for Module_26_Capstone_Payment_Gateway_AI_Fraud...")
    post_ledger_entry(1000, 998)
    print("Execution unexpectedly succeeded without catching defect.")

if __name__ == "__main__":
    try:
        reproduce_defect()
    except Exception as e:
        print(f"\n[OBSERVED FAILURE] {type(e).__name__}: {e}")
        print("\nThat is not what this should do. SYMPTOMS.md describes the "
              "expected behaviour; the cause is in the code above.")
