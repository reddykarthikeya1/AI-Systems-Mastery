"""DEBUG LAB: Full Table Scan Caused by Function Wrapping on Indexed Timestamp

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

def reproduce_defect():
    # Defect demonstration code
    print("Executing defective implementation: Full Table Scan Caused by Function Wrapping on Indexed Timestamp")
    # Root Cause: Query filters on `WHERE DATE(created_at) = '2026-01-01'`, blinding the query optimizer to the B-Tree index on `created_at`.
    raise RuntimeError("Defect triggered: Full Table Scan Caused by Function Wrapping on Indexed Timestamp")

if __name__ == "__main__":
    reproduce_defect()
