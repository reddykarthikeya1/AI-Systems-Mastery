"""DEBUG LAB: Cluster-Wide Scatter-Gather Latency Spikes on Sharded MongoDB

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

from __future__ import annotations

import zlib

class ShardedCluster:
    """A toy sharded cluster where the collection's shard key is tenant_id."""

    def __init__(self, num_shards: int) -> None:
        self.num_shards = num_shards
        self.docs: list[dict] = []

    def shard_for(self, tenant_id: str) -> int:
        return zlib.crc32(tenant_id.encode()) % self.num_shards

    def insert(self, tenant_id: str, email: str) -> None:
        self.docs.append({"tenant_id": tenant_id, "email": email})

    def query_by_shard_key(self, tenant_id: str) -> set[int]:
        return {self.shard_for(tenant_id)}

    def query_by_email(self, email: str) -> set[int]:
        """No shard key in the filter -- mongos must broadcast to every shard."""
        return set(range(self.num_shards))

def reproduce_defect() -> None:
    print("Querying a 10-shard cluster for one user profile by email...")
    cluster = ShardedCluster(num_shards=10)
    for i in range(200):
        cluster.insert(tenant_id=f"tenant-{i % 20}", email=f"user{i}@example.com")

    shards_for_shard_key_query = cluster.query_by_shard_key("tenant-7")
    shards_for_email_query = cluster.query_by_email("user77@example.com")

    print(f"Shards contacted filtering on tenant_id (shard key): {len(shards_for_shard_key_query)}")
    print(f"Shards contacted filtering on email (non-shard-key): {len(shards_for_email_query)}")
    if len(shards_for_email_query) == cluster.num_shards:
        print("[DEFECT OBSERVED] The hot profile-lookup query broadcasts to all "
              "10 shards instead of targeting the one shard that owns the tenant.")
    else:
        print("No defect observed.")

if __name__ == "__main__":
    reproduce_defect()
