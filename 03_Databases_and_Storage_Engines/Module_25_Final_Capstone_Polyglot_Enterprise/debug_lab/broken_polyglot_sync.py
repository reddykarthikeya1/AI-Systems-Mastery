"""DEBUG LAB: Dual-Write Inconsistency Between Relational DB and Redis Cache

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

def reproduce_defect():
    # Defect demonstration code
    print("Executing defective implementation: Dual-Write Inconsistency Between Relational DB and Redis Cache")
    # Root Cause: Application updates database and then updates Redis in two uncoordinated calls. Redis network glitch drops cache update, leaving stale data forever.
    raise RuntimeError("Defect triggered: Dual-Write Inconsistency Between Relational DB and Redis Cache")

if __name__ == "__main__":
    reproduce_defect()
