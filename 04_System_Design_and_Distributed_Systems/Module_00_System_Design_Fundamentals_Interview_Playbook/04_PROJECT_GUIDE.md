# Module_00_System_Design_Fundamentals_Interview_Playbook: Project Implementation Guide

**Deliverable:** an interview capacity calculator and bandwidth/storage estimation engine to navigate 45-minute architectural whiteboard sessions.

---

## 🎯 3-Tier Progressive Learning Path

| Tier | For you if… | You build | Estimated Time |
| :--- | :--- | :--- | :--- |
| **Tier 1 — Novice Walkthrough** | You are learning the core concepts and basic mechanics | Implement basic QPS estimation and daily ingest volume calculation. | ~2 hrs |
| **Tier 2 — Core Project** | Tier 1 passes completely and you want production quality | Build peak headroom multipliers, storage retention math with replication factor, and bandwidth egress/ingress estimations. | ~3 hrs |
| **Tier 3 — Architect Stretch** | You want production-hardened, high-throughput systems | Add dynamic hardware sizing recommendations (CPU cores, RAM cache sizing by 80/20 Pareto rule, NVMe SSD IOPS provisioning). | ~2.5 hrs |

### Setup for All Tiers

Verify your working directory and execute the test suite:
```bash
cd "System Design/Module_00_System_Design_Fundamentals_Interview_Playbook"
pytest project_solution/test_interview_capacity_calculator.py -v
```

Before writing code, verify your test environment imports the starter directory:
```bash
cd starter
pytest ../project_solution/test_interview_capacity_calculator.py -v
```
All starter stubs initially raise `NotImplementedError`. Your goal is to replace each stub with a working, production-grade implementation.

---

## 1. Architectural Blueprint & Invariants

```

     +-------------------------------------------------------------+
     |             45-Minute Interview Navigation Loop             |
     | [00-05m Scope & Clarify] -> [05-15m High-Level Design]      |
     |        -> [15-35m Deep-Dive] -> [35-45m Failure & Bottlenecks]|
     +-------------------------------------------------------------+
                                    |
                    +---------------+---------------+
                    v                               v
       [Capacity & QPS Calculator]     [Storage & Bandwidth Matrix]
       (Peak Multipliers, Headroom)    (IOPS, RAM, Ingress/Egress)

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
- Implement `estimate_qps(dau, actions_per_day, peak_factor)` with defensive checks for zero or negative DAU.
- Ensure initialization parameters are validated against boundary conditions.

#### Step 2: Core Algorithmic Mechanics
- Implement `calculate_daily_storage(qps, payload_bytes, replication_factor)` converting to GiB and TiB.
- Implement pure deterministic helper functions first.

### 🛑 Stop Here Until This Works!
Run the test suite for Tier 1:
```bash
pytest project_solution/test_interview_capacity_calculator.py -k "basic or initial or create or test_1" -v
```
Do not proceed to Tier 2 until all baseline data structure and creation checks pass cleanly.

---

### Phase B: Tier 2 — Core Production Project

#### Step 3: Concurrency, Error Isolation & Edge Cases
- Implement `estimate_network_bandwidth(qps, read_ratio, write_bytes, read_bytes)` with egress/ingress separation.
- Guard against concurrent mutations and race conditions where applicable.

#### Step 4: End-to-End Orchestration
- Add Pareto 80/20 cache sizing: 20% of daily active working set cached in memory.
- Connect the core engine to its secondary components and test full end-to-end operational flows.

### 🛑 Stop Here Until This Works!
Run the full automated test suite:
```bash
pytest project_solution/test_interview_capacity_calculator.py -v
```
Every single test in `project_solution/test_interview_capacity_calculator.py` must pass with zero failures and zero warnings.

---

### Phase C: Tier 3 — Architect Stretch Challenge

#### Step 5: High-Scale & Fault-Tolerant Extension
- Formulate a full 45-minute mock interview rubric evaluation report.
- Benchmark your implementation under synthetic stress or failure injections.
- Measure latency percentiles, memory footprints, and resource reclamation behavior.

---

## 3. Directory Layout

```
Module_00_System_Design_Fundamentals_Interview_Playbook/
├── 00_interactive_*.ipynb            # Interactive architectural exploration notebook
├── README.md                          # Deep-dive theory, trade-off matrices, and blueprints
├── SELF_ASSESSMENT_AND_CHALLENGES.md  # 10 diagnostic questions + 3 design challenges
├── PROJECT_GUIDE.md                   # This step-by-step implementation guide
├── TROUBLESHOOTING_AND_EDGE_CASES.md  # Real-world production failure post-mortems
├── debug_lab/                         # Intentional production defect lab & answers
│   ├── SYMPTOMS.md                    # P1 incident report & reproduction steps
│   ├── broken_interview_capacity_calculator.py # Defective simulation script
│   └── ANSWERS.md                     # Root cause forensic analysis & fix
├── project_solution/                  # Complete, verified reference implementation
│   ├── interview_capacity_calculator.py
│   └── test_interview_capacity_calculator.py
└── starter/                           # Student boilerplate raising NotImplementedError
    ├── conftest.py
    └── interview_capacity_calculator.py
```

---

## 4. You Have Mastered This Module When You Can…

Mastery is a demonstrated capability, not just passive reading. You have truly mastered this module when you can confidently check every box:

- [ ] Calculate peak QPS, ingress bandwidth, and multi-year disk requirements mentally in under 60 seconds.
- [ ] Decompose a vague requirements prompt into hard functional vs. non-functional requirements.
- [ ] Apply the 80/20 Pareto principle to size cache memory for any distributed tier.
- [ ] Structure an architectural whiteboard interview cleanly across the standard 4-stage time budget.
- [ ] Identify single points of failure (SPOFs) in a multi-tier client-loadbalancer-service-db topology.
- [ ] Articulate the fundamental trade-offs between consistency models (strong vs. eventual) under network partitions.
