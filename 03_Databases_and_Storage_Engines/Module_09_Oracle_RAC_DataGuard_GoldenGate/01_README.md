# Module 09: Oracle High Availability – RAC, Data Guard & GoldenGate

> **Brand new to this topic?** Start with [`00_FOUNDATIONS_PLAYGROUND.md`](00_FOUNDATIONS_PLAYGROUND.md) - the same ideas in
> plain language, with runnable standard-library code you can execute right now.
> No Docker, no server, no `pip install`.

Welcome to **Module 09**. In this module, you will master the enterprise-tier high availability (HA) and disaster recovery (DR) stack of Oracle: **Real Application Clusters (RAC)**, **Active Data Guard**, and **GoldenGate**.

---

## ⚡ 1. Oracle Real Application Clusters (RAC) & Cache Fusion

Most distributed databases use a **Shared-Nothing** architecture (each server has its own private CPU, RAM, and Disk). Oracle RAC uses a **Shared-Everything (Shared-Disk)** architecture:
- Multiple independent server nodes (each running their own Oracle instance with private SGA) access the **same shared SAN/NAS disk array**.
- If Node 1 fails, Node 2, 3, and 4 continue running with zero downtime and zero data loss.

```
       [Client Connections]              [Client Connections]
                 │                                 │
                 ▼                                 ▼
         ┌───────────────┐                 ┌───────────────┐
         │  RAC Node 1   │                 │  RAC Node 2   │
         │  (Instance 1) │                 │  (Instance 2) │
         │  [SGA Cache]  │                 │  [SGA Cache]  │
         └───────┬───────┘                 └───────┬───────┘
                 │                                 │
                 │◄── CACHE FUSION INTERCONNECT ──►│ (100 Gbps RoCE / InfiniBand)
                 │    (Dirty block transfer in RAM)│
                 │                                 │
                 └───────────────┬─────────────────┘
                                 ▼
                     ┌───────────────────────┐
                     │   SHARED STORAGE      │
                     │  (ASM / SAN / NVMe)   │
                     └───────────────────────┘
```

### The Magic of Cache Fusion
In older clustering technologies, if Node 1 updated Block #42 and Node 2 needed to read it:
1. Node 1 had to force DBWn to write Block #42 to physical disk.
2. Node 2 then had to read Block #42 from physical disk (incurring 10–20ms of disk I/O).

**Cache Fusion**: Managed by the **Global Cache Service (GCS)**, Node 1 sends the dirty data block directly across the private InfiniBand/Ethernet interconnect to Node 2's buffer cache in **microseconds** via RDMA (Remote Direct Memory Access), **completely bypassing physical disk writes**!

---

## 🛡️ 2. Disaster Recovery: Oracle Active Data Guard

While RAC protects against individual server hardware crashes within a single datacenter, **Active Data Guard** protects against regional datacenter disasters (floods, earthquakes, regional power outages).

### Architecture & Redo Transport
- **Primary Database**: Ingests production transactions and writes to local Online Redo Logs.
- **Redo Transport Service (NSS)**: Streams redo vectors over WAN to the remote standby datacenter.
- **Remote File Server (RFS)**: Standby background process that receives redo and writes to Standby Redo Logs.
- **Managed Recovery Process (MRP)**: Continuously applies redo to the standby datafiles in real-time.

```
[Primary Datacenter: London]                     [Standby Datacenter: Dublin]
┌───────────────────────────────┐               ┌───────────────────────────────┐
│ Primary Instance              │               │ Active Data Guard Standby     │
│  ├── User Writes              │               │  ├── MRP (Redo Apply)         │
│  └── LGWR -> Redo Log Buffer  │               │  └── Read-Only Reporting Open │
└───────────────┬───────────────┘               └───────────────▲───────────────┘
                │                                               │
                ▼ (NSS / TCP Network)                           ▼ (RFS)
         [Redo Transport] ──────────────────────────────► [Standby Redo Logs]
```

### Data Guard Protection Modes
1. **Maximum Protection**: Strict Zero Data Loss. Redo must be confirmed committed on both Primary and Standby before the user's `COMMIT` completes. If the network link drops, the **Primary database halts completely**!
2. **Maximum Availability** (Enterprise Standard): Operates identically to Maximum Protection during normal network health. If the standby becomes unreachable, the primary automatically downgrades to asynchronous mode to preserve availability.
3. **Maximum Performance**: Fully asynchronous. Redo is shipped in background. Offers lowest latency for the primary, but risks seconds of data loss (RPO) during catastrophic failover.

---

## 🔁 3. Heterogeneous CDC: Oracle GoldenGate

