#!/usr/bin/env python3
"""DEBUG LAB: Daily Storage Arithmetic Underflows by Factor of 1000 Due to Megabyte/Mebibyte Unit Confusion

THIS SCRIPT CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and verify the fix.
"""

import sys

def calculate_provisioned_storage(qps: int, payload_bytes: int, days: int, replication_factor: int = 3) -> float:
    daily_bytes = qps * payload_bytes * 86400
    # Underprovisions storage drastically:
    reported_gib = daily_bytes / (1000 * 1000)  # reports MB as GiB without replication
    return reported_gib


def reproduce_defect():
    print("Executing defective simulation for Module_00_System_Design_Fundamentals_Interview_Playbook...")
    capacity = calculate_provisioned_storage(qps=5000, payload_bytes=1024, days=365, replication_factor=3)
    # Expected ~12,987 GiB, but buggy calculation reports only 432,000 (wrong unit, no repl)
    assert capacity > 10000000, f'Storage dangerously underprovisioned: {capacity}'
    print("Execution unexpectedly succeeded without catching defect.")

if __name__ == "__main__":
    try:
        reproduce_defect()
    except Exception as e:
        print(f"\n[DEFECT TRIGGERED SUCCESSFULLY]\nException: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)
