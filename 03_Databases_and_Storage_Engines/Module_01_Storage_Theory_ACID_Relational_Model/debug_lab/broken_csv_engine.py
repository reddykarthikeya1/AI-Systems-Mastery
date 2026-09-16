"""DEBUG LAB: Uncommitted Transaction Leaks into Primary Table During Power Failure

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

def reproduce_defect():
    # Defect demonstration code
    print("Executing defective implementation: Uncommitted Transaction Leaks into Primary Table During Power Failure")
    # Root Cause: The csv engine flushes uncommitted in-memory rows directly to table.csv during insert() rather than deferring until commit(). When a crash occurs before commit(), dirty data is permanently written.
    raise RuntimeError("Defect triggered: Uncommitted Transaction Leaks into Primary Table During Power Failure")

if __name__ == "__main__":
    reproduce_defect()