Unlike Data Guard (which replicates at the physical block level and mirrors the exact binary database), **Oracle GoldenGate** performs decoupled **logical Change Data Capture (CDC)**:
- **Extract**: Tails transaction logs in real time, parses row changes, and writes to binary **Trail Files**.
- **Data Pump**: Ships Trail Files over TCP.
- **Replicat**: Reads Trail Files and executes corresponding SQL DML against any target engine (Oracle, PostgreSQL, Kafka, BigQuery, Snowflake).
- Enables **Zero-Downtime Database Migrations** and real-time streaming into data lakes.

---

## 5. Dual-Track Curriculum: Track A (Simulation) vs Track B (Real Operations)

This module implements a rigorous **dual-track architecture** guaranteeing both first-principles mechanistic understanding and battle-tested production operational skills:

| Dimension | Track A: Mechanistic Model | Track B: Live Engine Operations |
| :--- | :--- | :--- |
| **Location** | `project_solution/oracle_rac_engine.py` | `project_solution/*_live.py` |
| **Focus** | Internal algorithms & data structures | Real drivers, pooling, and production operations |
| **Technology** | oracle_rac_engine.py (Cache Fusion & Data Guard SCN replicator) | oracle_ha_live.py (python-oracledb, v$database, gv$instance) |
| **Verification** | `project_solution/test_oracle_rac_engine.py` | `project_solution/test_*_live.py` |
| **Offline Support** | 100% in-process with 0 external dependencies | Safe skips via `@pytest.mark.skipif` when offline |

### Reconciliation Contract
A dedicated reconciliation suite guarantees that the internal algorithmic model and the real live production driver strictly agree on core operational semantics, invariants, and expected outcomes.

---

## 6. Production Failure Modes & Operational Pitfalls

Every production engineer must understand how this database layer fails under extreme stress:

1. Interconnect Cache Fusion Pinging: Concurrent cross-node writes to the same blocks saturate private interconnect RAM.
2. Standby Transport Lag: Network bandwidth bottlenecks cause Active Data Guard to lag behind primary transaction streams.
3. Split-Brain Node Isolation: Loss of private interconnect without proper voting disk quorum causes cluster eviction stalls.

For complete diagnosis runbooks, error codes, and step-by-step resolution strategies, consult:
👉 **[TROUBLESHOOTING_AND_EDGE_CASES.md](06_TROUBLESHOOTING_AND_EDGE_CASES.md)**

---

## 7. When NOT to Use (Trade-offs & Anti-Patterns)

> [!WARNING]
> Architecture is the art of trade-offs. No database technology is universally optimal.

Do NOT stretch Oracle RAC clusters across high-latency WANs (use Active Data Guard or GoldenGate for cross-region replication instead).

---

## 8. Essential Production CLI & Query Playbook

Key operational diagnostic commands to verify health and diagnose performance:

```bash
# Verify environment and execute automated test suite
pytest Module_09_Oracle_RAC_DataGuard_GoldenGate -v

# Operational Diagnostics & Health Verification
sqlplus system/oracle@localhost:1521/FREEPDB1 <<EOF
SELECT inst_id, instance_name, status FROM gv\$instance;
SELECT protection_mode, open_mode FROM v\$database;
EXIT;
EOF
```

---

## 9. Next Steps & Pedagogical Resources

Accelerate your mastery using the structured pedagogical artifacts in this module:
1. 📓 **[Interactive Jupyter Lab](02_interactive_oracle_ha.ipynb)**: Hands-on sandbox for interactive exploration.
2. 🎯 **[3-Tier Guided Project](04_PROJECT_GUIDE.md)**: Novice, Core, and Architect implementation tracks.
3. 🛠️ **[Troubleshooting Guide](06_TROUBLESHOOTING_AND_EDGE_CASES.md)**: Real production error signatures & fixes.
4. 🧠 **[Self-Assessment Quiz](05_SELF_ASSESSMENT_AND_CHALLENGES.md)**: 10 diagnostic questions + coding challenges.
5. 🔬 **[Debug Lab](debug_lab/)**: Forensic debugging exercise diagnosing real production bugs.
### Oracle High Availability Deep-Dive: Redo Apply vs SQL Apply
- **Physical Standby (Redo Apply):** Active Data Guard applies exact block-level redo vectors via media recovery (`MRP0`), maintaining bit-for-bit parity.
- **Logical Standby (SQL Apply):** Data Guard converts redo vectors back into SQL transactions via LogMiner (`LSP0`), allowing open read/write tables.
- **Fast-Start Failover (FSFO):** Automates zero-touch failover to standby within seconds when primary crash is confirmed by an independent observer process.
