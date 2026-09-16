# Module_16_Social_Media_Newsfeed_Recommendation_TwoTower: Project Implementation Guide

**Deliverable:** a hybrid Fan-out-on-Write and Fan-out-on-Read newsfeed platform with Two-Tower vector candidate retrieval and ranking.

---

## 🎯 3-Tier Progressive Learning Path

| Tier | For you if… | You build | Estimated Time |
| :--- | :--- | :--- | :--- |
| **Tier 1 — Novice Walkthrough** | You are learning the core concepts and basic mechanics | Implement Fan-out-on-Write for normal users pushing posts to follower inboxes. | ~2 hrs |
| **Tier 2 — Core Project** | Tier 1 passes completely and you want production quality | Build hybrid feed merging: pull celebrity posts at read-time to prevent write amplification disasters. | ~3 hrs |
| **Tier 3 — Architect Stretch** | You want production-hardened, high-throughput systems | Implement Two-Tower vector candidate retrieval scoring user-post affinity via cosine similarity. | ~2.5 hrs |

### Setup for All Tiers

Verify your working directory and execute the test suite:
```bash
cd "System Design/Module_16_Social_Media_Newsfeed_Recommendation_TwoTower"
pytest project_solution/test_newsfeed_recommendation_engine.py -v
```

Before writing code, verify your test environment imports the starter directory:
```bash
cd starter
pytest ../project_solution/test_newsfeed_recommendation_engine.py -v
```
All starter stubs initially raise `NotImplementedError`. Your goal is to replace each stub with a working, production-grade implementation.

---

## 1. Architectural Blueprint & Invariants

```

      Standard User Posts  --> Fan-Out-on-Write (Push to all follower inboxes)
      Celebrity Posts      --> Fan-Out-on-Read  (Pull and merge at feed query time)
                                    |
                                    v
            [ Two-Tower Recommendation: User Tower dot Item Tower ]
                                    |
                            Top-K Ranked Feed

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
- Model `Post` and `UserProfile` entities with follower/following graph relationships.
- Ensure initialization parameters are validated against boundary conditions.

#### Step 2: Core Algorithmic Mechanics
- Implement `publish_post()` pushing to follower inboxes for users with < 25,000 followers.
- Implement pure deterministic helper functions first.

### 🛑 Stop Here Until This Works!
Run the test suite for Tier 1:
```bash
pytest project_solution/test_newsfeed_recommendation_engine.py -k "basic or initial or create or test_1" -v
```
Do not proceed to Tier 2 until all baseline data structure and creation checks pass cleanly.

---

### Phase B: Tier 2 — Core Production Project

#### Step 3: Concurrency, Error Isolation & Edge Cases
- Implement hybrid `get_feed()` pulling and merging posts from followed celebrity accounts.
- Guard against concurrent mutations and race conditions where applicable.

#### Step 4: End-to-End Orchestration
- Implement Two-Tower candidate retrieval: compute dot product of user feature vector and post embeddings.
- Connect the core engine to its secondary components and test full end-to-end operational flows.

### 🛑 Stop Here Until This Works!
Run the full automated test suite:
```bash
pytest project_solution/test_newsfeed_recommendation_engine.py -v
```
Every single test in `project_solution/test_newsfeed_recommendation_engine.py` must pass with zero failures and zero warnings.

---

### Phase C: Tier 3 — Architect Stretch Challenge

#### Step 5: High-Scale & Fault-Tolerant Extension
- Benchmark latency and memory consumption between pure push vs. pure pull vs. hybrid approach.
- Benchmark your implementation under synthetic stress or failure injections.
- Measure latency percentiles, memory footprints, and resource reclamation behavior.

---

## 3. Directory Layout

```
Module_16_Social_Media_Newsfeed_Recommendation_TwoTower/
├── 00_interactive_*.ipynb            # Interactive architectural exploration notebook
├── README.md                          # Deep-dive theory, trade-off matrices, and blueprints
├── SELF_ASSESSMENT_AND_CHALLENGES.md  # 10 diagnostic questions + 3 design challenges
├── PROJECT_GUIDE.md                   # This step-by-step implementation guide
├── TROUBLESHOOTING_AND_EDGE_CASES.md  # Real-world production failure post-mortems
├── debug_lab/                         # Intentional production defect lab & answers
│   ├── SYMPTOMS.md                    # P1 incident report & reproduction steps
│   ├── broken_newsfeed_recommendation_engine.py # Defective simulation script
│   └── ANSWERS.md                     # Root cause forensic analysis & fix
├── project_solution/                  # Complete, verified reference implementation
│   ├── newsfeed_recommendation_engine.py
│   └── test_newsfeed_recommendation_engine.py
└── starter/                           # Student boilerplate raising NotImplementedError
    ├── conftest.py
    └── newsfeed_recommendation_engine.py
```

---

## 4. You Have Mastered This Module When You Can…

Mastery is a demonstrated capability, not just passive reading. You have truly mastered this module when you can confidently check every box:

- [ ] Explain the write-amplification catastrophe of Fan-out-on-Write when applied to celebrity accounts.
- [ ] Design a hybrid Fan-out architecture that blends push-based inboxes with read-time pull aggregation.
- [ ] Implement Two-Tower neural recommendation retrieval separating candidate generation from heavy ranking.
- [ ] Size Redis timeline caches for 500M daily active users reading 20 posts per session.
- [ ] Implement feed deduplication and cursor-based pagination resistant to new post insertions.
- [ ] Design ranking models balancing recency, social graph proximity, and engagement scores.
