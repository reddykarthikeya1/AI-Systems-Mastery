# Module 23 Transactions Isolation Consensus Raft: Self-Assessment & Mastery Challenges

Evaluate your practical and conceptual mastery of **Transactions, Isolation Levels & Distributed Consensus (Raft)** before proceeding.

---

## Part 1: Conceptual Mastery Quiz (10 Questions)

### Questions

1. **Define the three ANSI SQL read phenomena: Dirty Read, Non-Repeatable Read, and Phantom Read.?** Define the three ANSI SQL read phenomena: Dirty Read, Non-Repeatable Read, and Phantom Read.
2. **What is the difference between Two-Phase Locking (2PL) and Strict 2PL (S2PL)?** What is the difference between Two-Phase Locking (2PL) and Strict 2PL (S2PL)?
3. **Explain the two phases of the Two-Phase Commit (2PC) protocol.?** Explain the two phases of the Two-Phase Commit (2PC) protocol.
4. **Why is 2PC considered a blocking protocol?** Why is 2PC considered a blocking protocol?
5. **How does the Raft consensus algorithm handle Leader Election?** How does the Raft consensus algorithm handle Leader Election?
6. **What is a Split-Brain in distributed systems, and how does quorum prevent it?** What is a Split-Brain in distributed systems, and how does quorum prevent it?
7. **What is Snapshot Isolation (SI), and what anomaly can occur under it that is prevented by Serializable?** What is Snapshot Isolation (SI), and what anomaly can occur under it that is prevented by Serializable?
8. **What is Serializable Snapshot Isolation (SSI) in PostgreSQL?** What is Serializable Snapshot Isolation (SSI) in PostgreSQL?
9. **What does the Raft Log Matching Property guarantee?** What does the Raft Log Matching Property guarantee?
10. **What is the difference between safety and liveness in distributed consensus?** What is the difference between safety and liveness in distributed consensus?

---

## Part 2: Answer Key & Detailed Explanations

<details>
<summary><b>Click to expand the Answer Key & Explanations</b></summary>

#### Answer 1:
Dirty Read: reading uncommitted changes; Non-Repeatable Read: re-reading a row returns modified values; Phantom Read: re-executing range query returns newly inserted rows.

#### Answer 2:
2PL releases locks during shrinking phase before commit; Strict 2PL holds all exclusive locks until transaction COMMIT or ABORT, preventing cascading rollbacks.

#### Answer 3:
Phase 1 (Prepare): Coordinator asks participants if they can commit; participants vote YES and write to WAL. Phase 2 (Commit): If all voted YES, coordinator issues COMMIT; otherwise ABORT.

#### Answer 4:
If the coordinator crashes after participants enter the PREPARED state, participants must hold locks indefinitely until coordinator recovers.

#### Answer 5:
Followers transition to Candidate upon election timer timeout, increment term, vote for self, and request votes; majority votes ($N/2 + 1$) wins election.

#### Answer 6:
Two nodes simultaneously believing they are leader; quorum ($N/2 + 1$) guarantees no two disjoint subsets can both achieve majority.

#### Answer 7:
Transactions read from a consistent snapshot taken at start; Write Skew anomaly can occur (prevented only by Serializable).

#### Answer 8:
An optimistic implementation of serializable isolation that tracks read-write conflicts (SIREAD locks) and aborts transactions exhibiting dangerous dependency cycles.

#### Answer 9:
If two logs contain an entry with the same index and term, they are identical up to that index.

#### Answer 10:
Safety: nothing bad happens (never two leaders, no split-brain); Liveness: something good eventually happens (cluster makes progress).

</details>

---

## Part 3: Architecture & Coding Mastery Challenges

### 🏋️ Challenge 1: Core System Implementation
Build a 3-node Raft consensus cluster in Python implementing leader election and heartbeat replication.

### 🚀 Challenge 2: Architect Stretch Problem
Demonstrate Write Skew under Snapshot Isolation and resolve it using SELECT FOR UPDATE.

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

### D1. Write Skew Anomaly Under REPEATABLE READ Isolation

