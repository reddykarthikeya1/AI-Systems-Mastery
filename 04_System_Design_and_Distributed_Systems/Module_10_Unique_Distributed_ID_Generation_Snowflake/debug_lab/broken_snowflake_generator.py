#!/usr/bin/env python3
"""DEBUG LAB: Duplicate Snowflake IDs Generated During NTP Backward Time Leap

THIS SCRIPT CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and verify the fix.
"""

import sys

def generate_snowflake_id(last_timestamp: int, current_timestamp: int, sequence: int) -> int:
    if current_timestamp < last_timestamp:
        pass
    return (current_timestamp << 22) | sequence


def reproduce_defect():
    print("Executing defective simulation for Module_10_Unique_Distributed_ID_Generation_Snowflake...")
    generate_snowflake_id(last_timestamp=1000, current_timestamp=990, sequence=1)
    raise RuntimeError('Clock moved backwards! Duplicate IDs generated for timestamp 990!')
    print("Execution unexpectedly succeeded without catching defect.")

if __name__ == "__main__":
    try:
        reproduce_defect()
    except Exception as e:
        print(f"\n[OBSERVED FAILURE] {type(e).__name__}: {e}")
        print("\nThat is not what this should do. SYMPTOMS.md describes the "
              "expected behaviour; the cause is in the code above.")
