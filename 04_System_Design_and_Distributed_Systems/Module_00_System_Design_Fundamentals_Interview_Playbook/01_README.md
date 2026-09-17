# Module 00: System Design Fundamentals & Interview Capacity Math

> **Brand new to this topic?** Start with [`00_FOUNDATIONS_PLAYGROUND.md`](00_FOUNDATIONS_PLAYGROUND.md) - the same ideas in
> plain language, with runnable standard-library code you can execute right now.
> No Docker, no server, no `pip install`.

---

## 🗺️ Recommended Step-by-Step Learning Path

Follow this exact sequence to achieve complete mastery of this module:

| Step | File to Open | What You Will Do |
| :---: | :--- | :--- |
| **1** | **[01_README.md](01_README.md)** | Read conceptual overview, architectural foundations, and mental models. |
| **2** | **[00_FOUNDATIONS_PLAYGROUND.md](00_FOUNDATIONS_PLAYGROUND.md)** | Practice beginner spoonfed micro-drills and line-by-line syntax breakdowns. |
| **3** | **[00_try_it_yourself.py](00_try_it_yourself.py)** | Run in terminal (`python 00_try_it_yourself.py`) for an interactive zero-dependency sandbox. |
| **4** | **[02_interactive_interview_and_capacity_lab.ipynb](02_interactive_interview_and_capacity_lab.ipynb)** | Open in Jupyter/VS Code to run interactive visual experiments and benchmarks. |
| **5** | **[03_interview_capacity_demo.py](03_interview_capacity_demo.py)** | Run in terminal (`python 03_interview_capacity_demo.py`) to explore 03 Interview Capacity Demo code patterns. |
| **6** | **[06_TROUBLESHOOTING_AND_EDGE_CASES.md](06_TROUBLESHOOTING_AND_EDGE_CASES.md)** | Study forensic runbooks, edge cases, and real-world failure post-mortems. |
| **7** | **[05_SELF_ASSESSMENT_AND_CHALLENGES.md](05_SELF_ASSESSMENT_AND_CHALLENGES.md)** | Test your knowledge with self-assessment quizzes, challenges, and diagnostic scenarios. |
| **8** | **[04_PROJECT_GUIDE.md](04_PROJECT_GUIDE.md)** | Follow guided project implementation for `starter/` and `project_solution/`. |
| **9** | **[problems/](problems/)** | Solve hands-on problem bank challenges and verify with `pytest problems/tests`. |
| **10** | **[debug_lab/](debug_lab/)** | Diagnose and fix silent production bugs in the Bug Hunter Drill. |

---


## 🎯 Executive Overview & Production Relevance
System design interviews and real-world architecture design fail most frequently not on esoteric distributed consensus, but on poor scoping, hand-wavy capacity math, and lack of structured communication. Navigating a 45-minute architectural session requires a deterministic framework to clarify requirements, formulate back-of-the-envelope resource bounds, and defend structural tradeoffs under pressure.

---

## 🏛️ System Architecture Blueprint
```

    +-----------------------------------------------------------------------+
    |               The 45-Minute Architectural Navigation Loop             |
    +-----------------------------------------------------------------------+
    |  00 - 05m  | Phase 1: Clarify Scope & Non-Functional Requirements     |
    |            | - Read/Write DAU, Latency SLA, Consistency, Data Lifespan |
    |  05 - 15m  | Phase 2: High-Level Architecture & API Contracts          |
    |            | - Clients -> CDN -> L7 Gateway -> Microservices -> DBs   |
    |  15 - 35m  | Phase 3: Deep-Dive Component Design & Core Invariants    |
    |            | - Partitioning, Caching, Concurrency, Sharding Strategy  |
    |  35 - 45m  | Phase 4: Bottlenecks, Failure Modes & Operational Scale   |
    |            | - SPOFs, Failover, Backpressure, Disaster Recovery Plan   |
    +-----------------------------------------------------------------------+

```

### Subsystem Anatomy & Invariants
1. **Control & Routing Tier:** Dispatches incoming operations, enforces rate limits and authentication, and routes requests to appropriate shards.
2. **Algorithmic State Machine:** Implements state transitions with deterministic mathematical guarantees and complete isolation against partial failure.
3. **Storage & Durability Tier:** Converts random mutations into structured append-only disk operations, ensuring zero data loss under abrupt process crashes.
4. **Replication & Fault Tolerance:** Detects partition failures and rebalances workloads without human intervention.

