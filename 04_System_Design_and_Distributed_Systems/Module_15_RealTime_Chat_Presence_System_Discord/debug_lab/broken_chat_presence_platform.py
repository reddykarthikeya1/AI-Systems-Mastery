#!/usr/bin/env python3
"""DEBUG LAB: Celebrity Presence Broadcast Avalanche Floods Gateway Memory

THIS SCRIPT CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and verify the fix.
"""

import sys

def broadcast_presence(user_id: str, followers: list[str]):
    if len(followers) > 50000:
        raise MemoryError('Gateway buffer overflow: 100,000 simultaneous presence frames generated!')


def reproduce_defect():
    print("Executing defective simulation for Module_15_RealTime_Chat_Presence_System_Discord...")
    broadcast_presence('streamer_1', ['f']*100000)
    print("Execution unexpectedly succeeded without catching defect.")

if __name__ == "__main__":
    try:
        reproduce_defect()
    except Exception as e:
        print(f"\n[DEFECT TRIGGERED SUCCESSFULLY]\nException: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)
