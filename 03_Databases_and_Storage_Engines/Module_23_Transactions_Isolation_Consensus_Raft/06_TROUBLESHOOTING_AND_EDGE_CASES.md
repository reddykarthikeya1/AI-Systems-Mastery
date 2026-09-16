# Module 23 Transactions Isolation Consensus Raft: Troubleshooting & Production Edge Cases

This guide documents the most common production traps, failure modes, error codes, and operational edge cases in **Transactions, Isolation Levels & Distributed Consensus (Raft)**, complete with root cause analysis and step-by-step resolution runbooks.

---

## 1. Phantom Reads Under Repeatable Read in Standard SQL

### 🚨 Symptom
> Transaction re-executes a range query and discovers new rows inserted by another committed transaction.

### 🔍 Root Cause Analysis
Repeatable Read prevents non-repeatable reads on existing rows, but in standard locking engines (like MySQL without next-key locks), range locks are not held on phantom gaps.

### 🛠️ Production Fix & Mitigation Runbook
Elevate transaction isolation to `SERIALIZABLE` or verify your database engine uses Next-Key Locking (InnoDB) or Serializable Snapshot Isolation (PostgreSQL SSI).

---

## 2. Split-Brain Leader Election in Raft

### 🚨 Symptom
> Two nodes simultaneously believe they are the legitimate leader, accepting conflicting writes.

### 🔍 Root Cause Analysis
A partitioned cluster elected a leader without achieving strict majority quorum ($N/2 + 1$).

### 🛠️ Production Fix & Mitigation Runbook
Enforce strict quorum vote tallying: a candidate can only step up if it receives affirmative votes from at least $(N/2) + 1$ distinct nodes in the cluster.

---

## 3. Two-Phase Commit (2PC) Indefinite Blocking on Coordinator Crash

### 🚨 Symptom
> All participant databases in a distributed transaction hang with locked rows indefinitely.

### 🔍 Root Cause Analysis
The 2PC coordinator crashed after participants entered the `PREPARED` state, leaving participants unable to decide whether to commit or abort.

### 🛠️ Production Fix & Mitigation Runbook
Implement automated coordinator recovery using persistent Write-Ahead Logs, or transition distributed transaction protocols to three-phase commit (3PC) or Paxos/Raft-backed transaction engines.

---

## 5-Minute Production Triage Checklist

When encountering latency spikes, transaction rollbacks, or service degradation in this domain:
1. **Check Connection Pools:** Verify active vs idle connection ratios and eliminate thread starvation.
2. **Examine Wait Events:** Inspect query wait states (`pg_stat_activity`, `SHOW PROCESSLIST`, `v$session_wait`) to identify lock contention.
3. **Validate Memory & Disk:** Monitor swap usage, buffer cache hit ratios, and disk I/O queue depths.
4. **Audit Stale Snapshots:** Terminate lingering idle-in-transaction connections holding back cleanup or replication.
