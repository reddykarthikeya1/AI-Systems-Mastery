# Module_14_Distributed_URL_Shortener_TinyURL: Project Implementation Guide

**Deliverable:** a production-scale TinyURL service with Base62 bijective encoding, offline Key Generation Service (KGS), and TTL expiration.

---

## 🎯 3-Tier Progressive Learning Path

| Tier | For you if… | You build | Estimated Time |
| :--- | :--- | :--- | :--- |
| **Tier 1 — Novice Walkthrough** | You are learning the core concepts and basic mechanics | Implement Base62 bijective encoding and decoding (`[0-9a-zA-Z]`) mapping 64-bit integers to short strings. | ~2 hrs |
| **Tier 2 — Core Project** | Tier 1 passes completely and you want production quality | Build `KeyGenerationService` pre-allocating collision-free key batches to worker nodes. | ~3 hrs |
| **Tier 3 — Architect Stretch** | You want production-hardened, high-throughput systems | Implement end-to-end URL shortener service with TTL expiration, LRU cache-aside, and 301 vs 302 redirect analytics. | ~2.5 hrs |

### Setup for All Tiers

Verify your working directory and execute the test suite:
```bash
cd "System Design/Module_14_Distributed_URL_Shortener_TinyURL"
pytest project_solution/test_url_shortener_service.py -v
```

Before writing code, verify your test environment imports the starter directory:
```bash
cd starter
pytest ../project_solution/test_url_shortener_service.py -v
```
All starter stubs initially raise `NotImplementedError`. Your goal is to replace each stub with a working, production-grade implementation.

---

## 1. Architectural Blueprint & Invariants

```

      Long URL -> [ Key Generation Service (KGS) ] -> Short URL: 'https://tiny.url/x7K2p'
                                    |
                    +---------------+---------------+
                    v                               v
          [ In-Memory Read Cache ]        [ Distributed DB Store ]
          (High read-to-write 100:1)      (ID, ShortKey, LongUrl, TTL)

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
- Implement `Base62Encoder.encode(integer)` and `Base62Encoder.decode(string)` with round-trip symmetry.
- Ensure initialization parameters are validated against boundary conditions.

#### Step 2: Core Algorithmic Mechanics
- Build `KeyGenerationService` dispensing unique sequential or pre-generated keys.
- Implement pure deterministic helper functions first.

### 🛑 Stop Here Until This Works!
Run the test suite for Tier 1:
```bash
pytest project_solution/test_url_shortener_service.py -k "basic or initial or create or test_1" -v
```
Do not proceed to Tier 2 until all baseline data structure and creation checks pass cleanly.

---

### Phase B: Tier 2 — Core Production Project

#### Step 3: Concurrency, Error Isolation & Edge Cases
- Implement `shorten_url(long_url, custom_alias, ttl_seconds)` storing metadata.
- Guard against concurrent mutations and race conditions where applicable.

#### Step 4: End-to-End Orchestration
- Implement `resolve_url(short_key)` with cache-aside lookup and 404/expired handling.
- Connect the core engine to its secondary components and test full end-to-end operational flows.

### 🛑 Stop Here Until This Works!
Run the full automated test suite:
```bash
pytest project_solution/test_url_shortener_service.py -v
```
Every single test in `project_solution/test_url_shortener_service.py` must pass with zero failures and zero warnings.

---

### Phase C: Tier 3 — Architect Stretch Challenge

#### Step 5: High-Scale & Fault-Tolerant Extension
- Analyze HTTP 301 Permanent Redirect (browser caches, saves server load) vs. 302 Found (server tracks click analytics).
- Benchmark your implementation under synthetic stress or failure injections.
- Measure latency percentiles, memory footprints, and resource reclamation behavior.

---

## 3. Directory Layout

```
Module_14_Distributed_URL_Shortener_TinyURL/
├── 00_interactive_*.ipynb            # Interactive architectural exploration notebook
├── README.md                          # Deep-dive theory, trade-off matrices, and blueprints
├── SELF_ASSESSMENT_AND_CHALLENGES.md  # 10 diagnostic questions + 3 design challenges
├── PROJECT_GUIDE.md                   # This step-by-step implementation guide
├── TROUBLESHOOTING_AND_EDGE_CASES.md  # Real-world production failure post-mortems
├── debug_lab/                         # Intentional production defect lab & answers
│   ├── SYMPTOMS.md                    # P1 incident report & reproduction steps
│   ├── broken_url_shortener_service.py # Defective simulation script
│   └── ANSWERS.md                     # Root cause forensic analysis & fix
├── project_solution/                  # Complete, verified reference implementation
│   ├── url_shortener_service.py
│   └── test_url_shortener_service.py
└── starter/                           # Student boilerplate raising NotImplementedError
    ├── conftest.py
    └── url_shortener_service.py
```

---

## 4. You Have Mastered This Module When You Can…

Mastery is a demonstrated capability, not just passive reading. You have truly mastered this module when you can confidently check every box:

- [ ] Design a 100:1 read-heavy system architecture capable of serving billions of redirects.
- [ ] Explain why MD5/SHA256 truncation leads to hash collisions and why Base62 counter encoding is superior.
- [ ] Design an offline Key Generation Service (KGS) that dispenses pre-computed tokens to web servers.
- [ ] Differentiate HTTP 301 (Permanent) vs. HTTP 302 (Temporary) redirect semantics in search engine ranking and analytics.
- [ ] Calculate 5-year storage requirements for 500 million new URLs per month.
- [ ] Implement TTL expiration cleanup using lazy deletion combined with background sweepers.
