# Module_12_Probabilistic_Data_Structures: Project Implementation Guide

**Deliverable:** memory-efficient probabilistic algorithms: Bloom Filter, Count-Min Sketch frequency tracker, and HyperLogLog cardinality estimator.

---

## 🎯 3-Tier Progressive Learning Path

| Tier | For you if… | You build | Estimated Time |
| :--- | :--- | :--- | :--- |
| **Tier 1 — Novice Walkthrough** | You are learning the core concepts and basic mechanics | Implement a space-efficient Bloom Filter using bitarray and multiple Murmur3/SHA256 hash seeds. | ~2 hrs |
| **Tier 2 — Core Project** | Tier 1 passes completely and you want production quality | Build a 2D Count-Min Sketch estimating item frequencies with mathematical error guarantees. | ~3 hrs |
| **Tier 3 — Architect Stretch** | You want production-hardened, high-throughput systems | Implement HyperLogLog with register buckets, leading-zero bit counting, and harmonic mean estimation. | ~2.5 hrs |

### Setup for All Tiers

Verify your working directory and execute the test suite:
```bash
cd "System Design/Module_12_Probabilistic_Data_Structures"
pytest project_solution/test_probabilistic_structures.py -v
```

Before writing code, verify your test environment imports the starter directory:
```bash
cd starter
pytest ../project_solution/test_probabilistic_structures.py -v
```
All starter stubs initially raise `NotImplementedError`. Your goal is to replace each stub with a working, production-grade implementation.

---

## 1. Architectural Blueprint & Invariants

```

     [Bloom Filter]       -> Membership test: 0 False Negatives, tunable False Positives
     [Count-Min Sketch]   -> Frequency tracking: Never underestimates, bounded overestimation
     [HyperLogLog]        -> Cardinality estimation: 1.04/sqrt(m) standard error in 1.5 KB

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
- Implement `BloomFilter(capacity, false_positive_rate)` calculating optimal bit array size m and hash count k.
- Ensure initialization parameters are validated against boundary conditions.

#### Step 2: Core Algorithmic Mechanics
- Implement `add()` and `__contains__()` in Bloom Filter; verify zero false negatives.
- Implement pure deterministic helper functions first.

### 🛑 Stop Here Until This Works!
Run the test suite for Tier 1:
```bash
pytest project_solution/test_probabilistic_structures.py -k "basic or initial or create or test_1" -v
```
Do not proceed to Tier 2 until all baseline data structure and creation checks pass cleanly.

---

### Phase B: Tier 2 — Core Production Project

#### Step 3: Concurrency, Error Isolation & Edge Cases
- Build `CountMinSketch(width, depth)` with pointwise min query over d hash rows.
- Guard against concurrent mutations and race conditions where applicable.

#### Step 4: End-to-End Orchestration
- Implement `HyperLogLog(precision)` hashing items into 2^p buckets and tracking max leading zeros.
- Connect the core engine to its secondary components and test full end-to-end operational flows.

### 🛑 Stop Here Until This Works!
Run the full automated test suite:
```bash
pytest project_solution/test_probabilistic_structures.py -v
```
Every single test in `project_solution/test_probabilistic_structures.py` must pass with zero failures and zero warnings.

---

### Phase C: Tier 3 — Architect Stretch Challenge

#### Step 5: High-Scale & Fault-Tolerant Extension
- Benchmark memory consumption of 1,000,000 items in HyperLogLog (1.5 KB) vs. a Python set (32 MB).
- Benchmark your implementation under synthetic stress or failure injections.
- Measure latency percentiles, memory footprints, and resource reclamation behavior.

---

## 3. Directory Layout

```
Module_12_Probabilistic_Data_Structures/
├── 00_interactive_*.ipynb            # Interactive architectural exploration notebook
├── README.md                          # Deep-dive theory, trade-off matrices, and blueprints
├── SELF_ASSESSMENT_AND_CHALLENGES.md  # 10 diagnostic questions + 3 design challenges
├── PROJECT_GUIDE.md                   # This step-by-step implementation guide
├── TROUBLESHOOTING_AND_EDGE_CASES.md  # Real-world production failure post-mortems
├── debug_lab/                         # Intentional production defect lab & answers
│   ├── SYMPTOMS.md                    # P1 incident report & reproduction steps
│   ├── broken_probabilistic_structures.py # Defective simulation script
│   └── ANSWERS.md                     # Root cause forensic analysis & fix
├── project_solution/                  # Complete, verified reference implementation
│   ├── probabilistic_structures.py
│   └── test_probabilistic_structures.py
└── starter/                           # Student boilerplate raising NotImplementedError
    ├── conftest.py
    └── probabilistic_structures.py
```

---

## 4. You Have Mastered This Module When You Can…

Mastery is a demonstrated capability, not just passive reading. You have truly mastered this module when you can confidently check every box:

- [ ] Derive optimal Bloom filter bit size m and hash count k from capacity and target error rate.
- [ ] Prove why Bloom Filters guarantee zero false negatives but have bounded false positives.
- [ ] Use Count-Min Sketch for real-time trending topics and DDoS attack detection.
- [ ] Explain how HyperLogLog uses register bucket hashing and harmonic means to estimate cardinality.
- [ ] Select the appropriate probabilistic data structure for web crawling, caching, and analytics.
- [ ] Serialize and merge distributed HyperLogLog registers across multiple worker nodes.
