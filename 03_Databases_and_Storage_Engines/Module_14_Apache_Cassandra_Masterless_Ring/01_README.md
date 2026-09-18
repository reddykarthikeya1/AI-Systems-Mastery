# Module 14: Apache Cassandra & ScyllaDB — Masterless Ring, Murmur3 & Tunable Consistency

> **Brand new to this topic?** Start with [`00_FOUNDATIONS_PLAYGROUND.md`](00_FOUNDATIONS_PLAYGROUND.md) - the same ideas in
> plain language, with runnable standard-library code you can execute right now.
> No Docker, no server, no `pip install`.

Welcome to **Module 14**. In this module, you will master **Apache Cassandra and ScyllaDB** — the premier distributed wide-column database engines powering global linear scale, zero-single-point-of-failure architectures, and high-throughput write workloads across companies like Netflix, Apple, Uber, and Discord.

---

## ⭕ 1. The Masterless Peer-to-Peer Ring Architecture

Traditional databases (PostgreSQL, MySQL, MongoDB) rely on hierarchical topologies with explicit Primary/Replica roles. In Cassandra, **every single node is completely equal**:
- **No Master / Worker Dichotomy**: There is no dedicated master to elect or fail over. Any node can accept any read or write request from any client.
- **The Coordinator Node**: The specific node contacted by the client acts as the temporary **Coordinator** for that transaction. The coordinator computes where data lives, broadcasts write/read requests to the responsible replica nodes, awaits quorum responses, and returns the result to the client.

```
                         [Node 1] (Token: -4611686018427387904)
                        /        \
                       /          \
     [Node 4] ────────             ──────── [Node 2]
  (Token: 4611686018427387903)          (Token: 0)
                       \          /
                        \        /
                         [Node 3] (Token: -1)
```

### The Murmur3 Token Ring
Cassandra maps partitions across the cluster using **Consistent Hashing**:
- **Murmur3Partitioner**: Hashes the partition key into a signed 64-bit integer:
  $$\text{Token} \in [-2^{63}, 2^{63} - 1] \quad (-9,223,372,036,854,775,808 \text{ to } 9,223,372,036,854,775,807)$$
- The ring is circular. A row belongs to the first node whose assigned token is greater than or equal to the row's token.
- **Virtual Nodes (vnodes)**: Instead of assigning 1 token per physical server, each physical machine hosts multiple (e.g. 128 or 256) small tokens distributed across the ring. When a new node joins or an old node dies, data streams evenly across the entire cluster rather than placing 100% of the burden onto immediate neighbor nodes.

### Gossip Protocol & Failure Detection
Nodes exchange health state every 1 second over port 7000 using an epidemic **Gossip Protocol**:
- **Phi ($\Phi$) Accrual Failure Detector**: Rather than using a binary timeout ("is node dead or alive?"), Cassandra calculates a continuous scale of suspicion $\Phi$ based on historical heartbeat arrival times. Network latency spikes result in low $\Phi$ values, while complete node crashes drive $\Phi$ exponentially higher, triggering node avoidance without false alarms.

---

## 🧱 2. Wide-Column Data Modeling: Partition Keys vs Clustering Columns

In relational databases, you design normalized schemas and use `JOIN`s at query time. In Cassandra, **you model strictly around your query access patterns**. Joining tables at scale across hundreds of distributed network nodes is impossible.

### The Compound Primary Key Layout
```sql
CREATE TABLE sensor_readings (
    device_id       uuid,
    facility_id     text,
    recorded_at     timestamp,
    reading_value   double,
    status          text,
    PRIMARY KEY ((facility_id, device_id), recorded_at)
) WITH CLUSTERING ORDER BY (recorded_at DESC);
```

1. **Partition Key (`(facility_id, device_id)`)**:
   - Passed through Murmur3 to generate the ring token.
   - Determines **which physical nodes** in the cluster will store the partition.
   - Compound partition keys allow multi-attribute sharding.
2. **Clustering Columns (`recorded_at`)**:
   - Determines the **physical sort order of rows on disk** inside that specific partition's SSTables.
   - Allows lightning-fast binary searches and range queries (`WHERE facility_id = ? AND device_id = ? AND recorded_at > ?`).

> [!WARNING]
> **The `ALLOW FILTERING` Trap**: In Cassandra, querying columns that are not part of the Partition Key or Clustering Prefix forces a full cluster table scan (scatter-gather across every node). Running `ALLOW FILTERING` in production is a fatal antipattern that causes catastrophic latency spikes and cluster timeouts.

