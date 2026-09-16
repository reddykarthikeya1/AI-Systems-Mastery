# Module_15_RealTime_Chat_Presence_System_Discord: Project Implementation Guide

**Deliverable:** a horizontally scalable real-time chat and user presence platform with WebSocket gateway routing and offline mailboxes.

---

## 🎯 3-Tier Progressive Learning Path

| Tier | For you if… | You build | Estimated Time |
| :--- | :--- | :--- | :--- |
| **Tier 1 — Novice Walkthrough** | You are learning the core concepts and basic mechanics | Model direct and group chat message routing across connected gateway sessions. | ~2 hrs |
| **Tier 2 — Core Project** | Tier 1 passes completely and you want production quality | Build heartbeat-based user presence tracking (`ONLINE`, `IDLE`, `OFFLINE`) with ephemeral timeouts. | ~3 hrs |
| **Tier 3 — Architect Stretch** | You want production-hardened, high-throughput systems | Implement offline mailbox queuing, history pagination, and cross-gateway Pub/Sub broadcast fanout. | ~2.5 hrs |

### Setup for All Tiers

Verify your working directory and execute the test suite:
```bash
cd "System Design/Module_15_RealTime_Chat_Presence_System_Discord"
pytest project_solution/test_chat_presence_platform.py -v
```

Before writing code, verify your test environment imports the starter directory:
```bash
cd starter
pytest ../project_solution/test_chat_presence_platform.py -v
```
All starter stubs initially raise `NotImplementedError`. Your goal is to replace each stub with a working, production-grade implementation.

---

## 1. Architectural Blueprint & Invariants

```

      User A (WebSocket) -> [ Chat Gateway 1 ] ----+
                                                    |---> [ Redis Pub/Sub / Message Bus ]
      User B (WebSocket) -> [ Chat Gateway 2 ] ----+                 |
                                                                     v
                                                          [ Offline Mailbox Queue ]

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
- Define `ChatMessage` and `UserStatus` schemas with timestamps and UUIDs.
- Ensure initialization parameters are validated against boundary conditions.

#### Step 2: Core Algorithmic Mechanics
- Implement `PresenceTracker` updating heartbeats and reaping idle users after 30s timeout.
- Implement pure deterministic helper functions first.

### 🛑 Stop Here Until This Works!
Run the test suite for Tier 1:
```bash
pytest project_solution/test_chat_presence_platform.py -k "basic or initial or create or test_1" -v
```
Do not proceed to Tier 2 until all baseline data structure and creation checks pass cleanly.

---

### Phase B: Tier 2 — Core Production Project

#### Step 3: Concurrency, Error Isolation & Edge Cases
- Build cross-gateway routing dispatching messages to recipient session handlers.
- Guard against concurrent mutations and race conditions where applicable.

#### Step 4: End-to-End Orchestration
- Implement offline message spooling: queue unread messages and flush immediately upon client reconnection.
- Connect the core engine to its secondary components and test full end-to-end operational flows.

### 🛑 Stop Here Until This Works!
Run the full automated test suite:
```bash
pytest project_solution/test_chat_presence_platform.py -v
```
Every single test in `project_solution/test_chat_presence_platform.py` must pass with zero failures and zero warnings.

---

### Phase C: Tier 3 — Architect Stretch Challenge

#### Step 5: High-Scale & Fault-Tolerant Extension
- Simulate network disconnections and verify presence states update without flapping.
- Benchmark your implementation under synthetic stress or failure injections.
- Measure latency percentiles, memory footprints, and resource reclamation behavior.

---

## 3. Directory Layout

```
Module_15_RealTime_Chat_Presence_System_Discord/
├── 00_interactive_*.ipynb            # Interactive architectural exploration notebook
├── README.md                          # Deep-dive theory, trade-off matrices, and blueprints
├── SELF_ASSESSMENT_AND_CHALLENGES.md  # 10 diagnostic questions + 3 design challenges
├── PROJECT_GUIDE.md                   # This step-by-step implementation guide
├── TROUBLESHOOTING_AND_EDGE_CASES.md  # Real-world production failure post-mortems
├── debug_lab/                         # Intentional production defect lab & answers
│   ├── SYMPTOMS.md                    # P1 incident report & reproduction steps
│   ├── broken_chat_presence_platform.py # Defective simulation script
│   └── ANSWERS.md                     # Root cause forensic analysis & fix
├── project_solution/                  # Complete, verified reference implementation
│   ├── chat_presence_platform.py
│   └── test_chat_presence_platform.py
└── starter/                           # Student boilerplate raising NotImplementedError
    ├── conftest.py
    └── chat_presence_platform.py
```

---

## 4. You Have Mastered This Module When You Can…

Mastery is a demonstrated capability, not just passive reading. You have truly mastered this module when you can confidently check every box:

- [ ] Architect bi-directional real-time communication using WebSockets and connection-state affinity.
- [ ] Design scalable user presence tracking systems handling millions of concurrent user heartbeats.
- [ ] Prevent presence update storms when a celebrity with 10,000 friends logs in or disconnects.
- [ ] Design offline message spooling and sync protocols guaranteeing at-least-once message delivery.
- [ ] Compare storage engines for chat history: Cassandra/ScyllaDB wide-column vs. PostgreSQL partitioned tables.
- [ ] Implement end-to-end message sequence ordering across multiple chat participants.
