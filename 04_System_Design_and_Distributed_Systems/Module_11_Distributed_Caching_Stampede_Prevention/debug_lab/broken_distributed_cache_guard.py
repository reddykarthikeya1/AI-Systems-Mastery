#!/usr/bin/env python3
"""DEBUG LAB: Cache Stampede Crashes Primary Database on Hot Key Expiration

THIS SCRIPT CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and verify the fix.
"""

import sys

def get_product(key: str, cache: dict, db_query_fn):
    val = cache.get(key)
    if val is None:
        val = db_query_fn(key)
        cache[key] = val
    return val


def reproduce_defect():
    print("Executing defective simulation for Module_11_Distributed_Caching_Stampede_Prevention...")
    call_count = 0
    def db():
        nonlocal call_count
        call_count += 1
        return 'data'
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
        list(ex.map(lambda _: get_product('hot_key', {}, db), range(10)))
    if call_count > 1:
        raise RuntimeError(f'Thundering herd! DB was hammered {call_count} times for 1 key!')
    print("Execution unexpectedly succeeded without catching defect.")

if __name__ == "__main__":
    try:
        reproduce_defect()
    except Exception as e:
        print(f"\n[OBSERVED FAILURE] {type(e).__name__}: {e}")
        print("\nThat is not what this should do. SYMPTOMS.md describes the "
              "expected behaviour; the cause is in the code above.")
