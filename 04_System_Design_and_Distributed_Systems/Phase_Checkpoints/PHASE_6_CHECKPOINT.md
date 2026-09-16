# Phase Checkpoint: Distributed Consensus, SRE Resilience & Master Capstone

> **Phase Scope:** Modules 23–26 (Sagas & Outbox, Raft & Vector Clocks, Telemetry & SRE, Enterprise Payment Gateway Capstone)  
> **Allocated Exam Duration:** 90 Minutes  
> **Evaluation Mode:** Closed-solution, timed architectural defense, capacity math drill, and code audit.

---

## 🎯 The Exam Mission: Defend the Master Capstone: Mission-Critical Enterprise Payment Platform with Distributed Consensus & AI Fraud Detection

### Executive Scenario
You are defending the complete Master Capstone before the Engineering Review Board (Staff/Principal Architects).
You have architected and deployed a multi-datacenter payment platform processing $10B annually across 12 countries.
The platform features an immutable Double-Entry Financial Ledger, distributed Saga orchestration for multi-service checkouts, Raft consensus for leader election and state machine replication, real-time AI fraud risk scoring, and W3C distributed telemetry with circuit breakers.

---

## 🏛️ Reference Architectural Blueprint (C4 Container View)

```

                    [ Merchant API Call: POST /v1/payments/authorize ]
                                            |
                         Idempotency Key Verification Layer
                                            v
               +---------------------------------------------------------+
               |                Payment Gateway Core                     |
               |                                                         |
               |   [ AI Fraud Scoring Engine (sub-25ms synchronous) ]    |
               |   (Velocity Rules, Heuristics, Embedding Scorer)        |
               |                            |                            |
               |                            v                            |
               |   [ Orchestrated Saga Controller ]                      |
               |   (Order -> Card Charge -> Inventory -> Compensate)     |
               |                            |                            |
               |                            v                            |
               |   [ Double-Entry Ledger (Immutable Zero-Sum Postings) ] |
               |   (Debit Customer Cash, Credit Merchant Settlement)     |
               |                            |                            |
               |                            v                            |
               |   [ Transactional Outbox Table (Local ACID DB) ]        |
               +---------------------------------------------------------+
                                            |
                             Raft Log Consensus Replicator
                                            v
               +---------------------------------------------------------+
               |              5-Node Distributed Raft Cluster            |
               |                                                         |
               |      [ Node 1: Leader (Term 4) ]                        |
               |        /                     \                          |
               |       v                       v                         |
               | [ Node 2: Follower ]    [ Node 3: Follower ]            |
               | (AppendEntries Quorum Committed to Disk via fsync)      |
               +---------------------------------------------------------+
                                            |
                              Outbox Dequeue Worker Relay
                                            v
               +---------------------------------------------------------+
               |           External Ecosystem & Observability            |
               |                                                         |
               |   [ Acquiring Bank API (Protected by Circuit Breaker) ] |
               |   [ W3C Distributed Tracer (traceparent Context) ]      |
               |   [ Prometheus / OpenTelemetry SRE Metrics Pipeline ]   |
               +---------------------------------------------------------+

```

---

## 📋 Hard Engineering & Scale Specifications

### 1. Functional Requirements
- **Zero-Discrepancy Double-Entry Ledger:** Guarantee strict balance conservation: for every transaction, $\sum \text{Debits} == \sum \text{Credits}$ down to the exact cent across multi-currency accounts.
- **Distributed Saga Compensation:** Orchestrate multi-step orders (`OrderPending` $	o$ `AuthorizeCard` $	o$ `DeductInventory` $	o$ `ConfirmOrder`). In case of card failure, backward compensations must reverse executed actions in reverse order.
- **Transactional Outbox Pattern:** Guarantee atomic persistence of domain state mutations and event broker payloads within the same local database transaction.
- **Raft Consensus Replication:** Maintain a 5-node distributed state machine cluster surviving the abrupt loss of 2 nodes without data corruption or split-brain.
- **Real-Time AI Fraud Scorer:** Evaluate transaction velocity, anomaly detection, and risk scores within a sub-25ms synchronous SLA.
- **W3C Distributed Tracing & Circuit Breaking:** Propagate `traceparent` headers across asynchronous boundaries and protect external acquiring bank APIs with 3-state Circuit Breakers (`CLOSED`, `OPEN`, `HALF_OPEN`).

