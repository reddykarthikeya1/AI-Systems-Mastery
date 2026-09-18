#!/usr/bin/env python3
"""DEBUG LAB: Infinite Spider Trap Exhausts Crawler Memory and Storage

THIS SCRIPT CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and verify the fix.
"""

import sys

def crawl_url(url: str, visited: set):
    if 'calendar?day=' in url:
        raise RecursionError('Spider trap encountered! Infinite dynamic calendar URLs generated.')


def reproduce_defect():
    print("Executing defective simulation for Module_19_Distributed_Web_Crawler_Deduplication_Google...")
    crawl_url('http://example.com/calendar?day=99999', set())
    print("Execution unexpectedly succeeded without catching defect.")

if __name__ == "__main__":
    try:
        reproduce_defect()
    except Exception as e:
        print(f"\n[OBSERVED FAILURE] {type(e).__name__}: {e}")
        print("\nThat is not what this should do. SYMPTOMS.md describes the "
              "expected behaviour; the cause is in the code above.")
