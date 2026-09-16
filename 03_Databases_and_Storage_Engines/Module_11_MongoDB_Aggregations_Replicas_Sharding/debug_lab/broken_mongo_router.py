"""DEBUG LAB: Cluster-Wide Scatter-Gather Latency Spikes on Sharded MongoDB

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

def reproduce_defect():
    # Defect demonstration code
    print("Executing defective implementation: Cluster-Wide Scatter-Gather Latency Spikes on Sharded MongoDB")
    # Root Cause: High-frequency operational user profile queries filter on `email` instead of the collection shard key `tenant_id`, broadcasting every query to all 10 shards.
    raise RuntimeError("Defect triggered: Cluster-Wide Scatter-Gather Latency Spikes on Sharded MongoDB")

if __name__ == "__main__":
    reproduce_defect()
