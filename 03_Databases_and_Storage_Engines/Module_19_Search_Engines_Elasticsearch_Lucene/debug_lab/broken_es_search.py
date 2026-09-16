"""DEBUG LAB: Deep Pagination Offset Crashes Elasticsearch Data Nodes

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

def reproduce_defect():
    # Defect demonstration code
    print("Executing defective implementation: Deep Pagination Offset Crashes Elasticsearch Data Nodes")
    # Root Cause: Application paginates search results using `from: 50000, size: 50`, exhausting coordinator node heap memory.
    raise RuntimeError("Defect triggered: Deep Pagination Offset Crashes Elasticsearch Data Nodes")

if __name__ == "__main__":
    reproduce_defect()
