# Debug Lab Solution & Forensic Post-Mortem

## Incident: Split-Brain Dual Leader Election in Raft Cluster

---

### 🔍 Forensic Root Cause Analysis
`wins_election()` checks `votes_received >= 2`, a constant, instead of
computing the majority for the cluster's actual size. In a 5-node cluster the
majority is `5 // 2 + 1 = 3`. Node A's 2 votes are not a majority of 5, yet
the fixed threshold lets it declare itself leader anyway. Because Node B
separately and correctly reaches 3 votes and also becomes leader, the cluster
ends up with two simultaneous leaders in the same term, each free to commit
conflicting values at the same log index.

---

### 🛠️ Production Corrective Action & Code Fix

```python
def wins_election(votes_received, cluster_size):
    """Majority must scale with cluster size: floor(N/2) + 1, never a constant."""
    majority = cluster_size // 2 + 1
    return votes_received >= majority
```

Applied to the reproduction: with `cluster_size=5`, node A's 2 votes no longer
satisfy `>= 3`, so it correctly stays a candidate/follower and only node B
becomes leader -- no split brain, no divergent commits.

---

### 🛡️ Production Prevention Invariants
1. **Quorum size must always be derived from live cluster membership**, never
   hardcoded, and recomputed on every membership change.
2. **Term-based fencing:** a node must step down immediately on observing a
   higher term, and followers must never accept two leaders in one term.
3. **Consensus protocol conformance tests (Jepsen-style)** that inject
   partitions and assert only one leader per term is ever observed.