```sql
-- Hospital Doctor On-Call Schedule Table
CREATE TABLE on_call_schedule (
    doctor_id int PRIMARY KEY,
    doctor_name text,
    is_on_call boolean
);
-- Constraint: At least ONE doctor must remain on call at all times!
-- Current state: Alice and Bob are BOTH on call (is_on_call = true).

-- Transaction 1 (Doctor Alice takes leave):
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SELECT count(*) FROM on_call_schedule WHERE is_on_call = true; -- Returns 2
UPDATE on_call_schedule SET is_on_call = false WHERE doctor_id = 1; -- Alice
COMMIT;

-- Concurrent Transaction 2 (Doctor Bob takes leave):
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SELECT count(*) FROM on_call_schedule WHERE is_on_call = true; -- Returns 2
UPDATE on_call_schedule SET is_on_call = false WHERE doctor_id = 2; -- Bob
COMMIT;
```

**Observed symptom:** Both transactions commit successfully with 0 errors. Querying the table reveals ZERO doctors on call (both Alice and Bob set to false), violating the hospital invariant.

**(a)** What is Write Skew, and why does REPEATABLE READ (Snapshot Isolation) fail to prevent it?

**(b)** Why was no row-level write-write lock conflict detected between Transaction 1 and Transaction 2?

**(c)** What are the two valid solutions: `SERIALIZABLE` isolation level vs explicit pessimistic locking (`SELECT ... FOR UPDATE`)?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
**Write Skew** occurs under Snapshot Isolation / REPEATABLE READ when two concurrent transactions read overlapping datasets (both see 2 doctors on call) but make disjoint mutations (Tx 1 updates Alice's row; Tx 2 updates Bob's row). Because the two transactions modified different physical rows, there was no write-write conflict to trigger a rollback. Each transaction made an assumption based on a premise that the other transaction simultaneously invalidated, breaking the global invariant.

**Diagnostic Commands:**
1. Reproduce under `REPEATABLE READ`: Both commit without errors.
2. Check transaction isolation level:
   ```sql
   SHOW transaction_isolation;
   ```

**Production Fix:**
- **Approach 1 (SERIALIZABLE Isolation):** Use true `SERIALIZABLE` isolation (SSI / Serializable Snapshot Isolation in Postgres):
  ```sql
  BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;
  ```
  Postgres tracks read-write dependencies (SIREAD locks). Transaction 2 will fail with: `ERROR: could not serialize access due to read/write dependencies among transactions`.
- **Approach 2 (Pessimistic Locking / Materialized Conflict):**
  Lock the entire group or use `FOR UPDATE` on all on-call records:
  ```sql
  SELECT count(*) FROM on_call_schedule WHERE is_on_call = true FOR UPDATE;
  ```
  Tx 2 will block until Tx 1 commits, then re-read `count = 1` and abort.

</details>

---

### D2. Two-Phase Commit (2PC) Participant In-Doubt Blocking on Coordinator Crash

```python
# Two-Phase Commit Distributed Transaction
# Coordinator coordinates Bank DB 1 and Bank DB 2

# Phase 1 (Prepare):
coord.send_prepare(DB1, "tx_991") # DB1 replies: PREPARED
coord.send_prepare(DB2, "tx_991") # DB2 replies: PREPARED

# Coordinator writes "COMMIT" to local WAL... and immediately suffers POWER FAILURE!
# Coordinator remains offline for 6 hours.
```

**Observed symptom:** Bank DB 1 and DB 2 have dozens of customer account rows completely locked. All incoming user transactions attempting to read or update those accounts hang indefinitely and time out.

**(a)** What is the 'In-Doubt' state in Two-Phase Commit (2PC)?

**(b)** Why cannot a 2PC participant unilaterally decide to commit or abort while in the Prepared state?

**(c)** How does Three-Phase Commit (3PC) or Paxos/Raft-backed transaction coordinators eliminate coordinator single-point-of-failure blocking?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
Once a 2PC participant votes `PREPARED`, it enters the **In-Doubt** state. It has promised the coordinator that it can and will either commit or abort whenever instructed, and holds exclusive row locks on the modified data to uphold ACID guarantees. The participant **cannot unilaterally abort** (because the coordinator might have decided to commit and told other participants to commit), nor can it **unilaterally commit** (because another participant might have voted abort). It is completely blocked until the coordinator recovers and tells it the outcome.

