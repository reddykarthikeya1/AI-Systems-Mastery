# Module_26_Final_Capstone_Project: Project Implementation Guide

**Deliverable:** the master capstone platform unifying FastAPI, SQLAlchemy 2.0, JWT RBAC, task queues, Polars analytics, and Prometheus telemetry.

---

## 🎯 3-Tier Progressive Learning Path

| Tier | For you if… | You build | Time |
| :--- | :--- | :--- | :--- |
| **Tier 1 — Novice Walkthrough** | You are learning the core mechanics | Basic working prototype passing fundamental unit tests | ~2 hrs |
| **Tier 2 — Core Project** | Tier 1 passes completely | Production-ready implementation with validation, error isolation, and edge cases | ~3 hrs |
| **Tier 3 — Architect Stretch** | You want production-hardened systems | High-throughput, distributed, or benchmarked extension | ~2.5 hrs |

### Setup for All Tiers

```bash
cd starter && pytest ../project_solution/test_capstone.py -v
```

Before writing code, verify your test environment imports the starter directory. All stubs initially raise `NotImplementedError`.

---

## Tier 1 — Novice Walkthrough

### Step 1 — API Gateway & Models
Implement `UserModel` and `ProjectModel` with SQLAlchemy 2.0 async mapping and FastAPI endpoints.

### Step 2 — Auth Subsystem
Implement user registration with Bcrypt hashing and JWT token issuance with role claims.

### 🛑 Stop Here Until This Works!
Run the test suite for Tier 1:
```bash
pytest ../project_solution/test_capstone.py -k "basic or initial or health or create or single" -v
```
Do not proceed to Tier 2 until your initial implementation compiles and passes all Tier 1 checks.

---

## Tier 2 — Core Project: Complete Turnkey Implementation

### Step 3 — Background Task Broker & DLQ
Implement `CapstoneTaskBroker` with retry tracking and Dead Letter Queue fallback.

### Step 4 — Polars & DuckDB Analytics
Implement `CapstoneAnalytics` aggregating owner project budgets and ranking projects with DuckDB window SQL.

### 💥 Deliberately Break It (Do this — it is the lesson!)
In `starter/tasks.py`, remove the Dead Letter Queue transition so failing tasks remain in the active queue forever.
Run:
```bash
pytest ../capstone_platform/test_capstone.py -k test_task_broker_retries_and_dlq -v
```
Watch the test fail when DLQ is empty, then restore DLQ routing.

### ✅ Tier 2 Acceptance
Run the full test suite:
```bash
pytest ../project_solution/test_capstone.py -v
```
All tests must pass cleanly.

---

## Tier 3 — Architect Stretch: Advanced Production Challenges

1. **Distributed Tracing Header Propagation:** Pass W3C traceparent headers across HTTP and background tasks.
2. **Prometheus Alerting Rules:** Define Alertmanager rules triggering alerts when task DLQ rate exceeds 1%.
3. **Database Read/Write Splitting:** Route analytics queries to read replicas and transactions to primary.
4. **Full Automated Load Test:** Run Locust load test asserting 1,000 req/sec under 50ms p99 latency.

---

## 📊 Grading Matrix

| Test | Proves |
| :--- | :--- |
| `test_auth_hash_and_verify_password` | Proves password hashing and constant-time verification |
| `test_task_broker_retries_and_dlq` | Proves failing tasks retry and transition to Dead Letter Queue |
| `test_analytics_aggregate_project_budgets` | Proves Polars lazy aggregation groups budgets accurately |
| `test_full_auth_and_project_creation_workflow` | Proves end-to-end user registration, login, and project creation |
| `test_telemetry_correlation_id_propagation` | Proves X-Correlation-ID flows from request to response |

---

## 🎓 You have mastered this module when you can…

- [ ] Architect and build multi-tier cloud-native Python platforms from scratch
- [ ] Synthesize async web APIs, relational databases, and background task queues
- [ ] Enforce enterprise security standards (Bcrypt, JWT, RBAC, input sanitization)
- [ ] Process analytical queries on large datasets using Polars and DuckDB
- [ ] Instrument distributed systems with correlation IDs and Prometheus observability
- [ ] Write end-to-end integration test suites asserting system invariants across subsystems
- [ ] Diagnose and remediate complex architectural bottlenecks in production codebases
