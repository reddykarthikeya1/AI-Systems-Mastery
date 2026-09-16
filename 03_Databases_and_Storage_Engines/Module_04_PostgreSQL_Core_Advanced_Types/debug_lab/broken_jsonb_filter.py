"""DEBUG LAB: Sequential Scan on 5,000,000 JSONB Document Catalog

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

def reproduce_defect():
    # Defect demonstration code
    print("Executing defective implementation: Sequential Scan on 5,000,000 JSONB Document Catalog")
    # Root Cause: Query uses text extraction operator `data->>'status' = 'active'` which bypasses the GIN index created with jsonb_path_ops.
    raise RuntimeError("Defect triggered: Sequential Scan on 5,000,000 JSONB Document Catalog")

if __name__ == "__main__":
    reproduce_defect()
