#!/usr/bin/env python3
"""DEBUG LAB: Token Bucket Negative Balance Under High Concurrency Race

THIS SCRIPT CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and verify the fix.
"""

import sys

class DefectiveRateLimiter:
    def __init__(self, capacity: int = 10):
        self.capacity = capacity
        self.tokens = capacity
    
    def allow_request(self) -> bool:
        if self.tokens > 0:
            import time
            time.sleep(0.001)  # Simulates thread context switch
            self.tokens -= 1
            return True
        return False


def reproduce_defect():
    print("Executing defective simulation for Module_03_Edge_Infrastructure_Reverse_Proxies...")
    rl = DefectiveRateLimiter(capacity=1)
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
        results = list(ex.map(lambda _: rl.allow_request(), range(5)))
    if sum(results) > 1:
        raise AssertionError(f'Rate limiter bypassed! {sum(results)} requests allowed on capacity 1')
    print("Execution unexpectedly succeeded without catching defect.")

if __name__ == "__main__":
    try:
        reproduce_defect()
    except Exception as e:
        print(f"\n[OBSERVED FAILURE] {type(e).__name__}: {e}")
        print("\nThat is not what this should do. SYMPTOMS.md describes the "
              "expected behaviour; the cause is in the code above.")
