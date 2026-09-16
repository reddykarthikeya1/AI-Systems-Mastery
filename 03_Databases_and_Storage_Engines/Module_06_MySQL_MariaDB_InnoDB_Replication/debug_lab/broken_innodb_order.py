"""DEBUG LAB: Deadlock 1213 on High Concurrency Multi-Row Updates

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

def reproduce_defect():
    # Defect demonstration code
    print("Executing defective implementation: Deadlock 1213 on High Concurrency Multi-Row Updates")
    # Root Cause: Application updates multiple inventory rows in arbitrary order (Thread A updates Item 10 then 20; Thread B updates Item 20 then 10), triggering cyclic lock waits.
    raise RuntimeError("Defect triggered: Deadlock 1213 on High Concurrency Multi-Row Updates")

if __name__ == "__main__":
    reproduce_defect()
