# Module_04_Load_Balancing_Algorithms_Health_Probes: Project Implementation Guide

**Deliverable:** a production-grade load balancing engine implementing Round-Robin, Weighted Round-Robin, Least Connections, and Consistent IP Hashing.

---

## 🎯 3-Tier Progressive Learning Path

| Tier | For you if… | You build | Estimated Time |
| :--- | :--- | :--- | :--- |
| **Tier 1 — Novice Walkthrough** | You are learning the core concepts and basic mechanics | Implement deterministic Round Robin and Weighted Round Robin balancing. | ~2 hrs |
| **Tier 2 — Core Project** | Tier 1 passes completely and you want production quality | Build Least Connections strategy and IP Hashing session affinity with dynamic server weights. | ~3 hrs |
| **Tier 3 — Architect Stretch** | You want production-hardened, high-throughput systems | Implement adaptive latency-weighted balancing and smooth weighted round-robin (Nginx algorithm) with flapping prevention. | ~2.5 hrs |

### Setup for All Tiers

Verify your working directory and execute the test suite:
```bash
cd "System Design/Module_04_Load_Balancing_Algorithms_Health_Probes"
pytest project_solution/test_load_balancer.py -v
```

Before writing code, verify your test environment imports the starter directory:
```bash
cd starter
pytest ../project_solution/test_load_balancer.py -v
```
All starter stubs initially raise `NotImplementedError`. Your goal is to replace each stub with a working, production-grade implementation.

---

## 1. Architectural Blueprint & Invariants

```

                          [ Load Balancer ]
                                  |
         +------------------------+------------------------+
         | (Round-Robin)          | (Least-Connections)   | (IP Hash)
         v                        v                        v
    [Server A: 2 conn]       [Server B: 0 conn]       [Server C: 5 conn]

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
- Define `BackendServer` entity with weight, active_conns, and `HealthStatus`.
- Ensure initialization parameters are validated against boundary conditions.

#### Step 2: Core Algorithmic Mechanics
- Implement standard and weighted Round Robin dispatch state machines.
- Implement pure deterministic helper functions first.

### 🛑 Stop Here Until This Works!
Run the test suite for Tier 1:
```bash
pytest project_solution/test_load_balancer.py -k "basic or initial or create or test_1" -v
```
Do not proceed to Tier 2 until all baseline data structure and creation checks pass cleanly.

---

### Phase B: Tier 2 — Core Production Project

#### Step 3: Concurrency, Error Isolation & Edge Cases
- Implement Least Connections strategy breaking ties via server index or weight.
- Guard against concurrent mutations and race conditions where applicable.

#### Step 4: End-to-End Orchestration
- Implement IP Hashing for sticky session persistence with fallback on server removal.
- Connect the core engine to its secondary components and test full end-to-end operational flows.

### 🛑 Stop Here Until This Works!
Run the full automated test suite:
```bash
pytest project_solution/test_load_balancer.py -v
```
Every single test in `project_solution/test_load_balancer.py` must pass with zero failures and zero warnings.

---

### Phase C: Tier 3 — Architect Stretch Challenge

#### Step 5: High-Scale & Fault-Tolerant Extension
- Add consecutive failure thresholds and recovery probe intervals to eliminate flapping.
- Benchmark your implementation under synthetic stress or failure injections.
- Measure latency percentiles, memory footprints, and resource reclamation behavior.

---

## 3. Directory Layout

```
Module_04_Load_Balancing_Algorithms_Health_Probes/
├── 00_interactive_*.ipynb            # Interactive architectural exploration notebook
├── README.md                          # Deep-dive theory, trade-off matrices, and blueprints
├── SELF_ASSESSMENT_AND_CHALLENGES.md  # 10 diagnostic questions + 3 design challenges
├── PROJECT_GUIDE.md                   # This step-by-step implementation guide
├── TROUBLESHOOTING_AND_EDGE_CASES.md  # Real-world production failure post-mortems
├── debug_lab/                         # Intentional production defect lab & answers
│   ├── SYMPTOMS.md                    # P1 incident report & reproduction steps
│   ├── broken_load_balancer.py # Defective simulation script
│   └── ANSWERS.md                     # Root cause forensic analysis & fix
├── project_solution/                  # Complete, verified reference implementation
│   ├── load_balancer.py
│   └── test_load_balancer.py
└── starter/                           # Student boilerplate raising NotImplementedError
    ├── conftest.py
    └── load_balancer.py
```

---

## 4. You Have Mastered This Module When You Can…

Mastery is a demonstrated capability, not just passive reading. You have truly mastered this module when you can confidently check every box:

- [ ] Contrast Layer 4 (Transport/TCP) vs. Layer 7 (Application/HTTP) load balancing architectures.
- [ ] Implement and mathematically analyze Weighted Round-Robin vs. Smooth Weighted Round-Robin.
- [ ] Explain how the Least Connections algorithm prevents slow-request server starvation.
- [ ] Design health checking systems that avoid the 'flapping cascade' failure mode.
- [ ] Differentiate hardware load balancers (F5) from software load balancers (Nginx, HAProxy, Envoy).
- [ ] Handle connection draining (graceful shutdown) during rolling deployments.
