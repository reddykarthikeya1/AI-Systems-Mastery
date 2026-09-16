#!/usr/bin/env python3
"""DEBUG LAB: Distributed Trace Context Dropped Across Asynchronous Thread Handoff

THIS SCRIPT CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and verify the fix.
"""

import sys

def execute_async_task(task_fn):
    import threading
    t = threading.Thread(target=task_fn)  # Loses thread-local traceparent!
    t.start()
    t.join()
    raise RuntimeError('Trace context lost! Child span created without parent_id.')


def reproduce_defect():
    print("Executing defective simulation for Module_25_Observability_Distributed_Tracing_SRE...")
    execute_async_task(lambda: None)
    print("Execution unexpectedly succeeded without catching defect.")

if __name__ == "__main__":
    try:
        reproduce_defect()
    except Exception as e:
        print(f"\n[DEFECT TRIGGERED SUCCESSFULLY]\nException: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)
