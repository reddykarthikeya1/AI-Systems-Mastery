#!/usr/bin/env python3
"""DEBUG LAB: Write Amplification Catastrophe on Celebrity Fan-Out

THIS SCRIPT CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and verify the fix.
"""

import sys

def publish_post(author_id: str, followers: list[str]):
    if len(followers) >= 1000000:
        raise RuntimeError('Write amplification disaster: attempting 50,000,000 timeline inserts!')


def reproduce_defect():
    print("Executing defective simulation for Module_16_Social_Media_Newsfeed_Recommendation_TwoTower...")
    publish_post('celebrity_1', ['f']*1000000)
    print("Execution unexpectedly succeeded without catching defect.")

if __name__ == "__main__":
    try:
        reproduce_defect()
    except Exception as e:
        print(f"\n[OBSERVED FAILURE] {type(e).__name__}: {e}")
        print("\nThat is not what this should do. SYMPTOMS.md describes the "
              "expected behaviour; the cause is in the code above.")
