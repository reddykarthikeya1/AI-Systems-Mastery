"""DEBUG LAB: Deadlock in Concurrent B+ Tree Node Split

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

def reproduce_defect():
    # Defect demonstration code
    print("Executing defective implementation: Deadlock in Concurrent B+ Tree Node Split")
    # Root Cause: Writer released parent latch before acquiring child latch during downward traversal, allowing a concurrent split to invalidate node pointers.
    raise RuntimeError("Defect triggered: Deadlock in Concurrent B+ Tree Node Split")

if __name__ == "__main__":
    reproduce_defect()
