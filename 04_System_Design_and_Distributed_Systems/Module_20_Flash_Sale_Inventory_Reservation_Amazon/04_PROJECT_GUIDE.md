# Module_20_Flash_Sale_Inventory_Reservation_Amazon: Project Implementation Guide

**Deliverable:** a high-concurrency flash sale inventory reservation engine preventing overselling using atomic tokens, TTL leases, and background rollback reapers.

---

## 🎯 3-Tier Progressive Learning Path

| Tier | For you if… | You build | Estimated Time |
| :--- | :--- | :--- | :--- |
| **Tier 1 — Novice Walkthrough** | You are learning the core concepts and basic mechanics | Demonstrate the classic overselling race condition with naive non-atomic read-then-write updates. | ~2 hrs |
| **Tier 2 — Core Project** | Tier 1 passes completely and you want production quality | Implement atomic inventory reservation issuing time-bounded cryptographically signed tokens. | ~3 hrs |
| **Tier 3 — Architect Stretch** | You want production-hardened, high-throughput systems | Build a background lease-reaper worker that automatically rolls back expired unconfirmed reservations. | ~2.5 hrs |

### Setup for All Tiers

Verify your working directory and execute the test suite:
```bash
cd "System Design/Module_20_Flash_Sale_Inventory_Reservation_Amazon"
pytest project_solution/test_flash_sale_engine.py -v
```

Before writing code, verify your test environment imports the starter directory:
```bash
cd starter
pytest ../project_solution/test_flash_sale_engine.py -v
```
All starter stubs initially raise `NotImplementedError`. Your goal is to replace each stub with a working, production-grade implementation.

---

## 1. Architectural Blueprint & Invariants

```

      100,000 Concurrent Buyers -> [ Rate Limiting & Token Bucket ]
                                                |
                                 [ In-Memory Inventory Store ]
                                 (Atomic DECR / Reservation Token)
                                                |
                               +----------------+----------------+
                               | Paid within 15 min              | Payment Timeout
                               v                                 v
                       [ Confirm Purchase ]            [ Background Reaper ]
                       (Deduct permanent)              (Release Inventory Stock)

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
- Implement `NaiveInventoryStore` showing how concurrent purchases oversell limited stock.
- Ensure initialization parameters are validated against boundary conditions.

#### Step 2: Core Algorithmic Mechanics
- Build `AtomicReservationEngine` with thread-safe atomic decrement and reservation token generation.
- Implement pure deterministic helper functions first.

### 🛑 Stop Here Until This Works!
Run the test suite for Tier 1:
```bash
pytest project_solution/test_flash_sale_engine.py -k "basic or initial or create or test_1" -v
```
Do not proceed to Tier 2 until all baseline data structure and creation checks pass cleanly.

---

### Phase B: Tier 2 — Core Production Project

#### Step 3: Concurrency, Error Isolation & Edge Cases
- Implement `confirm_purchase(token_id)` marking reservation as finalized and permanently committing stock.
- Guard against concurrent mutations and race conditions where applicable.

#### Step 4: End-to-End Orchestration
- Implement `release_expired_reservations()` reclaiming stock for tokens past their 15-minute lease.
- Connect the core engine to its secondary components and test full end-to-end operational flows.

### 🛑 Stop Here Until This Works!
Run the full automated test suite:
```bash
pytest project_solution/test_flash_sale_engine.py -v
```
Every single test in `project_solution/test_flash_sale_engine.py` must pass with zero failures and zero warnings.

---

### Phase C: Tier 3 — Architect Stretch Challenge

#### Step 5: High-Scale & Fault-Tolerant Extension
- Benchmark peak throughput under 50 concurrent threads contesting the final 10 items in stock.
- Benchmark your implementation under synthetic stress or failure injections.
- Measure latency percentiles, memory footprints, and resource reclamation behavior.

---

## 3. Directory Layout

```
Module_20_Flash_Sale_Inventory_Reservation_Amazon/
├── 00_interactive_*.ipynb            # Interactive architectural exploration notebook
├── README.md                          # Deep-dive theory, trade-off matrices, and blueprints
├── SELF_ASSESSMENT_AND_CHALLENGES.md  # 10 diagnostic questions + 3 design challenges
├── PROJECT_GUIDE.md                   # This step-by-step implementation guide
├── TROUBLESHOOTING_AND_EDGE_CASES.md  # Real-world production failure post-mortems
├── debug_lab/                         # Intentional production defect lab & answers
│   ├── SYMPTOMS.md                    # P1 incident report & reproduction steps
│   ├── broken_flash_sale_engine.py # Defective simulation script
│   └── ANSWERS.md                     # Root cause forensic analysis & fix
├── project_solution/                  # Complete, verified reference implementation
│   ├── flash_sale_engine.py
│   └── test_flash_sale_engine.py
└── starter/                           # Student boilerplate raising NotImplementedError
    ├── conftest.py
    └── flash_sale_engine.py
```

---

## 4. You Have Mastered This Module When You Can…

Mastery is a demonstrated capability, not just passive reading. You have truly mastered this module when you can confidently check every box:

- [ ] Explain how the race condition occurs in non-atomic inventory updates under high concurrency.
- [ ] Implement two-phase inventory reservation (reserve with lease TTL -> confirm on payment settlement).
- [ ] Use Redis Lua scripts or atomic DECR operations to prevent overselling at the caching tier.
- [ ] Design background rollback reapers that return expired reserved inventory back to available stock.
- [ ] Protect core database infrastructure using upstream traffic shaping, virtual waiting rooms, and token gates.
- [ ] Ensure idempotency across payment webhooks and inventory finalization events.
