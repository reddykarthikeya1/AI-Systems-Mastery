# Module 16 Neo4j Graph Databases Cypher: Troubleshooting & Production Edge Cases

This guide documents the most common production traps, failure modes, error codes, and operational edge cases in **Graph Databases: Neo4j & Declarative Cypher**, complete with root cause analysis and step-by-step resolution runbooks.

---

## 1. Cypher Cartesian Product & Memory Exhaustion

### 🚨 Symptom
> A MATCH query with multiple unconnected patterns causes OutOfMemoryError and crashes the Neo4j instance.

### 🔍 Root Cause Analysis
Writing `MATCH (a:Person), (b:Company)` without an explicit relationship pattern causes Neo4j to evaluate all possible pairs ($N \times M$ Cartesian product).

### 🛠️ Production Fix & Mitigation Runbook
Ensure patterns are connected, or use `WITH a MATCH (b) WHERE ...` to sequence intermediate bindings and use `LIMIT`.

---

## 2. Supernode Graph Traversal Stalls

### 🚨 Symptom
> Traversing relationships from a popular entity (e.g. an account with 5,000,000 followers) takes 30 seconds.

### 🔍 Root Cause Analysis
A 'supernode' has millions of relationship pointers. Traversing incoming/outgoing relationships requires scanning all pointers in RAM.

### 🛠️ Production Fix & Mitigation Runbook
Use direction-specific and typed relationship traversals (`-[:DIRECTED_EDGE]->`), or create intermediate relationship category nodes to shard the fan-out.

---

## 3. Missing Schema Index Causing Node Scan in Cypher

### 🚨 Symptom
> Cypher execution plan shows `NodeByLabelScan` examining 5,000,000 nodes instead of `NodeIndexSeek`.

### 🔍 Root Cause Analysis
No index or unique constraint exists on the lookup property.

### 🛠️ Production Fix & Mitigation Runbook
Create an index: `CREATE INDEX FOR (p:Person) ON (p.ssn);` and profile queries using `PROFILE MATCH ...`.

---

## 5-Minute Production Triage Checklist

When encountering latency spikes, transaction rollbacks, or service degradation in this domain:
1. **Check Connection Pools:** Verify active vs idle connection ratios and eliminate thread starvation.
2. **Examine Wait Events:** Inspect query wait states (`pg_stat_activity`, `SHOW PROCESSLIST`, `v$session_wait`) to identify lock contention.
3. **Validate Memory & Disk:** Monitor swap usage, buffer cache hit ratios, and disk I/O queue depths.
4. **Audit Stale Snapshots:** Terminate lingering idle-in-transaction connections holding back cleanup or replication.
