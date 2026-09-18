# Debug Lab Solution & Forensic Post-Mortem

## Incident: CROSSSLOT Keys in Request Don't Hash to the Same Slot

---

### 🔍 Forensic Root Cause Analysis
`mget_naive()` determines a single "target node" from the first key only, then
queries that one node for every key in the request. `user:101:profile` and
`user:101:cart` hash (via CRC16-style slotting) to different slots that happen
to live on different nodes, since Redis Cluster hashes each key independently
unless a hash tag forces them together. The second key is silently looked up
on the wrong node and returns `None`, instead of the client raising CROSSSLOT
or routing each key to its correct owner.

---

### 🛠️ Production Corrective Action & Code Fix

```python
def mget_safe(cluster, keys):
    """Route every key to the node that actually owns its slot, or use a
    hash tag ("{user:101}:profile") so related keys are colocated on purpose."""
    return [cluster.nodes[cluster.node_for(k)].get(k) for k in keys]
```

The idiomatic Redis Cluster fix is a **hash tag**: naming the keys
`{user:101}:profile` and `{user:101}:cart` forces the cluster to hash only the
`{user:101}` portion, guaranteeing both land in the same slot and can be
fetched together in one `MGET`.

---

### 🛡️ Production Prevention Invariants
1. **Hash-tag any keys that must be read together** in a single multi-key command.
2. **Use a cluster-aware client** that raises CROSSSLOT loudly rather than
   silently querying the wrong node.
3. **Integration tests against a real (or simulated) multi-node cluster**, not
   just a single-node Redis, for any code using multi-key commands.
