"""DEBUG LAB: ReadFailure Scanned Over 100,000 Tombstones

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

def reproduce_defect():
    # Defect demonstration code
    print("Executing defective implementation: ReadFailure Scanned Over 100,000 Tombstones")
    # Root Cause: Application repeatedly deleted expired queue items using CQL DELETE in a high-volume polling loop, generating millions of tombstones that choked subsequent range scans.
    raise RuntimeError("Defect triggered: ReadFailure Scanned Over 100,000 Tombstones")

if __name__ == "__main__":
    reproduce_defect()
