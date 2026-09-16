#!/usr/bin/env python3
"""DEBUG LAB: Decorator Retry Storm Exhausts Downstream Third-Party SMS API

THIS SCRIPT CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and verify the fix.
"""

import sys

def send_with_naive_retry(fn, max_retries: int = 5):
    for i in range(max_retries):
        try:
            return fn()
        except Exception:
            continue
    raise RuntimeError('Exhausted retries: hammered downstream service 5 times instantaneously!')


def reproduce_defect():
    print("Executing defective simulation for Module_06_GoF_Design_Patterns_Scalable_Systems...")
    send_with_naive_retry(lambda: (_ for _ in ()).throw(ConnectionError('503 Service Unavailable')))
    print("Execution unexpectedly succeeded without catching defect.")

if __name__ == "__main__":
    try:
        reproduce_defect()
    except Exception as e:
        print(f"\n[DEFECT TRIGGERED SUCCESSFULLY]\nException: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)
