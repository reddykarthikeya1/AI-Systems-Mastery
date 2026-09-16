# Phase Checkpoint: Low-Level Design (LLD), Clean Architecture & Machine Coding

> **Phase Scope:** Modules 05–08 (SOLID & DDD, GoF Patterns, State Machines & LOOK, Financial Settlement & Rate Limiting)  
> **Allocated Exam Duration:** 90 Minutes  
> **Evaluation Mode:** Closed-solution, timed architectural defense, capacity math drill, and code audit.

---

## 🎯 The Exam Mission: Machine Coding: Design a Concurrency-Safe Peer-to-Peer Expense Settlement & Group Ledger Engine

### Executive Scenario
You are participating in a 90-minute Staff-level Machine Coding and Low-Level Design interview.
You must construct a production-grade, object-oriented financial engine that handles split bills, user balances, debt graph minimization, and rate-limited payment intent dispatching.
Your code must strictly conform to Domain-Driven Design (DDD) principles, Clean Architecture / Hexagonal boundaries, and GoF patterns, while guaranteeing zero penny rounding drift under high concurrency.

---

## 🏛️ Reference Architectural Blueprint (C4 Container View)

```

               [ Client HTTP / CLI Interface Adapters ]
                                  |
                                  v
             +-----------------------------------------+
             |         Application Use Cases           |
             |                                         |
             |   [ RecordExpenseUseCase ]              |
             |   [ SettleGroupDebtsUseCase ]           |
             |   [ ProcessPaymentIntentUseCase ]       |
             +-----------------------------------------+
                                  |
                                  v
             +-----------------------------------------+
             |             Domain Core                 |
             |                                         |
             |   [ GroupAggregate (Aggregate Root) ]   |
             |   [ Money (Immutable Value Object) ]    |
             |   [ SplitStrategy (GoF Strategy) ]      |
             |   [ DebtSimplifier (Greedy Graph Min) ] |
             +-----------------------------------------+
                                  |
               (Dependency Inversion Ports / Interfaces)
                                  v
             +-----------------------------------------+
             |         Infrastructure Adapters         |
             |                                         |
             |   [ InMemoryGroupRepository ]           |
             |   [ ThreadSafeTokenBucketLimiter ]      |
             |   [ DecoratorChainedNotificationGateway]|
             +-----------------------------------------+

```

---

## 📋 Hard Engineering & Scale Specifications

### 1. Functional Requirements
- **Split Bill Types:** Support `EQUAL`, `EXACT_AMOUNTS`, and `PERCENTAGE` splits across arbitrary participant lists.
- **Penny Rounding Conservation:** Preserve the fundamental financial invariant: $\sum \text{splits} == \text{total\_cents}$ down to the exact cent without IEEE-754 floating point distortion.
- **Debt Graph Simplification:** Implement greedy balance settlement reducing $N$ pairwise debts to $\le N-1$ minimal direct transactions.
- **Extensible Notification Channel:** Dispatch settlement notifications via Email, SMS, and Push using Strategy and Decorator patterns (logging, retry, circuit breaker).

### 2. Non-Functional & Structural Invariants
- **Domain Purity:** Domain entities (`User`, `Transaction`, `BalanceSheet`) must have zero dependencies on frameworks, databases, or HTTP libraries.
- **Thread Safety:** All balance mutations and rate limiter checks must be thread-safe under concurrent multi-threaded invocation.
- **Idempotency:** Re-executing the same payment intent token must return the previous result without applying duplicate balance modifications.
- **Zero Memory Leaks:** State machines and observer lists must be weakly referenced or explicitly lifecycle-managed.

---

## 🧮 Quantitative Physics & Mathematical Formulations

### Financial Invariant & Graph Complexity Math
1. **Zero-Sum Ledger Conservation:** For any group of $M$ users, the sum of all net balances must equal zero:
   $$\sum_{i=1}^M \text{NetBalance}(u_i) = 0.00$$
