# Module 09 Oracle RAC DataGuard GoldenGate: Self-Assessment & Mastery Challenges

Evaluate your practical and conceptual mastery of **Oracle RAC, Active Data Guard & Real-Time Replication** before proceeding.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **What is Oracle RAC Cache Fusion?** What is Oracle RAC Cache Fusion?
2. **What role does the Global Cache Service (GCS) play in an Oracle RAC cluster?** What role does the Global Cache Service (GCS) play in an Oracle RAC cluster?
3. **What is the difference between Oracle Active Data Guard and standard physical standby?** What is the difference between Oracle Active Data Guard and standard physical standby?
4. **Explain the three Data Guard protection modes: Maximum Protection, Maximum Availability, and Maximum Performance.?** Explain the three Data Guard protection modes: Maximum Protection, Maximum Availability, and Maximum Performance.
5. **What is a Fast Connection Failover (FCF) in Oracle RAC?** What is a Fast Connection Failover (FCF) in Oracle RAC?
6. **What is the difference between a Data Guard Switchover and Failover?** What is the difference between a Data Guard Switchover and Failover?
7. **How does Oracle GoldenGate differ from Data Guard?** How does Oracle GoldenGate differ from Data Guard?
8. **What are RAC Voting Disks used for?** What are RAC Voting Disks used for?
9. **What is an Oracle RAC Service, and why should applications connect to Services rather than SID?** What is an Oracle RAC Service, and why should applications connect to Services rather than SID?
10. **What metric indicates Cache Fusion interconnect saturation?** What metric indicates Cache Fusion interconnect saturation?

---

## Part 2: Answer Key & Detailed Explanations

<details>
<summary><b>Click to expand the Answer Key & Explanations</b></summary>

#### Answer 1:
A technology that transfers data blocks directly between the SGA buffer caches of different cluster instances over high-speed private interconnect RAM, avoiding disk I/O.

#### Answer 2:
GCS tracks block ownership, locks, and cache states across all cluster instances to guarantee cluster-wide cache coherency.

#### Answer 3:
Active Data Guard allows the physical standby database to remain open in Read-Only mode for reporting queries while continuously applying redo in real-time.

#### Answer 4:
Max Protection: Zero data loss, synchronous redo commit on standby; primary halts if standby unreachable. Max Availability: Synchronous commit, downgrades to async if standby fails. Max Performance: Asynchronous redo shipping, zero primary impact.

#### Answer 5:
A mechanism using Oracle Notification Service (ONS) to inform client connection pools immediately when a node crashes, rapidly redirecting sessions without TCP timeouts.

#### Answer 6:
Switchover is a planned, zero-data-loss role reversal between primary and standby; Failover is an emergency promotion of standby following unexpected primary catastrophe.

#### Answer 7:
Data Guard replicates physical block redo for an entire database; GoldenGate performs logical transactional replication across heterogeneous databases and tables.

#### Answer 8:
They determine node membership and cluster quorum, evicting unresponsive nodes during split-brain network failures.

#### Answer 9:
A Service is a logical abstraction representing a workload; it allows load balancing and transparent failover across available cluster instances.

#### Answer 10:
`gc cr request` and `gc buffer busy acquire` wait events in AWR reports.

</details>

---

## Part 3: Architecture & Coding Mastery Challenges

### 🏋️ Challenge 1: Core System Implementation
Simulate multi-node Cache Fusion block contention and measure cross-instance block transfers.

### 🚀 Challenge 2: Architect Stretch Problem
Implement an automated standby lag monitor evaluating RPO compliance across Active Data Guard.

---

## Verification Criteria
- [ ] Answered all 10 diagnostic questions without checking reference notes.
- [ ] Implemented Challenge 1 and validated with automated unit tests.
- [ ] Documented trade-offs and edge case behaviors for Challenge 2.

---

## Part 4: Diagnostic Questions — Read the Symptom, Find the Cause

Recall questions measure reading. These measure diagnosis, which is the skill
that separates intermediate from senior: given code and an observed symptom,
find the cause, name the fix, and know which test would have caught it.

Work each one **before** expanding the answer. Write your diagnosis down first —
reading the answer with an un-committed guess teaches nothing.

### D1. Cache Fusion block ping thrashing across RAC interconnect

```sql
-- Instance 1 and Instance 2 concurrently inserting high-volume orders
-- Primary key generated via standard cached sequence:
CREATE SEQUENCE order_seq INCREMENT BY 1 CACHE 20;
```

**Observed symptom:** Interconnect network saturates; Top Wait Event is `gc current block busy` and `gc buffer busy acquire`; transaction throughput drops by 80%.

**(a)** What is Oracle RAC Cache Fusion, and how does it transfer dirty data blocks between instance buffer caches?

**(b)** Why does a low sequence cache size cause Global Cache Service (GCS) block ping thrashing?

**(c)** How does increasing sequence cache to `CACHE 5000 NOORDER` eliminate interconnect contention?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** Small sequence cache (`CACHE 20`) causes Instance 1 and Instance 2 to constantly fight for exclusive ownership of the sequence data block and index leaf blocks. Cache Fusion must ping the block across the private interconnect on every 20 inserts.

**Fix:** `ALTER SEQUENCE order_seq CACHE 10000 NOORDER;`. Each RAC instance preallocates a large contiguous chunk of numbers locally, completely eliminating cross-instance Cache Fusion block transfers.

</details>

---

