"""Beginner playground for Module 09 - Oracle RAC, Data Guard and GoldenGate.

    python 00_try_it_yourself.py

Standard library only. Every block here also appears in 00_W3_BEGINNER_PLAYGROUND.md;
both files are generated from one source, so they cannot drift apart.

Read the printed output alongside the markdown page. The `assert` lines are the
interesting part: each one is a claim the page makes, checked as it runs.
"""
from __future__ import annotations

# ------------------------------------------------- 1. Two different disasters
shared_storage = {"balance": 1000}
rac_nodes = ["node1", "node2", "node3"]
alive = set(rac_nodes)


def serve(node, delta):
    if node not in alive:
        return None
    shared_storage["balance"] += delta
    return shared_storage["balance"]


print("node1 serves a request:", serve("node1", 100))
alive.remove("node1")
print("node1 has died. node2 serves the next request:", serve("node2", 100))
assert shared_storage["balance"] == 1200, "the data was never on node1 - it is on the SAN"
print("RAC survives a NODE failure because the data was never on the node.")


# ----------------------------------------------------- 2. Why RAC is not free
block_owner = {}
interconnect_transfers = {"count": 0}


def node_writes(node, block_id):
    if block_owner.get(block_id) not in (None, node):
        interconnect_transfers["count"] += 1
    block_owner[block_id] = node


for i in range(6):
    node_writes(rac_nodes[i % 3], block_id="hot_counter")
print("all three nodes fighting over one block ->",
      interconnect_transfers["count"], "interconnect transfers")
assert interconnect_transfers["count"] == 5

interconnect_transfers["count"] = 0
block_owner.clear()
for i in range(6):
    node_writes(rac_nodes[i % 3], block_id=f"partition_{i % 3}")
print("each node owning its own partition ->",
      interconnect_transfers["count"], "interconnect transfers")
assert interconnect_transfers["count"] == 0, "no contention, no transfers"


# --------------------------- 3. Data Guard: how much are you willing to lose?
committed_on_primary = []
received_by_standby = []


def commit_transaction(txn, mode):
    if mode == "sync":
        received_by_standby.append(txn)
        committed_on_primary.append(txn)
        return 2.0  # ms: a round trip to the standby, on every commit
    committed_on_primary.append(txn)
    return 0.1  # ms: local only; shipping happens in the background


async_cost = sum(commit_transaction(f"txn{i}", "async") for i in range(5))
print("primary has committed:", committed_on_primary)
print("standby has received: ", received_by_standby)

lost = [t for t in committed_on_primary if t not in received_by_standby]
print("site is destroyed now. Transactions lost:", lost)
assert len(lost) == 5, "async means confirmed-but-not-yet-shipped work can vanish"


# --------------------------- 4. The same five transactions, paid for properly
committed_on_primary.clear()
received_by_standby.clear()
sync_cost = sum(commit_transaction(f"txn{i}", "sync") for i in range(5))

lost_now = [t for t in committed_on_primary if t not in received_by_standby]
print("Transactions lost with synchronous shipping:", lost_now)
assert lost_now == [], "RPO of zero - nothing committed is unprotected"

print(f"commit cost: async {async_cost:.1f} ms total, sync {sync_cost:.1f} ms total")
assert sync_cost > async_cost, "zero data loss is bought with latency, every commit"
print("RPO = how much you may lose. RTO = how long until you are back.")


print()
print("All checks passed.")
