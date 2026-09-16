# Module 23: Transactions, Isolation Anomalies & Distributed Consensus (Raft/2PC)

> **Brand new to this topic?** Start with [`00_W3_BEGINNER_PLAYGROUND.md`](00_W3_BEGINNER_PLAYGROUND.md) - the same ideas in
> plain language, with runnable standard-library code you can execute right now.
> No Docker, no server, no `pip install`.

Welcome to **Module 23**. In this module, you will master the most intellectually challenging frontier of database engineering: **Transaction Isolation Anomalies (Write Skew under Snapshot Isolation), Two-Phase Commit (2PC) across distributed partitions, and the Raft Distributed Consensus Protocol**.

---

## ⚡ 1. The ANSI SQL Lie vs. Snapshot Isolation

In 1992, the ANSI SQL standard defined four isolation levels based on three read phenomena:
1. **Dirty Read ($P1$)**: Reading uncommitted mutations from another transaction.
2. **Non-Repeatable Read ($P2$)**: Re-reading the same row and observing modified values.
3. **Phantom Read ($P3$)**: Re-running a range query and observing newly inserted rows.

| Isolation Level | Dirty Read | Non-Repeatable Read | Phantom Read |
| :--- | :--- | :--- | :--- |
| **Read Uncommitted** | Possible | Possible | Possible |
| **Read Committed** | Prevented | Possible | Possible |
| **Repeatable Read** | Prevented | Prevented | Possible |
| **Serializable** | Prevented | Prevented | Prevented |

### The 1995 Berenson Critique ("A Critique of ANSI SQL Isolation Levels")
In modern MVCC databases (PostgreSQL, Oracle, MySQL InnoDB), "Repeatable Read" does not use shared read locks; it uses **Snapshot Isolation (SI)**:
- Every transaction reads from an immutable point-in-time snapshot.
- Snapshot Isolation **prevents Dirty Reads, Non-Repeatable Reads, AND Phantom Reads**!
- Yet, Snapshot Isolation is **NOT Serializable** because it is vulnerable to a subtle anomaly called **Write Skew**.

---

## 🩺 2. The Write Skew Anomaly

Write Skew occurs when two concurrent transactions read overlapping datasets, evaluate a shared business invariant, and execute disjoint mutations that violate the invariant:

### The Classic "Doctors On-Call" Dilemma
- **Business Invariant**: At least one doctor must be on-call at all times ($Count(\text{on\_call}) \ge 1$).
- **Initial State**: Both Alice and Bob are on-call ($Count = 2$).

```
Timeline:
Tx 1 (Dr. Alice):                           Tx 2 (Dr. Bob):
-----------------                           ---------------
1. BEGIN (Snapshot Isolation)               1. BEGIN (Snapshot Isolation)
2. SELECT COUNT(*) WHERE on_call = True     2. SELECT COUNT(*) WHERE on_call = True
   (Returns 2 -> Invariant holds!)             (Returns 2 -> Invariant holds!)
3. UPDATE doctors SET on_call = False       3. UPDATE doctors SET on_call = False
   WHERE name = 'Alice';                       WHERE name = 'Bob';
4. COMMIT (Success!)                        4. COMMIT (Success!)
```

### Why MVCC Fails to Prevent Write Skew
- Alice modified row `Alice`. Bob modified row `Bob`.
- Because their **write-sets were completely disjoint**, MVCC write-write conflict detection (first-committer-wins) never fired!
- **Resulting State**: $Count(\text{on\_call}) = 0$. The invariant is shattered!

### Solving Write Skew: SSI vs. Explicit Locking
1. **Explicit Row Locks (`SELECT ... FOR UPDATE`)**: Forces both transactions to serialize on the evaluated rows.
2. **Serializable Snapshot Isolation (SSI)**:
   - Implemented in PostgreSQL since v9.1.
   - Maintains **SIREAD locks** (in-memory tracking flags, not blocking mutexes).
   - Detects rw-antidependencies ($T_1$ writes something $T_2$ read, and $T_2$ writes something $T_1$ read).
   - If a cycle forms in the serialization dependency graph ($T_1 \to T_2 \to T_1$), PostgreSQL aborts the younger transaction with `40001: could not serialize access due to read/write dependencies`.

