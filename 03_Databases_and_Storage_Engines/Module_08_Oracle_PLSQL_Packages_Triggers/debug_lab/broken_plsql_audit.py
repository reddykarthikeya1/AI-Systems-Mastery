"""DEBUG LAB: Audit Log Erased When Financial Transaction Fails

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

def reproduce_defect():
    # Defect demonstration code
    print("Executing defective implementation: Audit Log Erased When Financial Transaction Fails")
    # Root Cause: The security audit logging procedure was declared without `PRAGMA AUTONOMOUS_TRANSACTION`. When the parent transfer rolls back due to insufficient funds, the audit record is rolled back with it.
    raise RuntimeError("Defect triggered: Audit Log Erased When Financial Transaction Fails")

if __name__ == "__main__":
    reproduce_defect()