---

## ⚖️ 3. Tunable Consistency & The Quorum Equation

Cassandra is fundamentally an **AP system** under Eric Brewer's CAP Theorem (Available and Partition-tolerant), but it offers **tunable consistency** on a per-query basis:

### The Strict Quorum Math
To guarantee **Strong Consistency** (linearizable reads where you are guaranteed to read the latest written version of a row), your read and write consistency levels must overlap:
$$R + W > N$$
Where:
- $N$ = Replication Factor (e.g., $N = 3$ replicas).
- $W$ = Number of replicas that must acknowledge a write before success.
- $R$ = Number of replicas that must respond to a read before returning data.

| Write Level ($W$) | Read Level ($R$) | Equation ($R + W$) | Consistency Guarantee |
| :--- | :--- | :--- | :--- |
| `QUORUM` (2) | `QUORUM` (2) | $2 + 2 = 4 > 3$ | **Strong Consistency** (Zero stale reads) |
| `ALL` (3) | `ONE` (1) | $1 + 3 = 4 > 3$ | **Strong Consistency** (Expensive writes) |
| `ONE` (1) | `ALL` (3) | $3 + 1 = 4 > 3$ | **Strong Consistency** (Fast writes, slow reads) |
| `ONE` (1) | `ONE` (1) | $1 + 1 = 2 \ngtr 3$ | **Eventual Consistency** (Risk of stale reads) |
| `QUORUM` (2) | `ONE` (1) | $1 + 2 = 3 \ngtr 3$ | **Eventual Consistency** (Risk of stale reads) |

### Calculating Quorum
$$\text{QUORUM} = \left\lfloor \frac{N}{2} \right\rfloor + 1$$
For $N = 3$, $\text{QUORUM} = 2$. For $N = 5$, $\text{QUORUM} = 3$.
- `LOCAL_QUORUM`: Requires quorum only within the local data center, eliminating cross-datacenter WAN latency while preserving strong consistency locally.

---

## ⚔️ 4. Conflict Resolution, Tombstones & Anti-Entropy

Because multiple replicas can accept writes concurrently without locks:
1. **Last-Write-Wins (LWW)**: Every write is timestamped with microsecond precision. If two writes conflict, the mutation with the highest timestamp silently overwrites the older one. (Warning: NTP clock drift can cause newer writes to be dropped!).
2. **Tombstones & Deletions**: Because SSTables are immutable, deletions do **not** erase data on disk immediately. Instead, Cassandra appends a special record called a **Tombstone** containing a deletion timestamp.
   - Tombstones survive for `gc_grace_seconds` (default 10 days) to ensure disconnected replicas receive the deletion marker before it is physically purged during compaction.
   - If an application queries a range containing millions of tombstones, Cassandra raises a `TombstoneOverwhelmingException` to prevent out-of-memory crashes.
3. **Anti-Entropy Repairs**:
   - **Read Repair**: When a coordinator reads at `QUORUM`, if replica data checksums differ, the coordinator reads full rows, detects the stale replica via LWW, writes the latest data back to the stale replica, and returns the fresh value.
   - **Merkle Tree Active Repair (`nodetool repair`)**: Replicas generate cryptographic Merkle trees (hash trees) of their token ranges and exchange tree leaves to pinpoint and stream only diverging rows without full table copies.

---

## ⚡ 5. The ScyllaDB Evolution: Thread-per-Core Architecture

Cassandra is implemented in Java, which historically suffers from:
- **JVM Garbage Collection (GC) Pauses**: Stop-the-world GC pauses causing multi-second latency spikes.
- **Linux OS Context Switching**: Thread pool contention across hundreds of concurrent query threads.

**ScyllaDB** is a drop-in C++ replacement for Cassandra built on the **Seastar Framework**:
- **Shared-Nothing Thread-Per-Core**: ScyllaDB pins one operating system thread to each CPU core. Each core manages its own memory, network queue, and disk I/O with zero cross-core mutexes.
- **Sub-Millisecond Latency at 99th Percentile**: Achieves 10x the throughput of Cassandra per server with flat, predictable P99 latencies under heavy load.

---

## 🛠️ 6. Hands-On Lab: Building a Masterless Cassandra Ring Engine

