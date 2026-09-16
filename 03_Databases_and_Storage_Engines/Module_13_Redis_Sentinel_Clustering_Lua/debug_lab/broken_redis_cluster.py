"""DEBUG LAB: CROSSSLOT Keys in Request Don't Hash to the Same Slot

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

def reproduce_defect():
    # Defect demonstration code
    print("Executing defective implementation: CROSSSLOT Keys in Request Don't Hash to the Same Slot")
    # Root Cause: Application attempts multi-key MGET on `user:101:profile` and `user:101:orders` across Redis Cluster, failing with CROSSSLOT error.
    raise RuntimeError("Defect triggered: CROSSSLOT Keys in Request Don't Hash to the Same Slot")

if __name__ == "__main__":
    reproduce_defect()
