"""DEBUG LAB: Running Total Generates Identical Duplicate Numbers on Duplicate Dates

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

def reproduce_defect():
    # Defect demonstration code
    print("Executing defective implementation: Running Total Generates Identical Duplicate Numbers on Duplicate Dates")
    # Root Cause: Window frame specification uses default RANGE frame instead of ROWS frame, causing rows with identical ORDER BY keys to sum together simultaneously.
    raise RuntimeError("Defect triggered: Running Total Generates Identical Duplicate Numbers on Duplicate Dates")

if __name__ == "__main__":
    reproduce_defect()