### 2. Non-Functional & Regulatory Constraints
- **Financial Durability:** Zero data loss ($RPO = 0$); Raft synchronous quorum writes to disk before acknowledging transaction intent.
- **Idempotency Guarantee:** Duplicate HTTP requests with identical `Idempotency-Key` must return cached responses without re-executing ledger entries.
- **High Availability:** $RTO < 5\text{ seconds}$ during primary datacenter outage via automatic Raft leader election.
- **Regulatory Auditability:** Every ledger posting must be append-only and cryptographically immutable.

---

## 🧮 Quantitative Physics & Mathematical Formulations

### Financial Invariants & Consensus Quorum Math
1. **Double-Entry Balance Invariant:**
   $$\sum_{i=1}^k \text{DebitPosting}_i - \sum_{j=1}^m \text{CreditPosting}_j = 0.00 \quad (\text{down to exact integer cents})$$
   Any non-zero delta must immediately trigger an `AccountingDiscrepancyException` and abort the transaction.
2. **Raft Majority Quorum Requirement:**
   $$\text{Quorum Size} = \lfloor N / 2 \rfloor + 1$$
   For a cluster of $N = 5$ nodes, minimum quorum is $3$ nodes. The cluster tolerates $F = \lfloor (N-1)/2 \rfloor = 2$ simultaneous node crashes.
3. **Availability vs. Downtime Budget (Four Nines vs. Five Nines):**
   - $99.99\%$ Availability allows $4.38 \text{ minutes}$ of unplanned downtime per month.
   - $99.999\%$ Availability allows $25.9 \text{ seconds}$ of unplanned downtime per month.
4. **Circuit Breaker Failure Rate Threshold:**
   $$\text{Error Rate} = \frac{\text{Failed Requests in Rolling Window}}{\text{Total Requests in Rolling Window}} \ge 0.50 \implies \text{Trip to OPEN}.$$

---

### 💥 Production Chaos & Disaster Recovery Scenarios
1. **Primary Datacenter Sudden Severing (Split-Brain Test):** A network partition isolates the Raft Leader and Node 2 from Nodes 3, 4, and 5. The isolated Leader must be rejected when attempting to commit writes because it cannot achieve a 3-node majority quorum. Nodes 3, 4, and 5 must elect a new Leader and continue processing transactions without data loss.
2. **Double-Spend Idempotency Replay Attack:** An attacker fires 50 concurrent payment authorization requests with the exact same `Idempotency-Key`. The idempotency lock must ensure that only the first request reaches the payment gateway and ledger; the remaining 49 requests must block and return the exact authorized receipt.
3. **Dual-Write Failure Recovery:** The relational database commits the payment ledger row, but the server container loses power before publishing the event to Kafka. On reboot, the Transactional Outbox processor must read uncommitted rows and publish the event, achieving guaranteed at-least-once downstream notification.

---

## 📊 100-Point Comprehensive Grading Rubric

| Dimension | Evaluation Criteria | Maximum Points |
| :--- | :--- | :---: |
| **Financial Ledger Integrity** | Double-entry accounting, exact cent conservation, and immutable audit trails | 20 pts |
| **Sagas & Transactional Outbox** | Backward compensation orchestration, idempotency keys, and dual-write elimination | 20 pts |
| **Raft Consensus Protocol** | Leader election, randomized timeouts, log replication, and split-brain defenses | 20 pts |
| **Telemetry & Observability** | W3C context propagation, span hierarchy, and 3-state circuit breaker mechanics | 20 pts |
| **Real-Time Fraud & Capstone Defense**| Sub-25ms AI risk scoring, velocity checks, and comprehensive architectural defense | 20 pts |

**Passing Gate Threshold:** **85 / 100 Points** is required to officially certify and unlock the next phase.

---

## 🎙️ Diagnostic Oral Defense Questions (Staff-Level Panel)

Prepare to answer and defend these exact questions on a whiteboard during the review panel:

