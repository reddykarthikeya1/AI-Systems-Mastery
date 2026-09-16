#!/usr/bin/env python3
"""DEBUG LAB: Tail Latency Amplification Cripples Microservice Fanout

THIS SCRIPT CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and verify the fix.
"""

import sys

def estimate_user_experience_latency(service_p99_ms: float, fanout_calls: int) -> float:
    # In reality, probability of at least one call exceeding p99 across N calls is 1 - (1 - 0.01)^N!
    return service_p99_ms


def reproduce_defect():
    print("Executing defective simulation for Module_01_Physics_of_Scalability_Capacity_Math...")
    _ = estimate_user_experience_latency(10.0, fanout_calls=100)
    # With 100 parallel calls, 1 - (0.99)^100 = 63.4% of all user requests experience tail latency!
    raise RuntimeError('Aggregate tail latency is 63.4% degraded, but estimator reports 10ms!')
    print("Execution unexpectedly succeeded without catching defect.")

if __name__ == "__main__":
    try:
        reproduce_defect()
    except Exception as e:
        print(f"\n[DEFECT TRIGGERED SUCCESSFULLY]\nException: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)
