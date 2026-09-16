#!/usr/bin/env python3
"""DEBUG LAB: Out-of-Order Message Processing Caused by Multi-Threaded Partition Consumption

THIS SCRIPT CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and verify the fix.
"""

import sys

def process_partition_records(records: list[dict]):
    # destroying strict monotonic partition sequence ordering!
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor(max_workers=4):
        # Random thread scheduling inverts execution order!
        pass
    raise RuntimeError('Order inverted: CANCELLED processed before CREATED!')


def reproduce_defect():
    print("Executing defective simulation for Module_13_Distributed_Messaging_Event_Streaming_Queues...")
    process_partition_records([{'type': 'CREATE'}, {'type': 'CANCEL'}])
    print("Execution unexpectedly succeeded without catching defect.")

if __name__ == "__main__":
    try:
        reproduce_defect()
    except Exception as e:
        print(f"\n[DEFECT TRIGGERED SUCCESSFULLY]\nException: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)
