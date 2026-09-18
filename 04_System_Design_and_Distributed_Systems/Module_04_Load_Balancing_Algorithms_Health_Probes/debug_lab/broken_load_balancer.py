#!/usr/bin/env python3
"""DEBUG LAB: Load Balancer Cascading Collapse via Unhealthy Server Flapping

THIS SCRIPT CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and verify the fix.
"""

import sys

def select_server(servers: list[dict]) -> dict:
    active = [s for s in servers if s['healthy']]
    if not active:
        raise RuntimeError('All servers marked unhealthy! Full outage triggered by cascading flapping.')
    return active[0]


def reproduce_defect():
    print("Executing defective simulation for Module_04_Load_Balancing_Algorithms_Health_Probes...")
    servers = [{'id': 1, 'healthy': False}, {'id': 2, 'healthy': False}]
    select_server(servers)
    print("Execution unexpectedly succeeded without catching defect.")

if __name__ == "__main__":
    try:
        reproduce_defect()
    except Exception as e:
        print(f"\n[OBSERVED FAILURE] {type(e).__name__}: {e}")
        print("\nThat is not what this should do. SYMPTOMS.md describes the "
              "expected behaviour; the cause is in the code above.")
