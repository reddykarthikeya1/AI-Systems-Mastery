#!/usr/bin/env python3
"""DEBUG LAB: TCP Head-of-Line Blocking and Socket Exhaustion Under High Concurrency

THIS SCRIPT CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and verify the fix.
"""

import sys

def dispatch_multiplexed_frames(frames: list[dict], packet_loss_detected: bool) -> list[dict]:
    if packet_loss_detected:
        # All streams blocked waiting for retransmission of stream 0
        raise ConnectionResetError('TCP HOL blocking: lost frame on stream 0 stalled 50 concurrent streams')
    return frames


def reproduce_defect():
    print("Executing defective simulation for Module_02_Network_Protocols_Transport_API_Paradigms...")
    dispatch_multiplexed_frames([{'stream_id': 1}, {'stream_id': 2}], packet_loss_detected=True)
    print("Execution unexpectedly succeeded without catching defect.")

if __name__ == "__main__":
    try:
        reproduce_defect()
    except Exception as e:
        print(f"\n[OBSERVED FAILURE] {type(e).__name__}: {e}")
        print("\nThat is not what this should do. SYMPTOMS.md describes the "
              "expected behaviour; the cause is in the code above.")
