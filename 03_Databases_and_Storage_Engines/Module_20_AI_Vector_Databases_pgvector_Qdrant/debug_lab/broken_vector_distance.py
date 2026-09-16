"""DEBUG LAB: Vector Search Returns Irrelevant Nearest Neighbors Due to Dot Product on Unnormalized Vectors

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

def reproduce_defect():
    # Defect demonstration code
    print("Executing defective implementation: Vector Search Returns Irrelevant Nearest Neighbors Due to Dot Product on Unnormalized Vectors")
    # Root Cause: Embeddings inserted with arbitrary magnitudes while index was configured for Dot Product, causing vectors with huge norms to dominate similarity scores regardless of direction.
    raise RuntimeError("Defect triggered: Vector Search Returns Irrelevant Nearest Neighbors Due to Dot Product on Unnormalized Vectors")

if __name__ == "__main__":
    reproduce_defect()