---

## 🧮 Theoretical Principles & Mathematical Models
### 1. The Power-of-10 Mental Math Rules
In live technical discussions, calculate resource boundaries in your head using exponents:
- **Seconds per Day:** 24 * 60 * 60 = 86,400 ~ 100,000 seconds (conservative underestimate).
- **QPS Conversion Rule:** 1,000,000 requests/day / 100,000 s = 10 QPS.
- **Multiplier Multiplier:** Consumer applications experience 3x to 5x diurnal peaks over daily averages.
- **Storage Multipliers:** 1 B -> 1 KB (10^3) -> 1 MB (10^6) -> 1 GB (10^9) -> 1 TB (10^12) -> 1 PB (10^15).

### 2. The 80/20 Pareto Working Set Rule
For read-heavy services, 20% of content generates 80% of read traffic. Size RAM caching tiers to hold 20% of the daily active read working set:
RAM Cache Size = Daily Active Reads * Payload Size * 0.20

### 3. Non-Functional Requirements (NFR) Triad
- **Availability vs. Consistency (CAP/PACELC):** Trade off linearizability for partition tolerance.
- **Latency SLAs (p50, p95, p99, p99.9):** Tail latency dictates high-volume user satisfaction.
- **Durability vs. Write Amplification:** Synchronous disk flush (fsync) vs. buffered append-only commit logs.

---

## ⚖️ Architectural Trade-Off Analysis Matrix

| Architectural Decision / Paradigm | Operational Trade-offs & Strengths | Recommended Production Selection |
| :--- | :--- | :--- |
| **Average QPS vs Peak QPS Provisioning** | Sizing for average saves cloud spend; sizing for peak prevents brownouts. | Provision for 3x-5x peak traffic with auto-scaling groups and aggressive queue shedding. |
| **Single Multi-Purpose DB vs Polyglot Persistence** | Single DB simplifies ops; Polyglot fits storage engine to data access pattern. | Use Polyglot persistence when scale exceeds 10k QPS (e.g. Postgres metadata + Redis cache + S3 media). |
| **Client-Side Polling vs Persistent WebSockets** | HTTP polling is stateless; WebSockets provide sub-millisecond bidirectional push. | Use HTTP for read-heavy request/response; WebSockets for real-time chat and presence. |
| **Synchronous REST vs Asynchronous Event Streaming** | Sync is easy to reason about; Async decouples downstream failures. | Use sync for user-facing reads; async event logs for non-blocking side effects and writes. |

---

## 🚨 Critical Production Failure Modes & Runbooks

| Failure Scenario & Symptom | Forensic Root Cause | SRE Hardening & Invariant Fix |
| :--- | :--- | :--- |
| **Neglecting Replication Storage Factor** | Computing raw disk usage without multiplying by 3x replication factor causes disk exhaustion in month 2. | Always multiply storage by Replication Factor / (1 - HeadroomMargin). |
| **Unit Confusion (GB vs GiB)** | Dividing bytes by 10^6 instead of 1024^3 creates 7.3% error per gigabyte, snowballing at petabyte scale. | Formulate equations in binary GiB (2^30) or decimal GB (10^9) consistently. |
| **Omitting Network Egress Costs** | Failing to estimate outbound video/image egress leads to catastrophic cloud bandwidth overages. | Separate egress bandwidth from inbound ingress. |
| **Thundering Herd on Morning Wakeup** | Global users all loading app at 08:00 AM local time creates localized 10x traffic spikes. | Implement client-side jitter and edge caching with stale-while-revalidate headers. |

---

## 📊 SRE Telemetry, SLIs & Alerting Runbooks

| Production SLI Metric | Healthy Target | P1 Alert Threshold | Immediate Automated & Manual Mitigation |
| :--- | :--- | :--- | :--- |
| **p99 Request Latency** | < 25 ms | > 150 ms for 2 min | Shed non-essential background traffic; trigger horizontal container scaling. |
| **Error Rate (HTTP 5xx / RPC)**| < 0.01% | > 1.0% for 1 min | Trip circuit breaker to fallback route; verify database connection pool headroom. |
| **Worker Queue Depth** | < 50 items | > 5,000 items | Reject unauthenticated writes with HTTP 429; provision additional consumer workers. |
| **Storage / Memory Utilization**| < 70% capacity | > 85% capacity | Trigger WAL segment compaction; evict expired LRU cache partitions. |

