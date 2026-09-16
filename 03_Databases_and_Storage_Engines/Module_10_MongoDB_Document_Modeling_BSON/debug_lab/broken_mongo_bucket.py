"""DEBUG LAB: BSONObjectTooLarge Error on Unbounded Sensor Array

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

def reproduce_defect():
    # Defect demonstration code
    print("Executing defective implementation: BSONObjectTooLarge Error on Unbounded Sensor Array")
    # Root Cause: IoT readings appended continuously into a single document array without capping, eventually breaching the 16MB document size limit.
    raise RuntimeError("Defect triggered: BSONObjectTooLarge Error on Unbounded Sensor Array")

if __name__ == "__main__":
    reproduce_defect()
