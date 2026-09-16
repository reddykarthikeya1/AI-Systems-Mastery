"""DEBUG LAB: Exclusive Table Lock Starvation During Online Schema Migration

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

def reproduce_defect():
    # Defect demonstration code
    print("Executing defective implementation: Exclusive Table Lock Starvation During Online Schema Migration")
    # Root Cause: Migration script runs `ALTER TABLE orders ADD COLUMN status_code INT;` without a lock_timeout, blocking behind a slow query and queuing all incoming web requests.
    raise RuntimeError("Defect triggered: Exclusive Table Lock Starvation During Online Schema Migration")

if __name__ == "__main__":
    reproduce_defect()