---

## 🤝 3. Distributed Transactions: Two-Phase Commit (2PC)

When data is partitioned across multiple physical database nodes (e.g. CockroachDB, Spanner, Citus), committing a cross-shard transaction requires **atomic commitment across the network**:

```
           Coordinator                                Participants (Shard 1 & Shard 2)
                │                                                    │
                │ 1. Phase 1: PREPARE ("Can you commit?")            │
                ├───────────────────────────────────────────────────►│
                │                                                    │ Writes Prepare to WAL
                │                                                    │ Acquires Row Locks
                │ 2. VOTE ("YES" or "NO")                            │
                │◄───────────────────────────────────────────────────┤
                │                                                    │
   All voted YES?│                                                   │
   Write COMMIT │                                                    │
   to Local WAL │                                                    │
                │ 3. Phase 2: COMMIT ("Execute commit!")             │
                ├───────────────────────────────────────────────────►│
                │                                                    │ Writes Commit to WAL
                │                                                    │ Releases Locks
                │ 4. ACK ("Done")                                    │
                │◄───────────────────────────────────────────────────┤
```

### The Fatal Flaw of 2PC: The Coordinator Crash & Blocking
If a participant votes `YES` in Phase 1, it enters the **Prepared State**. It has promised to commit, but cannot execute until it hears from the Coordinator.
- **The Failure Mode**: If the Coordinator crashes after participants vote `YES` but before sending `COMMIT`, the participants are **indefinitely blocked**.
- They cannot abort (the coordinator might have committed). They cannot commit (another participant might have voted NO).
- Their table and row locks remain held indefinitely, causing cascading timeouts throughout the application until the coordinator is revived!

---

## 🎖️ 4. Distributed Consensus: The Raft Protocol

Modern cloud-native databases (CockroachDB, TiDB, etcd, Kafka KRaft) replace fragile 2PC with non-blocking **Distributed Consensus**:

### Core Raft Principles (Ongaro & Ousterhout 2014)
1. **Node States**:
   - `Follower`: Passive, responds to incoming RPCs from leaders and candidates.
   - `Candidate`: Initiates election if heartbeat timer expires.
   - `Leader`: Handles all client writes, sequences log entries, and heartbeats followers.
2. **Quorum Consensus**:
   - Any cluster of $N$ nodes can tolerate $F = \lfloor (N - 1) / 2 \rfloor$ failures.
   - A 3-node cluster tolerates 1 dead node; a 5-node cluster tolerates 2 dead nodes.
3. **Randomized Election Timeouts (150ms – 300ms)**:
   - Prevents split-vote ties when multiple nodes time out simultaneously.
4. **Log Replication & Commit Rule**:
   - A leader appends client mutations to its local log.
   - Broadcasts `AppendEntries` RPC to all followers.
   - Once an entry is written to disk on a **majority of nodes** ($\lfloor N/2 \rfloor + 1$), the leader marks it **Committed** and applies it to its state machine.
   - Even if the leader crashes immediately afterward, the election safety invariant guarantees the newly elected leader will contain that committed entry!

---

## 🛠️ 5. Hands-On Lab: Building a Consensus & Transaction Engine

In this lab, you will implement:
1. **Write Skew Simulator**: Demonstrate the classic Doctor On-Call anomaly under Snapshot Isolation and prove how SSI detection aborts the second transaction.
2. **Two-Phase Commit (2PC) Coordinator**: Coordinate distributed multi-node transactions, handle participant abort votes, and manage recovery logs.
3. **Raft State Machine & Leader Election**: Implement randomized election timeouts, vote solicitation, quorum tallying, and term incrementing.
4. **Raft Replicated Log**: Broadcast `AppendEntries`, manage `commitIndex`, and enforce majority replication consensus.

