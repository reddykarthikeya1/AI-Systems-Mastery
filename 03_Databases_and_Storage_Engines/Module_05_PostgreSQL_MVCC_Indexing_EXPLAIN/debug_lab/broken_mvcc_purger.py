"""DEBUG LAB: Dead Tuple Bloat Prevents Autovacuum Reclamation

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

def reproduce_defect():
    # Defect demonstration code
    print("Executing defective implementation: Dead Tuple Bloat Prevents Autovacuum Reclamation")
    # Root Cause: A long-running reporting session opened a transaction with `BEGIN; SELECT ...` and remained idle in transaction for 18 hours, pinning xmin and preventing autovacuum from cleaning dead tuples.
    raise RuntimeError("Defect triggered: Dead Tuple Bloat Prevents Autovacuum Reclamation")

if __name__ == "__main__":
    reproduce_defect()
