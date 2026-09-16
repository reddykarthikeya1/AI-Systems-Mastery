"""DEBUG LAB: Database is Locked Exception on High Concurrent Ingestion

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

def reproduce_defect():
    # Defect demonstration code
    print("Executing defective implementation: Database is Locked Exception on High Concurrent Ingestion")
    # Root Cause: SQLite connection initialized without setting PRAGMA busy_timeout, causing any writer encountering a momentary lock to crash immediately with SQLITE_BUSY.
    raise RuntimeError("Defect triggered: Database is Locked Exception on High Concurrent Ingestion")

if __name__ == "__main__":
    reproduce_defect()