### D2. Primary database freeze under Data Guard MAXIMUM PROTECTION

```sql
-- Oracle Data Guard configured with MAXIMUM PROTECTION:
ALTER DATABASE SET STANDBY DATABASE TO MAXIMIZE PROTECTION;
# Network maintenance switch reboot causes a 10-second blip on standby link!
```

**Observed symptom:** The production primary database immediately panics and terminates with `ORA-03113: end-of-file on communication channel`; the entire business platform goes offline.

**(a)** What is the mathematical durability contract of Data Guard MAXIMUM PROTECTION mode?

**(b)** Why is the primary database designed to intentionally crash if the standby cannot acknowledge redo?

**(c)** Which protection mode should be used to guarantee Zero Data Loss (RPO=0) without taking down the primary upon link failure?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** `MAXIMUM PROTECTION` strictly enforces Zero Data Loss ($RPO=0$) under all circumstances. If LGWR cannot synchronously confirm redo receipt on at least one standby database, the primary instance **intentionally terminates** to prevent un-replicated data from ever being committed.

**Fix:** Use `MAXIMUM AVAILABILITY`. In this mode, transactions commit synchronously ($RPO=0$), but if the standby becomes unreachable, the primary automatically downgrades to asynchronous mode to preserve cluster uptime, resynchronizing upon reconnection.

</details>

---

### D3. Private interconnect split-brain node eviction

```python
# Switch configuration error on private RAC cluster heartbeat interface:
# Heartbeat packets delayed by 32 seconds (exceeding misscount threshold)
```

**Observed symptom:** Node 2 abruptly reboots; alert.log reports `CRS-1607: Node 2 was evicted by CSS daemon; voting disk lease expired`.

**(a)** What role do Voting Disks and the Cluster Synchronization Service (CSS) play in Oracle RAC split-brain prevention?

**(b)** Why must a partitioned node commit 'fencing' (reboot) when it loses quorum?

**(c)** How do redundant dedicated NICs and LACP network bonding prevent spurious evictions?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** If heartbeat communication is interrupted between nodes, each partition could attempt to access shared SAN/NAS disks independently, causing catastrophic filesystem and database corruption. The CSS daemon uses Voting Disks to determine majority quorum; the minority partition is forcefully evicted (fenced) via reboot.

**Hardware Fix:** Configure redundant dedicated private network interfaces with LACP bonding on independent physical switches, ensuring no single network cable or switch failure drops the cluster interconnect.

</details>

---

### D4. Active Data Guard read-only standby ORA-01555 Snapshot Too Old

```sql
-- Analytical query running on Active Data Guard read-only replica:
SELECT * FROM financial_ledger WHERE fiscal_year = 2025; -- Takes 45 minutes
-- Primary database commits millions of small updates and purges undo
```

**Observed symptom:** Standby reporting query crashes after 30 minutes with `ORA-01555: snapshot too old: rollback segment number 12 with name '_SYSSMU12$' too small`.

**(a)** Why does a query on a read-only standby database require undo segments generated on the primary?

**(b)** What happens when the primary database overwrites old undo blocks before the standby query finishes?

**(c)** What setting on the primary database (`UNDO_RETENTION`) prevents premature undo overwrite?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** Under MVCC, long-running queries must reconstruct past image blocks using undo data. On Active Data Guard, queries use the standby's replicated undo stream. If high transaction volume on the primary causes undo blocks to be overwritten before the standby query completes, reconstruction fails with `ORA-01555`.

**Fix:** Increase `UNDO_RETENTION` on both primary and standby (e.g. `UNDO_RETENTION = 14400` for 4 hours) and enable `RETENTION GUARANTEE` on the undo tablespace.

</details>

---

### D5. GoldenGate bidirectional replication ping-pong infinite loop

```sql
-- User updates row on Node A:
UPDATE users SET status = 'ACTIVE' WHERE user_id = 10;
-- GoldenGate captures mutation on A, replicates to B.
-- GoldenGate on B captures mutation on B, replicates back to A!
```

**Observed symptom:** A single UPDATE triggers millions of circular replication events, consuming 100% CPU and network bandwidth.

**(a)** What causes replication ping-pong loops in bidirectional active-active replication?

**(b)** How does GoldenGate's `SUPPRESSTRIGGERS` and `GETREPLICATES / IGNOREREPLICATES` parameter prevent loopback?

**(c)** What is Conflict Detection and Resolution (CDR) based on monotonic timestamps?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root cause:** The Extract process on Node B captures changes applied by the Replicat process on Node B and forwards them back to Node A, causing an infinite replication feedback loop.

**Fix:** Configure the Extract process to ignore transactions generated by the Replicat process using `TRANLOGOPTIONS EXCLUDEUSER ggs_admin` or `IGNOREREPLICATES`.

**Conflict Resolution:** Implement timestamp-based CDR: only apply updates if incoming timestamp is strictly greater than local row timestamp.

</details>

---

### Scoring

| Diagnosed correctly | Verdict |
| :--- | :--- |
| 5 of 5 | You can debug this module's material unaided. |
| 3–4 | Solid. Re-read the ones you missed and the file they cite. |
| 1–2 | Work the `debug_lab/` for this module before moving on. |
| 0 | Re-read the README and re-run the demos; the material has not landed yet. |

Every answer above cites real storage engine behaviors, configuration directives, and production failure modes.
Open your implementation files and verify the behavior — the fix is not hypothetical, it is in the code you have built.
