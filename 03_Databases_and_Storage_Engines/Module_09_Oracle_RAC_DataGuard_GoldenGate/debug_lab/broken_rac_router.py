"""DEBUG LAB: Interconnect Saturation Due to Unpartitioned Workload

THIS FILE CONTAINS AN INTENTIONAL PRODUCTION DEFECT.
Analyze the symptoms in SYMPTOMS.md, identify the root cause, and fix the defect.
"""

from __future__ import annotations

class RacCluster:
    """A toy 2-node RAC cluster tracking Cache Fusion block transfers."""

    def __init__(self) -> None:
        self.block_owner: dict[int, int] = {}
        self.fusion_transfers = 0

    def touch(self, node: int, block_id: int) -> None:
        owner = self.block_owner.get(block_id)
        if owner is not None and owner != node:
            self.fusion_transfers += 1  # block pinged across the private interconnect
        self.block_owner[block_id] = node

def route_unpartitioned(tx_id: int) -> int:
    """Load-balances transactions round-robin, ignoring which data they touch."""
    return tx_id % 2

def reproduce_defect() -> None:
    print("Routing 2,000 transactions round-robin across a 2-node RAC cluster...")
    cluster = RacCluster()
    for tx_id in range(2000):
        node = route_unpartitioned(tx_id)
        block_id = tx_id % 49  # every account lives in one of only 49 hot blocks
        cluster.touch(node, block_id)

    expected_max = 100  # node-affinity routing keeps cross-node transfers bounded
    print(f"Cache Fusion transfers over the private interconnect: {cluster.fusion_transfers}")
    print(f"Expected upper bound with affinity-based routing: {expected_max}")
    if cluster.fusion_transfers > expected_max:
        print("[DEFECT OBSERVED] Round-robin routing keeps handing the same hot "
              "blocks to alternating nodes, saturating the interconnect with pings.")
    else:
        print("No defect observed.")

if __name__ == "__main__":
    reproduce_defect()
