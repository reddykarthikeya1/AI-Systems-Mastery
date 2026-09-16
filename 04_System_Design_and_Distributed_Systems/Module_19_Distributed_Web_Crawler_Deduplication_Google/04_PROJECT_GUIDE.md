# Module_19_Distributed_Web_Crawler_Deduplication_Google: Project Implementation Guide

**Deliverable:** a production-scale distributed web crawler with URL canonicalization, `robots.txt` compliance, politeness queues, and SimHash near-duplicate detection.

---

## 🎯 3-Tier Progressive Learning Path

| Tier | For you if… | You build | Estimated Time |
| :--- | :--- | :--- | :--- |
| **Tier 1 — Novice Walkthrough** | You are learning the core concepts and basic mechanics | Implement URL normalization/canonicalization and `robots.txt` directive parsing. | ~2 hrs |
| **Tier 2 — Core Project** | Tier 1 passes completely and you want production quality | Build host-based politeness scheduling using priority queues and per-domain rate limiting. | ~3 hrs |
| **Tier 3 — Architect Stretch** | You want production-hardened, high-throughput systems | Implement 64-bit SimHash near-duplicate document detection with Hamming distance thresholding. | ~2.5 hrs |

### Setup for All Tiers

Verify your working directory and execute the test suite:
```bash
cd "System Design/Module_19_Distributed_Web_Crawler_Deduplication_Google"
pytest project_solution/test_web_crawler_frontier.py -v
```

Before writing code, verify your test environment imports the starter directory:
```bash
cd starter
pytest ../project_solution/test_web_crawler_frontier.py -v
```
All starter stubs initially raise `NotImplementedError`. Your goal is to replace each stub with a working, production-grade implementation.

---

## 1. Architectural Blueprint & Invariants

```

      Seed URLs -> [ URL Canonicalizer ] -> [ Politeness Host Queues ]
                                                    |
                                       [ Robots.txt Parser / Gatekeeper ]
                                                    |
                                      +-------------+-------------+
                                      v                           v
                              [ HTTP Fetcher ]            [ SimHash Deduper ]

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
- Implement `URLCanonicalizer.normalize()` (lowercase domain, strip fragments, sort query params).
- Ensure initialization parameters are validated against boundary conditions.

#### Step 2: Core Algorithmic Mechanics
- Implement `RobotsTxtParser` respecting `Disallow` paths and `Crawl-delay` directives.
- Implement pure deterministic helper functions first.

### 🛑 Stop Here Until This Works!
Run the test suite for Tier 1:
```bash
pytest project_solution/test_web_crawler_frontier.py -k "basic or initial or create or test_1" -v
```
Do not proceed to Tier 2 until all baseline data structure and creation checks pass cleanly.

---

### Phase B: Tier 2 — Core Production Project

#### Step 3: Concurrency, Error Isolation & Edge Cases
- Build `CrawlFrontier` managing per-host FIFO queues and a global ready min-heap.
- Guard against concurrent mutations and race conditions where applicable.

#### Step 4: End-to-End Orchestration
- Implement 64-bit `SimHash` tokenizing document text into weighted feature vectors.
- Connect the core engine to its secondary components and test full end-to-end operational flows.

### 🛑 Stop Here Until This Works!
Run the full automated test suite:
```bash
pytest project_solution/test_web_crawler_frontier.py -v
```
Every single test in `project_solution/test_web_crawler_frontier.py` must pass with zero failures and zero warnings.

---

### Phase C: Tier 3 — Architect Stretch Challenge

#### Step 5: High-Scale & Fault-Tolerant Extension
- Implement `is_duplicate(doc_a, doc_b, max_hamming_dist)` identifying near-identical web pages.
- Benchmark your implementation under synthetic stress or failure injections.
- Measure latency percentiles, memory footprints, and resource reclamation behavior.

---

## 3. Directory Layout

```
Module_19_Distributed_Web_Crawler_Deduplication_Google/
├── 00_interactive_*.ipynb            # Interactive architectural exploration notebook
├── README.md                          # Deep-dive theory, trade-off matrices, and blueprints
├── SELF_ASSESSMENT_AND_CHALLENGES.md  # 10 diagnostic questions + 3 design challenges
├── PROJECT_GUIDE.md                   # This step-by-step implementation guide
├── TROUBLESHOOTING_AND_EDGE_CASES.md  # Real-world production failure post-mortems
├── debug_lab/                         # Intentional production defect lab & answers
│   ├── SYMPTOMS.md                    # P1 incident report & reproduction steps
│   ├── broken_web_crawler_frontier.py # Defective simulation script
│   └── ANSWERS.md                     # Root cause forensic analysis & fix
├── project_solution/                  # Complete, verified reference implementation
│   ├── web_crawler_frontier.py
│   └── test_web_crawler_frontier.py
└── starter/                           # Student boilerplate raising NotImplementedError
    ├── conftest.py
    └── web_crawler_frontier.py
```

---

## 4. You Have Mastered This Module When You Can…

Mastery is a demonstrated capability, not just passive reading. You have truly mastered this module when you can confidently check every box:

- [ ] Design a crawl frontier balancing freshness, crawl depth, and strict per-host politeness delays.
- [ ] Detect and avoid spider traps (infinite calendar loops, dynamic path generation).
- [ ] Implement URL canonicalization rules to prevent crawling duplicate variants of identical endpoints.
- [ ] Use SimHash and MinHash LSH for near-duplicate document detection across billions of web pages.
- [ ] Size frontier storage and Bloom filter memory for tracking 50 billion seen URLs.
- [ ] Architect distributed worker clusters with DNS caching to avoid local DNS resolver exhaustion.
