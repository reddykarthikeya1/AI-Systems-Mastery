#!/usr/bin/env python3
"""DEBUG LAB: MD5 Hash Collision and Truncation Inconsistencies

THIS SCRIPT CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and verify the fix.
"""

import sys

def naive_shorten(url: str) -> str:
    import hashlib
    return hashlib.md5(url.encode()).hexdigest()[:6]


def reproduce_defect():
    print("Executing defective simulation for Module_14_Distributed_URL_Shortener_TinyURL...")
    _ = naive_shorten('https://example.com/a')
    # Birthday paradox: 6-char hex is only 16^6 = 16.7M keys; collisions occur after ~4,000 items!
    raise RuntimeError('Hash truncation collision detected!')
    print("Execution unexpectedly succeeded without catching defect.")

if __name__ == "__main__":
    try:
        reproduce_defect()
    except Exception as e:
        print(f"\n[DEFECT TRIGGERED SUCCESSFULLY]\nException: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)
