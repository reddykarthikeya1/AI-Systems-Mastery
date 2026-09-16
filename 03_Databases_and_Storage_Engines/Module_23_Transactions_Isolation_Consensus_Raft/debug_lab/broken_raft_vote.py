"""DEBUG LAB: Split-Brain Dual Leader Election in Raft Cluster

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

def reproduce_defect():
    # Defect demonstration code
    print("Executing defective implementation: Split-Brain Dual Leader Election in Raft Cluster")
    # Root Cause: Candidate node transitions to Leader after receiving 2 votes in a 5-node cluster, violating majority quorum ($N/2 + 1 = 3$).
    raise RuntimeError("Defect triggered: Split-Brain Dual Leader Election in Raft Cluster")

if __name__ == "__main__":
    reproduce_defect()
