# Module_03_Edge_Infrastructure_Reverse_Proxies: Project Implementation Guide

**Deliverable:** an asynchronous Layer 7 API Gateway with route prefix dispatching, token-bucket rate limiting, and upstream connection health checks.

---

## 🎯 3-Tier Progressive Learning Path

| Tier | For you if… | You build | Estimated Time |
| :--- | :--- | :--- | :--- |
| **Tier 1 — Novice Walkthrough** | You are learning the core concepts and basic mechanics | Implement URI prefix-based route dispatching and request/response header sanitization. | ~2 hrs |
| **Tier 2 — Core Project** | Tier 1 passes completely and you want production quality | Build distributed token-bucket rate limiting per client IP/API key, circuit breakers, and connection timeouts. | ~3 hrs |
| **Tier 3 — Architect Stretch** | You want production-hardened, high-throughput systems | Implement dynamic backend service registration, TLS termination simulation, and stale-while-revalidate edge caching. | ~2.5 hrs |

### Setup for All Tiers

Verify your working directory and execute the test suite:
```bash
cd "System Design/Module_03_Edge_Infrastructure_Reverse_Proxies"
pytest project_solution/test_api_gateway_proxy.py -v
```

Before writing code, verify your test environment imports the starter directory:
```bash
cd starter
pytest ../project_solution/test_api_gateway_proxy.py -v
```
All starter stubs initially raise `NotImplementedError`. Your goal is to replace each stub with a working, production-grade implementation.

---

## 1. Architectural Blueprint & Invariants

```

      Client Request -> [ Edge / Reverse Proxy / API Gateway ]
                                    |
                    +---------------+---------------+
                    | Rate Limiter  | Path Router   |
                    | Token Bucket  | Upstream Pool |
                    +---------------+---------------+
                                    |
                    +---------------+---------------+
                    v                               v
           [Auth Service :8081]            [Order Service :8082]

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
- Create `UpstreamServer` with state tracking (healthy, unhealthy, active connections).
- Ensure initialization parameters are validated against boundary conditions.

#### Step 2: Core Algorithmic Mechanics
- Implement `TokenBucketRateLimiter` supporting burst capacity and constant refill rate.
- Implement pure deterministic helper functions first.

### 🛑 Stop Here Until This Works!
Run the test suite for Tier 1:
```bash
pytest project_solution/test_api_gateway_proxy.py -k "basic or initial or create or test_1" -v
```
Do not proceed to Tier 2 until all baseline data structure and creation checks pass cleanly.

---

### Phase B: Tier 2 — Core Production Project

#### Step 3: Concurrency, Error Isolation & Edge Cases
- Build `ServiceCluster` with round-robin dispatch among healthy upstreams.
- Guard against concurrent mutations and race conditions where applicable.

#### Step 4: End-to-End Orchestration
- Construct `APIGateway` orchestrating authentication, rate limiting, routing, and error responses.
- Connect the core engine to its secondary components and test full end-to-end operational flows.

### 🛑 Stop Here Until This Works!
Run the full automated test suite:
```bash
pytest project_solution/test_api_gateway_proxy.py -v
```
Every single test in `project_solution/test_api_gateway_proxy.py` must pass with zero failures and zero warnings.

---

### Phase C: Tier 3 — Architect Stretch Challenge

#### Step 5: High-Scale & Fault-Tolerant Extension
- Implement passive and active health check probes that evict failing upstream nodes.
- Benchmark your implementation under synthetic stress or failure injections.
- Measure latency percentiles, memory footprints, and resource reclamation behavior.

---

## 3. Directory Layout

```
Module_03_Edge_Infrastructure_Reverse_Proxies/
├── 00_interactive_*.ipynb            # Interactive architectural exploration notebook
├── README.md                          # Deep-dive theory, trade-off matrices, and blueprints
├── SELF_ASSESSMENT_AND_CHALLENGES.md  # 10 diagnostic questions + 3 design challenges
├── PROJECT_GUIDE.md                   # This step-by-step implementation guide
├── TROUBLESHOOTING_AND_EDGE_CASES.md  # Real-world production failure post-mortems
├── debug_lab/                         # Intentional production defect lab & answers
│   ├── SYMPTOMS.md                    # P1 incident report & reproduction steps
│   ├── broken_api_gateway_proxy.py # Defective simulation script
│   └── ANSWERS.md                     # Root cause forensic analysis & fix
├── project_solution/                  # Complete, verified reference implementation
│   ├── api_gateway_proxy.py
│   └── test_api_gateway_proxy.py
└── starter/                           # Student boilerplate raising NotImplementedError
    ├── conftest.py
    └── api_gateway_proxy.py
```

---

## 4. You Have Mastered This Module When You Can…

Mastery is a demonstrated capability, not just passive reading. You have truly mastered this module when you can confidently check every box:

- [ ] Differentiate Forward Proxy, Reverse Proxy, Edge Router, and API Gateway responsibilities.
- [ ] Implement token-bucket and leaky-bucket algorithms with millisecond refill precision.
- [ ] Explain how SSL/TLS termination at edge offloads compute from internal microservices.
- [ ] Configure Layer 7 path-based, header-based, and query-param routing policies.
- [ ] Mitigate DDoS attacks at edge using SYN cookies, IP reputation, and volumetric rate limiting.
- [ ] Explain the operational mechanics of Anycast DNS and CDN edge POP point-of-presence routing.