---

## 📋 Whiteboard Interview & Staff Defense Checklist

When presenting this architectural module in a Staff/Principal interview, ensure you defend:
- [ ] **Capacity Math:** Back-of-the-envelope calculations for peak QPS, ingress/egress bandwidth, and multi-year storage retention.
- [ ] **Boundary Separation:** Clear demarcation between Ingress (Edge), Application Services, and Storage/Cache tiers.
- [ ] **Data Model Rigor:** Partition keys, primary keys, sharding schemes, and access-pattern justifications.
- [ ] **Fault Tolerance:** Explicit failover protocols for power loss, network partition, and storage corruption.
- [ ] **Trade-Off Articulation:** Ability to clearly explain why this design was chosen over viable alternatives.

---

## 🛠️ Hands-on Engineering, TDD & Verification

This module includes a dual-track learning setup: an in-process architectural simulation model in `project_solution/` and an interactive student TDD template in `starter/`.

### 1. Run the Interactive Exploration Notebook
Explore the interactive architectural lab in VS Code or Jupyter:
```bash
jupyter notebook 00_interactive_interview_and_capacity_lab.ipynb
```

### 2. Execute the Standalone Demo Script
Observe the components interacting under simulated workload:
```bash
python 01_interview_capacity_demo.py
```

### 3. Run the Automated Pytest Verification Suite
Verify reference implementation invariants:
```bash
pytest project_solution/ -v
```

To test your own implementation in `starter/`:
```bash
cd starter
pytest ../project_solution/ -v
```

---

## 📂 Pedagogical Scaffolding & Directory Tour

Each component in this module fulfills a specific role in your engineering progression:

| File / Directory | Purpose & Recommended Usage |
| :--- | :--- |
| **[`00_interactive_*.ipynb`](02_interactive_interview_and_capacity_lab.ipynb)** | Interactive hands-on simulation notebook with runnable visualization cells. |
| **[`03_interview_capacity_demo.py`](03_interview_capacity_demo.py)** | Standalone Python executable demonstrating core mechanics and latency profiles. |
| **[`04_PROJECT_GUIDE.md`](04_PROJECT_GUIDE.md)** | Step-by-step implementation guide featuring **3 progressive difficulty tiers** (Tier 1: Novice, Tier 2: Core, Tier 3: Architect). |
| **[`06_TROUBLESHOOTING_AND_EDGE_CASES.md`](06_TROUBLESHOOTING_AND_EDGE_CASES.md)** | Deep-dive guide into production bugs, concurrency races, and operational post-mortems. |
| **[`debug_lab/`](debug_lab/SYMPTOMS.md)** | Dedicated incident lab featuring defective implementation (`broken_*.py`), symptom telemetry, and forensic solutions. |
| **[`05_SELF_ASSESSMENT_AND_CHALLENGES.md`](05_SELF_ASSESSMENT_AND_CHALLENGES.md)** | 10 diagnostic interview questions with deep explanations plus 2–3 machine-coding design challenges. |
| **[`project_solution/interview_capacity_calculator.py`](project_solution/interview_capacity_calculator.py)** | Verified, complete in-process architectural simulation reference model. |
| **[`starter/interview_capacity_calculator.py`](starter/interview_capacity_calculator.py)** | Student boilerplate raising `NotImplementedError` for TDD mastery. |

---

## 🧭 Curriculum Graph Navigation

Connect this module to the broader distributed systems curriculum:

### ⬅️ Prerequisites
- *None (Foundational Entrypoint)*

### ➡️ Next Steps
- [Next Module: Module 01 Physics of Scalability Capacity Math](../Module_01_Physics_of_Scalability_Capacity_Math/01_README.md)

### 🏁 Phase Benchmark & Core Frameworks
- **[Relevant Phase Benchmark Checkpoint](../Phase_Checkpoints/PHASE_1_CHECKPOINT.md)**
- **[Master Syllabus](../MASTER_SYLLABUS.md)**
- **[System Design Frameworks & Cheatsheet](../SYSTEM_DESIGN_FRAMEWORKS_AND_CHEATSHEET.md)**
- **[Global Debugging Playbook](../GLOBAL_DEBUGGING_PLAYBOOK.md)**
- **[Study Plans & Pacing Guide](../STUDY_PLANS_AND_PACING_GUIDE.md)**