In this lab, you will implement:
1. **Murmur3 Consistent Hashing Ring**: Map partition keys across a simulated 64-bit token ring with Virtual Nodes (vnodes).
2. **Coordinator Routing & Replica Selection**: Identify natural replica endpoints for any given partition key using Replication Factor ($N$).
3. **Tunable Quorum Read/Write Engine**: Enforce consistency levels (`ONE`, `QUORUM`, `ALL`) and prove mathematically when $R + W > N$ eliminates stale reads.
4. **Last-Write-Wins (LWW) Conflict Resolution & Tombstones**: Resolve conflicting writes via microsecond timestamps and handle soft-deletion markers.

---

## 📂 Project Structure
```
Module_14_Apache_Cassandra_Masterless_Ring/
├── README.md
├── 01_cassandra_ring_and_quorum_demo.py
├── starter/
│   └── cassandra_ring_engine.py
└── project_solution/
    ├── cassandra_ring_engine.py
    └── test_cassandra_ring_engine.py
```

---
## 5. Dual-Track Curriculum: Track A (Simulation) vs Track B (Real Operations)

This module implements a rigorous **dual-track architecture** guaranteeing both first-principles mechanistic understanding and battle-tested production operational skills:

| Dimension | Track A: Mechanistic Model | Track B: Live Engine Operations |
| :--- | :--- | :--- |
| **Location** | `project_solution/cassandra_ring_engine.py` | `project_solution/*_live.py` |
| **Focus** | Internal algorithms & data structures | Real drivers, pooling, and production operations |
| **Technology** | cassandra_ring_engine.py (Token ring, consistent hashing, quorum) | cassandra_live.py (cassandra-driver, CQL queries, tunable consistency) |
| **Verification** | `project_solution/test_cassandra_ring_engine.py` | `project_solution/test_*_live.py` |
| **Offline Support** | 100% in-process with 0 external dependencies | Safe skips via `@pytest.mark.skipif` when offline |

### Reconciliation Contract
A dedicated reconciliation suite guarantees that the internal algorithmic model and the real live production driver strictly agree on core operational semantics, invariants, and expected outcomes.

---

## 6. Production Failure Modes & Operational Pitfalls

Every production engineer must understand how this database layer fails under extreme stress:

1. Tombstone Overload: Frequent deletions creating millions of tombstones that abort subsequent range scans.
2. Hot Partitions: Choosing low-cardinality partition keys concentrating gigabytes of writes onto a single physical node.
3. Write Timeout on ALL: Using ConsistencyLevel.ALL causing write failure whenever a single node undergoes restart.

For complete diagnosis runbooks, error codes, and step-by-step resolution strategies, consult:
👉 **[TROUBLESHOOTING_AND_EDGE_CASES.md](06_TROUBLESHOOTING_AND_EDGE_CASES.md)**

---

## 7. When NOT to Use (Trade-offs & Anti-Patterns)

> [!WARNING]
> Architecture is the art of trade-offs. No database technology is universally optimal.

Do NOT use Apache Cassandra as an ACID queue or run queries requiring ad-hoc JOINs, aggregations, or unpartitioned secondary index searches.

---

## 8. Essential Production CLI & Query Playbook

Key operational diagnostic commands to verify health and diagnose performance:

```bash
# Verify environment and execute automated test suite
pytest Module_14_Apache_Cassandra_Masterless_Ring -v

# Operational Diagnostics & Health Verification
cqlsh localhost 9042 -e "DESCRIBE KEYSPACES;"
nodetool status
nodetool info
```

---

## 9. Next Steps & Pedagogical Resources

Accelerate your mastery using the structured pedagogical artifacts in this module:
1. 📓 **[Interactive Jupyter Lab](02_interactive_cassandra_ring.ipynb)**: Hands-on sandbox for interactive exploration.
2. 🎯 **[3-Tier Guided Project](04_PROJECT_GUIDE.md)**: Novice, Core, and Architect implementation tracks.
3. 🛠️ **[Troubleshooting Guide](06_TROUBLESHOOTING_AND_EDGE_CASES.md)**: Real production error signatures & fixes.
4. 🧠 **[Self-Assessment Quiz](05_SELF_ASSESSMENT_AND_CHALLENGES.md)**: 10 diagnostic questions + coding challenges.
5. 🔬 **[Debug Lab](debug_lab/)**: Forensic debugging exercise diagnosing real production bugs.