**Diagnostic Commands:**
1. Check prepared transactions in PostgreSQL:
   ```sql
   SELECT gid, prepared, owner, database FROM pg_prepared_xacts;
   ```
2. Check locks held by prepared transactions:
   ```sql
   SELECT * FROM pg_locks WHERE transactionid IS NOT NULL;
   ```

**Production Fix:**
1. **Manual Administrator Recovery:** Inspect coordinator logs. If coordinator committed, manually commit the prepared transaction:
   ```sql
   COMMIT PREPARED 'tx_991';
   -- Or if coordinator aborted:
   ROLLBACK PREPARED 'tx_991';
   ```
2. **Modern Architecture Fix:** Replace traditional 2PC coordinators with a replicated state machine backed by **Raft or Paxos** (e.g. CockroachDB, Spanner, or Temporal). In these systems, coordinator state is replicated across a consensus group; if the active coordinator crashes, a new leader takes over immediately and finishes in-doubt transactions within milliseconds.

</details>

---

### D3. Raft Consensus Split-Vote Livelock from Homogeneous Election Timeouts

```python
# Raft Consensus Node Configuration (5-node cluster)
heartbeat_interval = 100ms
election_timeout_min = 200ms
election_timeout_max = 200ms  # Fixed, non-randomized timeout!
```

**Observed symptom:** When the active Raft leader is killed, the cluster fails to elect a new leader. Term numbers rapidly increment from Term 1 to Term 840 in 2 minutes. The cluster remains completely unavailable for client writes.

**(a)** Why does a fixed election timeout cause split votes in Raft?

**(b)** What is the quorum requirement for electing a leader in a 5-node cluster?

**(c)** How does randomized election timeout resolve split votes and guarantee quick leader convergence?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
In Raft, a leader candidate must receive votes from a majority of nodes ($\lfloor N/2 
floor + 1 = 3$ in a 5-node cluster). When the current leader fails, all 4 remaining followers wait for their election timeout before starting an election. Because their election timeouts are identical (200ms), all 4 nodes transition to Candidate state and broadcast `RequestVote` RPCs at the exact same millisecond. Each node votes for itself first, splitting the votes ($1 + 1 + 1 + 1$). None achieve a 3-node majority. The term expires, they all restart elections simultaneously, repeating the split-vote loop indefinitely (**election livelock**).

**Diagnostic Commands:**
1. Inspect Raft logs:
   ```text
   Node 2: Election timeout -> Starting election for Term 42
   Node 3: Election timeout -> Starting election for Term 42
   Node 2: Received 2 votes, required 3 -> Election failed
   Node 3: Received 2 votes, required 3 -> Election failed
   ```

**Production Fix:**
Implement **Randomized Election Timeouts** as mandated by the Raft specification:
```python
import random

heartbeat_interval = 100  # ms
# Randomize election timeout between 150ms and 300ms
election_timeout = random.uniform(150, 300)
```
With randomized timeouts, one node's timer will naturally expire before the others (e.g. at 162ms). It increments the term, votes for itself, and broadcasts `RequestVote` before other nodes timeout, securing votes from the other followers and establishing leadership in a single round.

</details>

---

### D4. Raft Stale Read Anomaly During Asymmetric Network Partition

```python
# 5-Node Raft Cluster: Node 1 (Leader), Nodes 2, 3, 4, 5 (Followers)
# Network partition occurs:
# Partition A: Node 1 (Old Leader) isolated with Node 2
# Partition B: Nodes 3, 4, 5 (Elected Node 3 as New Leader)

# Client reads user balance from Node 1:
balance = node1.read("account:user_42:balance")
```

**Observed symptom:** Client reads balance = $1,000 from Node 1, even though a write committing balance = $200 was successfully acknowledged by Node 3 (new leader) to another client 5 seconds ago.

