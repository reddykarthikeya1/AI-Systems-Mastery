# Module_23_Distributed_Transactions_Sagas_Outbox: Project Implementation Guide

**Deliverable:** a distributed transaction orchestrator implementing Orchestrated Sagas, backward compensating actions, and the Transactional Outbox pattern.

---

## 🎯 3-Tier Progressive Learning Path

| Tier | For you if… | You build | Estimated Time |
| :--- | :--- | :--- | :--- |
| **Tier 1 — Novice Walkthrough** | You are learning the core concepts and basic mechanics | Model multi-step Saga transactions with forward execution and backward compensation handlers. | ~2 hrs |
| **Tier 2 — Core Project** | Tier 1 passes completely and you want production quality | Build `SagaOrchestrator` handling partial execution failures with automated reverse rollback compensation. | ~3 hrs |
| **Tier 3 — Architect Stretch** | You want production-hardened, high-throughput systems | Implement the Transactional Outbox pattern with atomic local DB commits and idempotent message relay. | ~2.5 hrs |

### Setup for All Tiers

Verify your working directory and execute the test suite:
```bash
cd "System Design/Module_23_Distributed_Transactions_Sagas_Outbox"
pytest project_solution/test_saga_orchestrator.py -v
```

Before writing code, verify your test environment imports the starter directory:
```bash
cd starter
pytest ../project_solution/test_saga_orchestrator.py -v
```
All starter stubs initially raise `NotImplementedError`. Your goal is to replace each stub with a working, production-grade implementation.

---

## 1. Architectural Blueprint & Invariants

```

      [ Saga Orchestrator ]
               |
         +-----+---------------------------------------+
         | Step 1: Order Pending                       |
         v                                             v
     [Order Service]                            [Transaction Log]
         |                                             |
         | Step 2: Charge Payment (FAILS!)             |
         v                                             v
     [Payment Service] --------------------> Trigger Compensation:
                                             Step 1 Rollback -> Cancel Order!

```

### Core Invariants & Algorithmic Contracts
1. **Deterministic State Progression:** State mutations must be deterministic and fully traceable.
2. **Defensive Validation:** All inputs must be strictly validated before modifying internal state.
3. **No Hidden State Corruption:** If an operation fails midway, all state changes must be cleanly rolled back or isolated.
4. **Time & Space Bounds:** Lookups, iterations, and memory allocations must strictly adhere to the module's target Big-O complexity bounds.

---

## 2. Step-by-Step Implementation Sequence

### Phase A: Tier 1 — Novice Walkthrough

#### Step 1: Baseline Data Structures & Invariants
- Define `SagaStep` with `action` and `compensation` callable functions.
- Ensure initialization parameters are validated against boundary conditions.

#### Step 2: Core Algorithmic Mechanics
- Implement `SagaOrchestrator.execute()`: execute steps sequentially and log state.
- Implement pure deterministic helper functions first.

### 🛑 Stop Here Until This Works!
Run the test suite for Tier 1:
```bash
pytest project_solution/test_saga_orchestrator.py -k "basic or initial or create or test_1" -v
```
Do not proceed to Tier 2 until all baseline data structure and creation checks pass cleanly.

---

### Phase B: Tier 2 — Core Production Project

#### Step 3: Concurrency, Error Isolation & Edge Cases
- Simulate mid-workflow failure: catch exception, reverse executed steps in LIFO order, and run compensations.
- Guard against concurrent mutations and race conditions where applicable.

#### Step 4: End-to-End Orchestration
- Implement `TransactionalOutbox`: save domain entity and outbox message in the same atomic transaction.
- Connect the core engine to its secondary components and test full end-to-end operational flows.

### 🛑 Stop Here Until This Works!
Run the full automated test suite:
```bash
pytest project_solution/test_saga_orchestrator.py -v
```
Every single test in `project_solution/test_saga_orchestrator.py` must pass with zero failures and zero warnings.

---

### Phase C: Tier 3 — Architect Stretch Challenge

#### Step 5: High-Scale & Fault-Tolerant Extension
- Implement idempotent consumer processing outbox events using unique deduplication keys.
- Benchmark your implementation under synthetic stress or failure injections.
- Measure latency percentiles, memory footprints, and resource reclamation behavior.

---

## 3. Directory Layout

```
Module_23_Distributed_Transactions_Sagas_Outbox/
├── 00_interactive_*.ipynb            # Interactive architectural exploration notebook
├── README.md                          # Deep-dive theory, trade-off matrices, and blueprints
├── SELF_ASSESSMENT_AND_CHALLENGES.md  # 10 diagnostic questions + 3 design challenges
├── PROJECT_GUIDE.md                   # This step-by-step implementation guide
├── TROUBLESHOOTING_AND_EDGE_CASES.md  # Real-world production failure post-mortems
├── debug_lab/                         # Intentional production defect lab & answers
│   ├── SYMPTOMS.md                    # P1 incident report & reproduction steps
│   ├── broken_saga_orchestrator.py # Defective simulation script
│   └── ANSWERS.md                     # Root cause forensic analysis & fix
├── project_solution/                  # Complete, verified reference implementation
│   ├── saga_orchestrator.py
│   └── test_saga_orchestrator.py
└── starter/                           # Student boilerplate raising NotImplementedError
    ├── conftest.py
    └── saga_orchestrator.py
```

---

## 4. You Have Mastered This Module When You Can…

Mastery is a demonstrated capability, not just passive reading. You have truly mastered this module when you can confidently check every box:

- [ ] Explain why Two-Phase Commit (2PC) is an anti-pattern in high-scale microservices.
- [ ] Differentiate Choreography-based Sagas vs. Orchestration-based Sagas.
- [ ] Design idempotent compensating transactions that handle out-of-order execution safely.
- [ ] Implement the Transactional Outbox pattern to solve the Dual-Write distributed inconsistency problem.
- [ ] Explain the semantic trade-offs of BASE vs. ACID.
- [ ] Handle catastrophic compensation failures through dead-letter queues and manual operational runbooks.
