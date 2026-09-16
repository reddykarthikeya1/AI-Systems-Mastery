"""DEBUG LAB: DB::Exception: Too Many Parts in Table in ClickHouse

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

def reproduce_defect():
    # Defect demonstration code
    print("Executing defective implementation: DB::Exception: Too Many Parts in Table in ClickHouse")
    # Root Cause: Microservice sends 5,000 single-row HTTP INSERT requests per second to ClickHouse MergeTree, exhausting background merge worker capacity.
    raise RuntimeError("Defect triggered: DB::Exception: Too Many Parts in Table in ClickHouse")

if __name__ == "__main__":
    reproduce_defect()
