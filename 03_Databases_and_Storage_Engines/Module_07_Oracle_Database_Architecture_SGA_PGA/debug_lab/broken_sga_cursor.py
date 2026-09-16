"""DEBUG LAB: ORA-04031 Shared Pool Out of Memory via Literal SQL

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

def reproduce_defect():
    # Defect demonstration code
    print("Executing defective implementation: ORA-04031 Shared Pool Out of Memory via Literal SQL")
    # Root Cause: Application constructs SQL dynamically using f-strings (`SELECT * FROM emp WHERE id = {emp_id}`), creating 100,000 unique unsharable execution plans in the Library Cache.
    raise RuntimeError("Defect triggered: ORA-04031 Shared Pool Out of Memory via Literal SQL")

if __name__ == "__main__":
    reproduce_defect()