---

## 📂 Project Structure
```
Module_23_Transactions_Isolation_Consensus_Raft/
├── README.md
├── 01_write_skew_and_raft_consensus_demo.py
├── starter/
│   └── consensus_engine.py
└── project_solution/
    ├── consensus_engine.py
    └── test_consensus_engine.py
```

---

## 5. Dual-Track Curriculum: Track A (Simulation) vs Track B (Real Operations)

This module implements a rigorous **dual-track architecture** guaranteeing both first-principles mechanistic understanding and battle-tested production operational skills:

| Dimension | Track A: Mechanistic Model | Track B: Live Engine Operations |
| :--- | :--- | :--- |
| **Location** | `project_solution/transaction_raft_engine.py` | `project_solution/*_live.py` |
| **Focus** | Internal algorithms & data structures | Real drivers, pooling, and production operations |
| **Technology** | transaction_raft_engine.py (Raft consensus, 2PC, isolation levels) | isolation_live.py (psycopg2 isolation levels, dirty/phantom reads) |
| **Verification** | `project_solution/test_transaction_raft_engine.py` | `project_solution/test_*_live.py` |
| **Offline Support** | 100% in-process with 0 external dependencies | Safe skips via `@pytest.mark.skipif` when offline |

### Reconciliation Contract
A dedicated reconciliation suite guarantees that the internal algorithmic model and the real live production driver strictly agree on core operational semantics, invariants, and expected outcomes.

---

## 6. Production Failure Modes & Operational Pitfalls

Every production engineer must understand how this database layer fails under extreme stress:

1. Write Skew under Snapshot Isolation: Concurrent transactions modifying disjoint rows based on shared premise.
2. Split-Brain Dual Leader: Candidate becoming leader without strict majority quorum ($N/2 + 1$), accepting divergent writes.
3. 2PC Indefinite Lock Blocking: Coordinator crashing after participants enter PREPARED state, freezing resources.

For complete diagnosis runbooks, error codes, and step-by-step resolution strategies, consult:
👉 **[TROUBLESHOOTING_AND_EDGE_CASES.md](06_TROUBLESHOOTING_AND_EDGE_CASES.md)**

---

## 7. When NOT to Use (Trade-offs & Anti-Patterns)

> [!WARNING]
> Architecture is the art of trade-offs. No database technology is universally optimal.

Do NOT implement custom distributed consensus protocols in application code; utilize established distributed consensus backbones (etcd, Raft, Paxos).

---

## 8. Essential Production CLI & Query Playbook

Key operational diagnostic commands to verify health and diagnose performance:

```bash
# Verify environment and execute automated test suite
pytest Module_23_Transactions_Isolation_Consensus_Raft -v

# Operational Diagnostics & Health Verification
pytest Module_23_Transactions_Isolation_Consensus_Raft -v
```

---

## 9. Next Steps & Pedagogical Resources

Accelerate your mastery using the structured pedagogical artifacts in this module:
1. 📓 **[Interactive Jupyter Lab](02_interactive_transactions_consensus.ipynb)**: Hands-on sandbox for interactive exploration.
2. 🎯 **[3-Tier Guided Project](04_PROJECT_GUIDE.md)**: Novice, Core, and Architect implementation tracks.
3. 🛠️ **[Troubleshooting Guide](06_TROUBLESHOOTING_AND_EDGE_CASES.md)**: Real production error signatures & fixes.
4. 🧠 **[Self-Assessment Quiz](05_SELF_ASSESSMENT_AND_CHALLENGES.md)**: 10 diagnostic questions + coding challenges.
5. 🔬 **[Debug Lab](debug_lab/)**: Forensic debugging exercise diagnosing real production bugs.

