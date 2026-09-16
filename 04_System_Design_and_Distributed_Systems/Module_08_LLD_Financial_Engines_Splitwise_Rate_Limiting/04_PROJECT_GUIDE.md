# Module_08_LLD_Financial_Engines_Splitwise_Rate_Limiting: Project Implementation Guide

**Deliverable:** a financial expense sharing engine with exact penny rounding, debt graph minimization, and thread-safe Token Bucket rate limiters.

---

## 🎯 3-Tier Progressive Learning Path

| Tier | For you if… | You build | Estimated Time |
| :--- | :--- | :--- | :--- |
| **Tier 1 — Novice Walkthrough** | You are learning the core concepts and basic mechanics | Implement equal and percentage-based expense splits with penny-rounding conservation. | ~2 hrs |
| **Tier 2 — Core Project** | Tier 1 passes completely and you want production quality | Build the greedy balance minimization algorithm to reduce $N$ debts to minimal transactions. | ~3 hrs |
| **Tier 3 — Architect Stretch** | You want production-hardened, high-throughput systems | Implement a high-throughput, thread-safe Token Bucket rate limiter protecting transaction endpoints. | ~2.5 hrs |

### Setup for All Tiers

Verify your working directory and execute the test suite:
```bash
cd "System Design/Module_08_LLD_Financial_Engines_Splitwise_Rate_Limiting"
pytest project_solution/test_splitwise_engine.py -v
```

Before writing code, verify your test environment imports the starter directory:
```bash
cd starter
pytest ../project_solution/test_splitwise_engine.py -v
```
All starter stubs initially raise `NotImplementedError`. Your goal is to replace each stub with a working, production-grade implementation.

---

## 1. Architectural Blueprint & Invariants

```

       Alice owes Bob $10        Bob owes Charlie $10
                \                        /
                 \                      /
                  +---- Debt Graph ----+
                            |
                 [Greedy Graph Simplification]
                            |
                     v                      v
             Alice pays Charlie $10 (1 transaction instead of 2)

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
- Implement `Split` and `Transaction` models enforcing total sum equality down to the exact cent.
- Ensure initialization parameters are validated against boundary conditions.

#### Step 2: Core Algorithmic Mechanics
- Build user balance sheet computing net credit/debit balances across all participants.
- Implement pure deterministic helper functions first.

### 🛑 Stop Here Until This Works!
Run the test suite for Tier 1:
```bash
pytest project_solution/test_splitwise_engine.py -k "basic or initial or create or test_1" -v
```
Do not proceed to Tier 2 until all baseline data structure and creation checks pass cleanly.

---

### Phase B: Tier 2 — Core Production Project

#### Step 3: Concurrency, Error Isolation & Edge Cases
- Implement `simplify_debts()`: separate net debtors and net creditors, repeatedly settle maximum balances.
- Guard against concurrent mutations and race conditions where applicable.

#### Step 4: End-to-End Orchestration
- Implement `TokenBucketRateLimiter` with lock-free or atomic timestamp refills.
- Connect the core engine to its secondary components and test full end-to-end operational flows.

### 🛑 Stop Here Until This Works!
Run the full automated test suite:
```bash
pytest project_solution/test_splitwise_engine.py -v
```
Every single test in `project_solution/test_splitwise_engine.py` must pass with zero failures and zero warnings.

---

### Phase C: Tier 3 — Architect Stretch Challenge

#### Step 5: High-Scale & Fault-Tolerant Extension
- Verify zero-sum financial invariant: the sum of all participant balances must equal exactly 0.00.
- Benchmark your implementation under synthetic stress or failure injections.
- Measure latency percentiles, memory footprints, and resource reclamation behavior.

---

## 3. Directory Layout

```
Module_08_LLD_Financial_Engines_Splitwise_Rate_Limiting/
├── 00_interactive_*.ipynb            # Interactive architectural exploration notebook
├── README.md                          # Deep-dive theory, trade-off matrices, and blueprints
├── SELF_ASSESSMENT_AND_CHALLENGES.md  # 10 diagnostic questions + 3 design challenges
├── PROJECT_GUIDE.md                   # This step-by-step implementation guide
├── TROUBLESHOOTING_AND_EDGE_CASES.md  # Real-world production failure post-mortems
├── debug_lab/                         # Intentional production defect lab & answers
│   ├── SYMPTOMS.md                    # P1 incident report & reproduction steps
│   ├── broken_splitwise_engine.py # Defective simulation script
│   └── ANSWERS.md                     # Root cause forensic analysis & fix
├── project_solution/                  # Complete, verified reference implementation
│   ├── splitwise_engine.py
│   └── test_splitwise_engine.py
└── starter/                           # Student boilerplate raising NotImplementedError
    ├── conftest.py
    └── splitwise_engine.py
```

---

## 4. You Have Mastered This Module When You Can…

Mastery is a demonstrated capability, not just passive reading. You have truly mastered this module when you can confidently check every box:

- [ ] Preserve exact currency conservation invariants without floating-point representation loss.
- [ ] Solve debt graph simplification using greedy settlement and understand when it approximates min-cash-flow NP-hard solutions.
- [ ] Implement thread-safe token bucket and leaky bucket rate limiters under high concurrency.
- [ ] Explain the difference between proportional, percentage, and exact split models in financial ledgers.
- [ ] Detect and prevent debt cycles in peer-to-peer settlement networks.
- [ ] Design idempotent payment intent endpoints that prevent double-charging.
