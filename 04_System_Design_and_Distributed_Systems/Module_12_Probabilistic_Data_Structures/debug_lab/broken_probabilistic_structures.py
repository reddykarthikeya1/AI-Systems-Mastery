#!/usr/bin/env python3
"""DEBUG LAB: Bloom Filter False Positive Rate Explodes Beyond Expected Bounds

THIS SCRIPT CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and verify the fix.
"""

import sys

def check_bloom_filter_saturation(bit_array: list[int], current_items: int, capacity: int):
    saturation = sum(bit_array) / len(bit_array)
    if saturation > 0.90:
        raise RuntimeError(f'Bloom filter completely saturated ({saturation*100:.1f}% bits set)! False positives catastrophic.')


def reproduce_defect():
    print("Executing defective simulation for Module_12_Probabilistic_Data_Structures...")
    check_bloom_filter_saturation([1]*95 + [0]*5, current_items=2000000, capacity=100000)
    print("Execution unexpectedly succeeded without catching defect.")

if __name__ == "__main__":
    try:
        reproduce_defect()
    except Exception as e:
        print(f"\n[OBSERVED FAILURE] {type(e).__name__}: {e}")
        print("\nThat is not what this should do. SYMPTOMS.md describes the "
              "expected behaviour; the cause is in the code above.")
