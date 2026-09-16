# Module_07_LLD_State_Machines_Scheduling_Elevator_Parking: Project Implementation Guide

**Deliverable:** a multi-car elevator control system featuring SCAN/LOOK disk-scheduling algorithms, finite state machines, and nearest-car dispatch.

---

## 🎯 3-Tier Progressive Learning Path

| Tier | For you if… | You build | Estimated Time |
| :--- | :--- | :--- | :--- |
| **Tier 1 — Novice Walkthrough** | You are learning the core concepts and basic mechanics | Model `ElevatorCar` state transitions (`IDLE`, `MOVING_UP`, `MOVING_DOWN`) and door states (`OPEN`, `CLOSED`). | ~2 hrs |
| **Tier 2 — Core Project** | Tier 1 passes completely and you want production quality | Implement the classic LOOK/SCAN scheduling algorithm serving requests in the current direction before reversing. | ~3 hrs |
| **Tier 3 — Architect Stretch** | You want production-hardened, high-throughput systems | Build multi-car supervisory controller with cost-function dispatch minimizing passenger wait times and energy usage. | ~2.5 hrs |

### Setup for All Tiers

Verify your working directory and execute the test suite:
```bash
cd "System Design/Module_07_LLD_State_Machines_Scheduling_Elevator_Parking"
pytest project_solution/test_elevator_system.py -v
```

Before writing code, verify your test environment imports the starter directory:
```bash
cd starter
pytest ../project_solution/test_elevator_system.py -v
```
All starter stubs initially raise `NotImplementedError`. Your goal is to replace each stub with a working, production-grade implementation.

---

## 1. Architectural Blueprint & Invariants

```

      Car 1 [Moving UP, Floor 7]        Car 2 [IDLE, Floor 2]
                |                                 |
         +-------------------------------------------------+
         |            LOOK Dispatch Controller             |
         | Evaluates Hall Calls (Floor, Direction)         |
         | Computes Minimal Distance + Directional Penalty |
         +-------------------------------------------------+

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
- Define `Direction`, `DoorState`, and `HallCall` data classes.
- Ensure initialization parameters are validated against boundary conditions.

#### Step 2: Core Algorithmic Mechanics
- Implement single-car step loop: move to target floor, open doors, unload/load passengers, close doors.
- Implement pure deterministic helper functions first.

### 🛑 Stop Here Until This Works!
Run the test suite for Tier 1:
```bash
pytest project_solution/test_elevator_system.py -k "basic or initial or create or test_1" -v
```
Do not proceed to Tier 2 until all baseline data structure and creation checks pass cleanly.

---

### Phase B: Tier 2 — Core Production Project

#### Step 3: Concurrency, Error Isolation & Edge Cases
- Implement LOOK algorithm: maintain sorted target sets for upward and downward trips.
- Guard against concurrent mutations and race conditions where applicable.

#### Step 4: End-to-End Orchestration
- Implement multi-car `ElevatorController` assigning hall calls based on directional alignment and distance.
- Connect the core engine to its secondary components and test full end-to-end operational flows.

### 🛑 Stop Here Until This Works!
Run the full automated test suite:
```bash
pytest project_solution/test_elevator_system.py -v
```
Every single test in `project_solution/test_elevator_system.py` must pass with zero failures and zero warnings.

---

### Phase C: Tier 3 — Architect Stretch Challenge

#### Step 5: High-Scale & Fault-Tolerant Extension
- Simulate peak-hour traffic patterns and measure average passenger wait times.
- Benchmark your implementation under synthetic stress or failure injections.
- Measure latency percentiles, memory footprints, and resource reclamation behavior.

---

## 3. Directory Layout

```
Module_07_LLD_State_Machines_Scheduling_Elevator_Parking/
├── 00_interactive_*.ipynb            # Interactive architectural exploration notebook
├── README.md                          # Deep-dive theory, trade-off matrices, and blueprints
├── SELF_ASSESSMENT_AND_CHALLENGES.md  # 10 diagnostic questions + 3 design challenges
├── PROJECT_GUIDE.md                   # This step-by-step implementation guide
├── TROUBLESHOOTING_AND_EDGE_CASES.md  # Real-world production failure post-mortems
├── debug_lab/                         # Intentional production defect lab & answers
│   ├── SYMPTOMS.md                    # P1 incident report & reproduction steps
│   ├── broken_elevator_system.py # Defective simulation script
│   └── ANSWERS.md                     # Root cause forensic analysis & fix
├── project_solution/                  # Complete, verified reference implementation
│   ├── elevator_system.py
│   └── test_elevator_system.py
└── starter/                           # Student boilerplate raising NotImplementedError
    ├── conftest.py
    └── elevator_system.py
```

---

## 4. You Have Mastered This Module When You Can…

Mastery is a demonstrated capability, not just passive reading. You have truly mastered this module when you can confidently check every box:

- [ ] Implement deterministic finite state machines (FSM) with strict state transition validation.
- [ ] Explain why the LOOK/SCAN algorithm prevents elevator passenger and disk I/O starvation.
- [ ] Design cost-heuristic dispatchers for concurrent multi-agent resource allocation.
- [ ] Prevent race conditions when multiple concurrent users summon elevators simultaneously.
- [ ] Handle edge cases: emergency stops, floor bounds checking, and capacity overload sensors.
- [ ] Represent state machine logic cleanly without deeply nested if/else statements.
