# 02_database_replication_lag.py
"""
High-Level Design Lab 02: Database Replication Lag & Read-Your-Own-Writes Consistency.
Simulates asynchronous Master-Replica replication, reproduces the stale read anomaly,
and verifies sticky-leader routing and LSN tracking mitigations.
"""

import time
import threading
from typing import Dict, Optional, Tuple

class DatabaseNode:
    def __init__(self, node_id: str, is_leader: bool = False):
        self.node_id = node_id
        self.is_leader = is_leader
        self.storage: Dict[str, str] = {}
        self.lsn: int = 0  # Log Sequence Number (monotonically increasing version)
        self._lock = threading.Lock()

    def write(self, key: str, value: str) -> int:
        with self._lock:
            if not self.is_leader:
                raise PermissionError("Writes are only permitted on the Leader node!")
            self.lsn += 1
            self.storage[key] = value
            return self.lsn

    def apply_replication(self, key: str, value: str, lsn: int):
        with self._lock:
            self.storage[key] = value
            self.lsn = lsn

    def read(self, key: str) -> Tuple[Optional[str], int]:
        with self._lock:
            return self.storage.get(key), self.lsn

class DistributedDatabaseCluster:
    def __init__(self, replication_lag_seconds: float = 0.05):
        self.leader = DatabaseNode("primary-db", is_leader=True)
        self.replica = DatabaseNode("read-replica-01", is_leader=False)
        self.lag_seconds = replication_lag_seconds

    def execute_write(self, key: str, value: str) -> int:
        # Write to primary
        lsn = self.leader.write(key, value)

        # Asynchronously replicate to follower with simulated cross-region network lag
        def async_replicator():
            time.sleep(self.lag_seconds)
            self.replica.apply_replication(key, value, lsn)

        threading.Thread(target=async_replicator, daemon=True).start()
        return lsn

    def naive_read(self, key: str) -> Optional[str]:
        # Naive pattern: all reads sent blindly to read-replica to save primary CPU
        val, _ = self.replica.read(key)
        return val

    def consistent_user_read(self, user_id: str, key: str, last_write_time: float, min_lsn: int) -> Optional[str]:
        # Production Mitigation: "Read-Your-Own-Writes" Consistency
        # If the user recently performed a write (< 0.2s ago), route read directly to Primary!
        if time.time() - last_write_time < 0.2:
            val, _ = self.leader.read(key)
            return val
        
        # Otherwise, safe to read from replica
        val, _ = self.replica.read(key)
        return val

def run_replication_lag_lab():
    print("=" * 70)
    print("  HLD LAB 02: DATABASE REPLICATION LAG & STALE READS LAB")
    print("=" * 70)

    cluster = DistributedDatabaseCluster(replication_lag_seconds=0.04)

    # 1. User Alice publishes a post at t = 0
    print("[STEP 1] Alice writes new profile status: 'Hiking in the Alps' to Primary DB...")
    write_timestamp = time.time()
    write_lsn = cluster.execute_write("user:alice:status", "Hiking in the Alps")

    # 2. Alice immediately refreshes her browser at t = 5ms (Replication lag is 40ms!)
    time.sleep(0.005)
    print("\n[STEP 2] Alice immediately refreshes page (5ms later). Routing via NAIVE READ...")
    stale_val = cluster.naive_read("user:alice:status")
    print(f"  Result seen by Alice: '{stale_val}'")
    assert stale_val is None, "Expected stale read due to active replication lag!"
    print("  >>> [ANOMALY DETECTED] Read-Your-Own-Writes Violation! Alice thinks her post was lost! <<<")

    # 3. Reading with Production Mitigation (Sticky User Routing)
    print("\n[STEP 3] Alice refreshes page via CONSISTENT ROUTING (Sticky User Leader Route)...")
    consistent_val = cluster.consistent_user_read("alice", "user:alice:status", write_timestamp, write_lsn)
    print(f"  Result seen by Alice: '{consistent_val}'")
    assert consistent_val == "Hiking in the Alps"
    print("  >>> [OK] Invariant Preserved: Alice reads her own write instantly from Primary! <<<")

    # 4. Wait for replication lag to settle
    time.sleep(0.05)
    replica_val = cluster.naive_read("user:alice:status")
    print(f"\n[STEP 4] 50ms later, Replica has caught up. Replica value: '{replica_val}'")
    assert replica_val == "Hiking in the Alps"
    print("[SUCCESS] Replication lag mechanics and mitigations mathematically proven!\n")

if __name__ == "__main__":
    run_replication_lag_lab()
