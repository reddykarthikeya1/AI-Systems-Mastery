"""DEBUG LAB: Cartesian Product OutOfMemoryError in Cypher Path Match

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

def reproduce_defect():
    # Defect demonstration code
    print("Executing defective implementation: Cartesian Product OutOfMemoryError in Cypher Path Match")
    # Root Cause: Query written as `MATCH (a:Person), (b:Company) WHERE a.city = b.city` without a relationship pattern, forcing an exhaustive $N \times M$ Cartesian product in RAM.
    raise RuntimeError("Defect triggered: Cartesian Product OutOfMemoryError in Cypher Path Match")

if __name__ == "__main__":
    reproduce_defect()
