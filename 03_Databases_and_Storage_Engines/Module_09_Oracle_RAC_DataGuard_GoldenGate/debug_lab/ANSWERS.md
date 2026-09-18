# Debug Lab Solution & Forensic Post-Mortem

## Incident: Interconnect Saturation Due to Unpartitioned Workload

---

### 🔍 Forensic Root Cause Analysis
`route_unpartitioned()` assigns each transaction to a node purely by
round-robin (`tx_id % 2`), with no regard for which account block the
transaction touches. Because the same set of hot blocks is revisited by both
nodes in quick succession, ownership of each block ping-pongs between the two
instances constantly. Every time a block's cached copy is needed by the node
that doesn't currently own it, RAC's Cache Fusion protocol must ship it across
the private interconnect -- and with unpartitioned round-robin routing, that
happens on almost every transaction.

---

### 🛠️ Production Corrective Action & Code Fix

```python
def route_by_affinity(block_id, num_nodes=2):
    """Route by the data being touched, not by an unrelated counter, so a given
    block is consistently served by the same node."""
    return block_id % num_nodes
```

Applied to the reproduction: routing each transaction by `block_id % 2`
instead of `tx_id % 2` means every hot block is always processed by the same
node, so ownership never has to move across the interconnect.

---

### 🛡️ Production Prevention Invariants
1. **Affinity-based (data-aware) routing** at the connection pool / middle
   tier for any RAC workload with hot, reused rows.
2. **Monitor `gc cr/current block` wait events** and alert when Cache Fusion
   traffic exceeds a baseline.
3. **Partition genuinely hot ranges** across services/schemas where affinity
   routing alone isn't enough.
