#!/usr/bin/env python3
"""DEBUG LAB: Elevator Starvation Under Upward Continuous Hall Calls

THIS SCRIPT CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and verify the fix.
"""

import sys

def get_next_floor(current_floor: int, direction: str, up_queue: list, down_queue: list) -> int:
    if direction == 'UP' and up_queue:
        return min(up_queue)
    if down_queue:
        return max(down_queue)
    raise RuntimeError('Starvation anomaly: down_queue never serviced while up_queue has items!')


def reproduce_defect():
    print("Executing defective simulation for Module_07_LLD_State_Machines_Scheduling_Elevator_Parking...")
    get_next_floor(1, 'UP', up_queue=[2, 3], down_queue=[1])
    raise RuntimeError('Starvation: Passenger on floor 1 never served!')
    print("Execution unexpectedly succeeded without catching defect.")

if __name__ == "__main__":
    try:
        reproduce_defect()
    except Exception as e:
        print(f"\n[OBSERVED FAILURE] {type(e).__name__}: {e}")
        print("\nThat is not what this should do. SYMPTOMS.md describes the "
              "expected behaviour; the cause is in the code above.")