**(a)** Why can an isolated old Raft leader serve stale reads if it simply reads its local state machine?

**(b)** What is ReadIndex and Lease Read in Raft linearizable read semantics?

**(c)** How do you guarantee linearizable reads without running full Raft log consensus for every read query?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
In Raft, writes require a majority quorum (3 out of 5 nodes), so Node 1 cannot commit new writes in Partition A. However, if read requests are served directly from the local state machine without checking current leadership status, an old leader that hasn't realized it has been deposed will continue serving stale data to clients until its election/heartbeat probe times out.

**Diagnostic Commands:**
1. Check current leader identity across nodes:
   ```bash
   curl http://node1:8001/raft/status  # Claims leader=Node 1, Term=5
   curl http://node3:8001/raft/status  # Claims leader=Node 3, Term=6
   ```

**Production Fix:**
1. **ReadIndex Algorithm:**
   When a read arrives at a leader:
   - Leader records its current `commitIndex` as `readIndex`.
   - Leader broadcasts a heartbeat round (`AppendEntries` with 0 logs) to followers and waits for a majority confirmation to verify it is still the legitimate leader.
   - Once confirmed, the leader waits until its state machine applies up to `readIndex`, and then returns the data.
2. **Leader Leases:** The leader maintains a bounded time lease renewed on successful heartbeats. Reads can be answered locally as long as the leader lease has not expired.

</details>

---

### D5. Deadlock Cycle from Inconsistent Multi-Table Locking Order

```sql
-- Transaction 1 (Payment Service):
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE account_id = 'acc_A';
-- Does other processing...
UPDATE accounts SET balance = balance + 100 WHERE account_id = 'acc_B';
COMMIT;

-- Concurrent Transaction 2 (Refund Service):
BEGIN;
UPDATE accounts SET balance = balance + 100 WHERE account_id = 'acc_B';
-- Does other processing...
UPDATE accounts SET balance = balance - 100 WHERE account_id = 'acc_A';
COMMIT;
```

**Observed symptom:** Both transactions freeze for 1,000ms until one terminates with: ERROR: deadlock detected. Detail: Process 2819 waits for ExclusiveLock on tuple (0, 12) of relation accounts; blocked by process 2820.

**(a)** What are the four necessary conditions for deadlock (Coffman conditions)?

**(b)** How does PostgreSQL's deadlock detector identify deadlock cycles?

**(c)** How does enforcing a deterministic global lock ordering eliminate deadlocks by design?

<details>
<summary><b>Show the diagnosis</b></summary>

**Root Cause:**
A deadlock occurs when two or more transactions hold locks that the other needs and neither can proceed.
- Tx 1 acquired an exclusive row lock on `acc_A` and requested a lock on `acc_B`.
- Tx 2 acquired an exclusive row lock on `acc_B` and requested a lock on `acc_A`.
Because the locks were acquired in reverse order (`A -> B` vs `B -> A`), a circular wait condition was created. After `deadlock_timeout` (default 1s), Postgres traces the dependency graph, detects the cycle, and aborts one transaction.

**Diagnostic Commands:**
1. Examine PostgreSQL log file for the full deadlock dump:
   ```text
   Process 2819: UPDATE accounts ... WHERE account_id = 'acc_B';
   Process 2820: UPDATE accounts ... WHERE account_id = 'acc_A';
   ```
2. Inspect `pg_stat_database` deadlock counter:
   ```sql
   SELECT datname, deadlocks FROM pg_stat_database;
   ```

**Production Fix:**
1. **Deterministic Lock Ordering:** Always acquire locks in a globally consistent, deterministic order (e.g. sorted by primary key):
   ```python
   def transfer(acc_from, acc_to, amount):
       # Sort account IDs lexicographically:
       first, second = sorted([acc_from, acc_to])
       with db.transaction():
           db.execute("SELECT * FROM accounts WHERE id = %s FOR UPDATE", (first,))
           db.execute("SELECT * FROM accounts WHERE id = %s FOR UPDATE", (second,))
           # Perform updates...
   ```
   Because all transactions lock `first` then `second`, circular waits are mathematically impossible.

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
