#!/usr/bin/env python3
"""DEBUG LAB: Penny Discrepancy Leak in Three-Way Bill Split

THIS SCRIPT CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and verify the fix.
"""

import sys

def split_bill_naive(total: float, people: list[str]) -> dict[str, float]:
    share = round(total / len(people), 2)
    return {p: share for p in people}


def reproduce_defect():
    print("Executing defective simulation for Module_08_LLD_Financial_Engines_Splitwise_Rate_Limiting...")
    splits = split_bill_naive(100.00, ['Alice', 'Bob', 'Charlie'])
    allocated = sum(splits.values())
    if allocated != 100.00:
        raise AssertionError(f'Financial balance violated! Allocated ${allocated}, lost ${100.00 - allocated}')
    print("Execution unexpectedly succeeded without catching defect.")

if __name__ == "__main__":
    try:
        reproduce_defect()
    except Exception as e:
        print(f"\n[DEFECT TRIGGERED SUCCESSFULLY]\nException: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)
