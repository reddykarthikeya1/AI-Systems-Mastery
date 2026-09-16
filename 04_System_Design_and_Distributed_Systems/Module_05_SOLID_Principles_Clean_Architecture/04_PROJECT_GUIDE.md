# Module_05_SOLID_Principles_Clean_Architecture: Project Implementation Guide

**Deliverable:** an enterprise Clean Architecture checkout system featuring Domain-Driven Design (DDD) aggregate roots, value objects, and dependency inversion.

---

## 🎯 3-Tier Progressive Learning Path

| Tier | For you if… | You build | Estimated Time |
| :--- | :--- | :--- | :--- |
| **Tier 1 — Novice Walkthrough** | You are learning the core concepts and basic mechanics | Model immutable value objects (`Money`, `OrderItem`) enforcing domain validation invariants. | ~2 hrs |
| **Tier 2 — Core Project** | Tier 1 passes completely and you want production quality | Build `Order` aggregate root managing line items, total calculations, and lifecycle status transitions. | ~3 hrs |
| **Tier 3 — Architect Stretch** | You want production-hardened, high-throughput systems | Implement `CheckoutUseCase` with mockable repository/payment ports, domain event publishing, and compensation rollback. | ~2.5 hrs |

### Setup for All Tiers

Verify your working directory and execute the test suite:
```bash
cd "System Design/Module_05_SOLID_Principles_Clean_Architecture"
pytest project_solution/test_clean_checkout.py -v
```

Before writing code, verify your test environment imports the starter directory:
```bash
cd starter
pytest ../project_solution/test_clean_checkout.py -v
```
All starter stubs initially raise `NotImplementedError`. Your goal is to replace each stub with a working, production-grade implementation.

---

## 1. Architectural Blueprint & Invariants

```

      [ External Frameworks / DB / HTTP Controllers ]
                             |
         [ Interface Adapters / Repositories / Gateways ]
                             |
             [ Use Cases / Application Services ]
                             |
                 [ Domain Entities & Value Objects ]

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
- Implement `Money` value object with currency matching rules and non-negative assertions.
- Ensure initialization parameters are validated against boundary conditions.

#### Step 2: Core Algorithmic Mechanics
- Implement `Order` aggregate enforcing transitions: `DRAFT` -> `CONFIRMED` -> `PAID`.
- Implement pure deterministic helper functions first.

### 🛑 Stop Here Until This Works!
Run the test suite for Tier 1:
```bash
pytest project_solution/test_clean_checkout.py -k "basic or initial or create or test_1" -v
```
Do not proceed to Tier 2 until all baseline data structure and creation checks pass cleanly.

---

### Phase B: Tier 2 — Core Production Project

#### Step 3: Concurrency, Error Isolation & Edge Cases
- Define abstract protocol interfaces for `InventoryGateway`, `PaymentGateway`, and `OrderRepository`.
- Guard against concurrent mutations and race conditions where applicable.

#### Step 4: End-to-End Orchestration
- Assemble `CheckoutUseCase` coordinating transaction boundaries and emitting `OrderPaidEvent`.
- Connect the core engine to its secondary components and test full end-to-end operational flows.

### 🛑 Stop Here Until This Works!
Run the full automated test suite:
```bash
pytest project_solution/test_clean_checkout.py -v
```
Every single test in `project_solution/test_clean_checkout.py` must pass with zero failures and zero warnings.

---

### Phase C: Tier 3 — Architect Stretch Challenge

#### Step 5: High-Scale & Fault-Tolerant Extension
- Test resilience by simulating payment gateway timeout and verifying inventory reservation rollback.
- Benchmark your implementation under synthetic stress or failure injections.
- Measure latency percentiles, memory footprints, and resource reclamation behavior.

---

## 3. Directory Layout

```
Module_05_SOLID_Principles_Clean_Architecture/
├── 00_interactive_*.ipynb            # Interactive architectural exploration notebook
├── README.md                          # Deep-dive theory, trade-off matrices, and blueprints
├── SELF_ASSESSMENT_AND_CHALLENGES.md  # 10 diagnostic questions + 3 design challenges
├── PROJECT_GUIDE.md                   # This step-by-step implementation guide
├── TROUBLESHOOTING_AND_EDGE_CASES.md  # Real-world production failure post-mortems
├── debug_lab/                         # Intentional production defect lab & answers
│   ├── SYMPTOMS.md                    # P1 incident report & reproduction steps
│   ├── broken_clean_checkout.py # Defective simulation script
│   └── ANSWERS.md                     # Root cause forensic analysis & fix
├── project_solution/                  # Complete, verified reference implementation
│   ├── clean_checkout.py
│   └── test_clean_checkout.py
└── starter/                           # Student boilerplate raising NotImplementedError
    ├── conftest.py
    └── clean_checkout.py
```

---

## 4. You Have Mastered This Module When You Can…

Mastery is a demonstrated capability, not just passive reading. You have truly mastered this module when you can confidently check every box:

- [ ] Apply the Single Responsibility and Dependency Inversion principles to decouple domain from databases.
- [ ] Distinguish between Entities, Value Objects, Aggregates, and Domain Events in DDD.
- [ ] Enforce transactional boundaries around aggregate roots without leaking persistence concerns.
- [ ] Structure Hexagonal / Clean Architecture ports and adapters in production codebases.
- [ ] Design idempotent domain methods resistant to repeated invocation.
- [ ] Refactor tightly-coupled spaghetti code into testable, mockable domain layers.