2. **Penny Remainder Distribution:** When splitting $C$ cents among $K$ users:
   $$\text{Base} = \lfloor C / K \rfloor, \quad R = C \pmod K$$
   The first $R$ users pay $\text{Base} + 1$ cents; the remaining $K - R$ pay $\text{Base}$ cents.
3. **Debt Minimization Bounds:** An un-simplified pairwise debt graph with $N$ users can have up to $N(N-1)/2$ edges ($O(N^2)$). The greedy settlement algorithm collapses this to at most $N-1$ directed transaction edges ($O(N)$).

---

### 💥 Machine Coding Edge-Case Scenarios
1. **The Three-Way $100 Bill Split:** Splitting $100.00 among 3 participants yields $33.33 each, leaving $0.01 unassigned. Your algorithm must deterministically attribute the remainder to the payer or first participant without violating the zero-sum ledger invariant.
2. **Cyclic Debt Deadlock:** User A owes B $50, B owes C $50, and C owes A $50. Naive pairwise iteration enters infinite loops. Your engine must reduce net balances to 0 for all three users, outputting 0 required transactions.
3. **Concurrent Intent Race:** 20 concurrent threads submit the exact same `$50 settlement token` simultaneously. Your rate limiter and idempotency lock must ensure exactly 1 execution succeeds and 19 receive cached idempotency responses.

---

## 📊 100-Point Comprehensive Grading Rubric

| Dimension | Evaluation Criteria | Maximum Points |
| :--- | :--- | :---: |
| **Domain Modeling & Invariants** | Value objects (`Money`), immutable entities, and exact penny conservation math | 20 pts |
| **Clean Architecture Separation** | Hexagonal ports and adapters; zero database or framework leakage into domain core | 20 pts |
| **Algorithmic Correctness** | Debt graph simplification (greedy net balance matching) producing minimal transactions | 20 pts |
| **Pattern Composition** | Strategy, Factory, Decorator, and Chain of Responsibility implemented cleanly | 20 pts |
| **Concurrency & Defensive Guards** | Thread-safe locks, atomic rate limiting, boundary validation, and 100% pytest pass | 20 pts |

**Passing Gate Threshold:** **85 / 100 Points** is required to officially certify and unlock the next phase.

---

## 🎙️ Diagnostic Oral Defense Questions (Staff-Level Panel)

Prepare to answer and defend these exact questions on a whiteboard during the review panel:

1. **Why is the greedy debt simplification algorithm an approximation of the NP-hard minimum cash flow problem, and in what graph topologies does it fail to find the global minimum?**
2. **How do you enforce that a `Money` Value Object cannot add USD to EUR without an explicit CurrencyExchange domain service?**
3. **Explain how the Decorator pattern allows you to add exponential backoff retry and distributed tracing to notification strategies without modifying their source code.**
4. **What is the difference between an Entity, a Value Object, and an Aggregate Root in Domain-Driven Design?**
5. **How would you prevent deadlocks when two users concurrently attempt to settle debts with each other in opposite directions?**

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
pytest Module_05_SOLID_Principles_Clean_Architecture \n      Module_06_GoF_Design_Patterns_Scalable_Systems \n      Module_07_LLD_State_Machines_Scheduling_Elevator_Parking \n      Module_08_LLD_Financial_Engines_Splitwise_Rate_Limiting       -q

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
2. Re-read: **Module 05's dependency direction and Module 07's state modelling**.
3. Work that module's `debug_lab/` - it drills the exact failure modes this
   exam punishes.
4. Re-take with the numbers changed (different DAU, different payload size) so
   you are re-deriving rather than recalling.

Re-taking a checkpoint is normal. Advancing past one you failed is not, because
every later phase assumes this one.

---

## 🎓 What This Checkpoint Measures

The modules in scope taught you a set of techniques. This exam tests
**whether you can turn a vague requirement into classes whose invariants hold**.

That is deliberately different from the module quizzes, which check whether each
piece landed. Here nobody tells you which technique to reach for. Choosing well,
under a clock, with no answer key, is the closest this course gets to the real
thing.
