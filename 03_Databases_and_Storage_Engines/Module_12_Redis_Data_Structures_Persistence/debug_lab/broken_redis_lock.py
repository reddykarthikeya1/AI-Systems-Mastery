"""DEBUG LAB: Distributed Lock Race Condition Releases Another Worker's Lock

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

def reproduce_defect():
    # Defect demonstration code
    print("Executing defective implementation: Distributed Lock Race Condition Releases Another Worker's Lock")
    # Root Cause: Worker acquires lock with `SET lock_key 1 EX 10`. Worker takes 12 seconds to finish. Lock expires. Worker 2 acquires lock. Worker 1 then calls `DEL lock_key`, releasing Worker 2's lock prematurely.
    raise RuntimeError("Defect triggered: Distributed Lock Race Condition Releases Another Worker's Lock")

if __name__ == "__main__":
    reproduce_defect()