1. **Why does the Double-Entry bookkeeping system forbid updating or deleting an existing transaction row, requiring compensating reversal entries instead?**
2. **Explain how the Transactional Outbox pattern mathematically eliminates the Dual-Write distributed inconsistency problem without requiring Two-Phase Commit (2PC).**
3. **What is the Raft Election Safety property, and how does checking that candidate log is at least as up-to-date as the voter's log prevent data loss?**
4. **How does a 3-State Circuit Breaker prevent a struggling downstream acquiring bank from suffering a thundering herd when transitioning from OPEN to HALF-OPEN?**
5. **Why is Vector Clock causality tracking necessary in Dynamo-style peer-to-peer storage systems when wall-clock NTP timestamps cannot guarantee ordering?**

---

## 🚦 Pre-Flight Submission & Quality Checklist

Before submitting your phase architecture for certification, verify:
- [ ] All quantitative capacity math equations use explicit powers of 10 and real-world hardware latencies.
- [ ] API endpoints specify HTTP verbs, status codes, request bodies, and idempotency headers.
- [ ] Data models define primary keys, partition keys, sharding strategies, and secondary indexes.
- [ ] No single point of failure (SPOF) exists in either the control plane or the data path.
- [ ] Failure modes (split-brain, clock skew, thundering herds, cascading timeouts) have explicit mitigations.
- [ ] All starter exercises and unit tests in this phase pass with a 100% success rate (`pytest`).


---

## 🚦 Pre-Flight Gate: Verify Before You Start

**Do not start until all of this is green.** Sitting a timed exam on a broken
checkout means spending the clock on setup instead of on architecture.

```bash
# From the course root.
pytest Module_23_Distributed_Transactions_Sagas_Outbox \n      Module_24_Distributed_Consensus_Raft_Vector_Clocks \n      Module_25_Observability_Distributed_Tracing_SRE \n      Module_26_Capstone_Payment_Gateway_AI_Fraud       -q

python tools/check_links.py --quiet
ruff check .
```

---

## 📏 Exam Rules

| Rule | Detail |
| :--- | :--- |
| **Time box** | Set a timer for the duration above. When it ends, stop and score what exists. |
| **No solution exists** | There is deliberately no reference answer for this exam. The rubric *is* the specification. |
| **Modules are open-book** | Re-read any README, notebook or troubleshooting guide. That is what the job looks like. |
| **`project_solution/` is closed-book** | Do not open the module solutions during the exam. Copying them measures nothing. |
| **Numbers or it did not happen** | Every capacity claim needs arithmetic you can show. "It scales" scores zero. |
| **Name your tradeoffs** | A design with no stated downside is an unexamined design, and the rubric penalises it. |

---

## 🔬 Self-Verification Harness

Produce this evidence before scoring yourself. The rubric grades **evidence**,
not intent.

```bash
# 1. Your design's code runs at all
python -m your_design               # must not traceback

# 2. Your own tests pass
pytest your_tests.py -v             # paste the summary line

# 3. It is clean
ruff check .

# 4. Your capacity numbers are reproducible
python your_capacity_math.py        # prints QPS, bandwidth, storage, cache size
```

A design document with no runnable artefact caps at the analysis criteria only.

---

## ⏱️ If You Run Out of Time

1. **Submit the working subset.** Comment out anything that does not run - a
   broken import forfeits every point in the file.
2. **Write down what is missing**, one line per requirement. Naming your own gap
   accurately is a senior skill and earns analysis credit.
3. **Keep your numbers.** Capacity math for the parts you finished outscores
   hand-waving about the parts you did not.

---

## 🔁 If You Score Below the Threshold

1. Identify the **rubric row** you lost the most points on.
2. Re-read: **Module 23's compensation model and Module 24's majority requirement**.
3. Work that module's `debug_lab/` - it drills the exact failure modes this
   exam punishes.
4. Re-take with the numbers changed (different DAU, different payload size) so
   you are re-deriving rather than recalling.

Re-taking a checkpoint is normal. Advancing past one you failed is not, because
every later phase assumes this one.

---

## 🎓 What This Checkpoint Measures

The modules in scope taught you a set of techniques. This exam tests
**whether you can keep a multi-service system correct when parts of it fail**.

That is deliberately different from the module quizzes, which check whether each
piece landed. Here nobody tells you which technique to reach for. Choosing well,
under a clock, with no answer key, is the closest this course gets to the real
thing.
