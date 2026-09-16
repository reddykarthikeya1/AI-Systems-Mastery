# Phase Checkpoint: Foundations, Capacity Physics & Edge Ingress Infrastructure

> **Phase Scope:** Modules 00–04 (Fundamentals Playbook, Capacity Math, Protocols, Reverse Proxies, Load Balancing)  
> **Allocated Exam Duration:** 90 Minutes  
> **Evaluation Mode:** Closed-solution, timed architectural defense, capacity math drill, and code audit.

---

## 🎯 The Exam Mission: Architect a Global Edge Ingress & Layer 7 Routing Fabric for an International Streaming Service

### Executive Scenario
You are the Principal Infrastructure Architect at a global streaming company (similar to Netflix/YouTube). 
The platform serves 50,000,000 Daily Active Users across 4 global regions (North America, Europe, Asia-Pacific, Latin America).
Traffic is heavily bursty: during major live events (sports finals, global keynotes), peak traffic surges to 4.5x normal volume within 3 minutes.
Your objective is to design the complete edge ingress layer—from DNS resolution to edge POPs, TLS termination, WAF/rate-limiting, Layer 7 path routing, and load-balanced microservice clusters.

---

## 🏛️ Reference Architectural Blueprint (C4 Container View)

```

                       [ Global Clients (Mobile, Web, Smart TV) ]
                                            |
                         BGP Anycast DNS + Geo-Routing
                                            v
               +---------------------------------------------------------+
               |            Edge Point of Presence (POP)                 |
               |                                                         |
               |  +-------------------+        +----------------------+  |
               |  | Layer 4 ECMP LVS  | -----> | Layer 7 Envoy Proxy  |  |
               |  | (BGP Anycast IP)  |        | (TLS Termination)    |  |
               |  +-------------------+        +----------------------+  |
               |                                           |             |
               |       +-----------------------------------+             |
               |       v                                   v             |
               | [ Token Bucket WAF ]            [ Edge POP Cache ]      |
               | (DDoS Mitigation)               (HTTP Stale-While-Reval)|
               +---------------------------------------------------------+
                                            |
                              Encrypted Backbone (mTLS)
                                            v
               +---------------------------------------------------------+
               |                 Origin Datacenter Mesh                  |
               |                                                         |
               |  [ Internal HAProxy / Service Mesh Ingress Router ]     |
               |         |                        |                      |
               |         v                        v                      |
               |   [ Auth Cluster ]         [ Video Metadata ]           |
               |   (gRPC / HTTP/2)          (gRPC / HTTP/2)              |
               +---------------------------------------------------------+

```

---

## 📋 Hard Engineering & Scale Specifications

### 1. Functional Requirements
- **Anycast Ingress Routing:** Route client connections to the nearest Point of Presence (POP) via BGP Anycast.
- **Protocol Flexibility:** Support HTTP/3 (QUIC) for high-packet-loss mobile clients, HTTP/2 for modern browsers, and gRPC for internal microservice RPCs.
- **Layer 7 Path & Header Dispatch:** Dispatch `/api/v1/auth/*` to Auth Cluster, `/api/v1/video/*` to Streaming Cluster, and `/api/v1/user/*` to Profile Cluster.
- **Edge Rate Limiting:** Enforce dynamic Token Bucket rate limits per IP and per API key, dropping DDoS surges at the boundary.

### 2. Non-Functional & Scale Metrics
- **Peak Throughput:** 250,000 Peak QPS across 4 global edge POPs.
- **Latency SLA:** Edge TLS handshake < 25ms; Layer 7 proxy routing overhead < 2ms (p99).
- **Availability:** 99.999% ('Five Nines') uptime; edge POP failure must trigger BGP withdrawal and automatic traffic failover in < 3 seconds.
- **Security:** Zero plain-text internal traffic; mutual TLS (mTLS) between reverse proxy and upstream service meshes.

---

## 🧮 Quantitative Physics & Mathematical Formulations

### Quantitative Capacity & Resource Math Drill
1. **Average QPS:** $50,000,000 \text{ DAU} \times 40 \text{ requests/day} / 86,400 \approx 23,148 \text{ QPS}$.
2. **Peak QPS (4.5x Surge):** $23,148 \times 4.5 \approx 104,166 \text{ QPS}$ (provision for $120,000 \text{ QPS}$ with 15% headroom).
3. **Ingress Bandwidth:** $120,000 \text{ QPS} \times 1.2 \text{ KB/req} = 144 \text{ MB/s} = 1.152 \text{ Gbps}$.
4. **Egress Bandwidth:** $120,000 \text{ QPS} \times 15 \text{ KB/resp} = 1.8 \text{ GB/s} = 14.4 \text{ Gbps}$.
5. **Worker Thread Pool Size (Little's Law):** At $25,000 \text{ QPS}$ per POP with mean proxy latency of $4 \text{ ms}$ ($0.004 \text{ s}$):
   $$L = \lambda \times W = 25,000 \times 0.004 = 100 \text{ concurrent active connections per server}.$$
6. **Edge RAM Cache Sizing:** Sizing for 20% of daily active media metadata working set ($500 \text{ GB} \times 0.20 = 100 \text{ GB RAM}$) distributed across edge proxy nodes.

---

### 💥 Production Chaos Injection Scenarios
1. **Transatlantic Fiber Cut:** A submarine cable severing North America from Europe doubles WAN latency from 75ms to 280ms. The ingress architecture must reroute DNS Anycast routes within 15 seconds without dropping active sessions.
2. **Upstream Service Brownout (Cascading Flapping):** The Auth Service latency spikes from 5ms to 1200ms. The Layer 7 reverse proxy must trip its Circuit Breaker to `OPEN`, serving cached stale profile tokens rather than exhausting reverse proxy connection pools.
3. **DDoS SYN Flood Surge:** 5,000,000 forged SYN packets/sec strike the ingress IP. Layer 4 routers must activate SYN Cookies and drop non-whitelisted flows in hardware without increasing L7 CPU utilization.

---

## 📊 100-Point Comprehensive Grading Rubric

| Dimension | Evaluation Criteria | Maximum Points |
| :--- | :--- | :---: |
| **Capacity & Hardware Math** | Precise QPS derivation, Little's Law thread sizing, ingress/egress bandwidth calculation, and 80/20 cache sizing | 20 pts |
| **Transport & Protocols** | Defensible selection of HTTP/3 QUIC vs. HTTP/2 TCP vs. gRPC, solving Head-of-Line blocking | 20 pts |
| **Reverse Proxy Topology** | Multi-tier edge architecture (Anycast BGP -> L4 ECMP -> L7 Envoy/Nginx) with mTLS termination | 20 pts |
| **Load Balancing Mechanics** | Smooth Weighted Round-Robin / Least-Connections implementation with flapping prevention | 20 pts |
| **DDoS & Failure Modes** | Token Bucket rate limiting, circuit breaker cascading prevention, and connection draining | 20 pts |

**Passing Gate Threshold:** **85 / 100 Points** is required to officially certify and unlock the next phase.

---

## 🎙️ Diagnostic Oral Defense Questions (Staff-Level Panel)

Prepare to answer and defend these exact questions on a whiteboard during the review panel:

1. **Why does HTTP/2 multiplexing suffer worse tail latency than HTTP/1.1 over lossy 3% packet-drop cellular networks?**
2. **How does Smooth Weighted Round-Robin (Nginx algorithm) prevent the burst starvation caused by naive modulo-based weighted selection?**
3. **What happens to existing in-flight TCP connections when an Anycast BGP router shifts traffic to a new POP during an ISP routing flap?**
4. **Explain the exact difference between Layer 4 Direct Server Return (DSR) and Layer 7 proxying in terms of return packet path.**
5. **How would you size the rate limiter token bucket burst capacity to tolerate legitimate mobile app resume storms without allowing DDoS attacks?**

---

## 🚦 Pre-Flight Submission & Quality Checklist

Before submitting your phase architecture for certification, verify:
- [ ] All quantitative capacity math equations use explicit powers of 10 and real-world hardware latencies.
- [ ] API endpoints specify HTTP verbs, status codes, request bodies, and idempotency headers.
- [ ] Data models define primary keys, partition keys, sharding strategies, and secondary indexes.
- [ ] No single point of failure (SPOF) exists in either the control plane or the data path.
- [ ] Failure modes (split-brain, clock skew, thundering herds, cascading timeouts) have explicit mitigations.
- [ ] All starter exercises and unit tests in this phase pass with a 100% success rate (`pytest`).


---

## 🚦 Pre-Flight Gate: Verify Before You Start

**Do not start until all of this is green.** Sitting a timed exam on a broken
checkout means spending the clock on setup instead of on architecture.

```bash
# From the course root.
pytest Module_00_System_Design_Fundamentals_Interview_Playbook \n      Module_01_Physics_of_Scalability_Capacity_Math \n      Module_02_Network_Protocols_Transport_API_Paradigms \n      Module_03_Edge_Infrastructure_Reverse_Proxies \n      Module_04_Load_Balancing_Algorithms_Health_Probes       -q

python tools/check_links.py --quiet
ruff check .
```

---

## 📏 Exam Rules

| Rule | Detail |
| :--- | :--- |
| **Time box** | Set a timer for the duration above. When it ends, stop and score what exists. |
| **No solution exists** | There is deliberately no reference answer for this exam. The rubric *is* the specification. |
| **Modules are open-book** | Re-read any README, notebook or troubleshooting guide. That is what the job looks like. |
| **`project_solution/` is closed-book** | Do not open the module solutions during the exam. Copying them measures nothing. |
| **Numbers or it did not happen** | Every capacity claim needs arithmetic you can show. "It scales" scores zero. |
| **Name your tradeoffs** | A design with no stated downside is an unexamined design, and the rubric penalises it. |

---

## 🔬 Self-Verification Harness

Produce this evidence before scoring yourself. The rubric grades **evidence**,
not intent.

```bash
# 1. Your design's code runs at all
python -m your_design               # must not traceback

# 2. Your own tests pass
pytest your_tests.py -v             # paste the summary line

# 3. It is clean
ruff check .

# 4. Your capacity numbers are reproducible
python your_capacity_math.py        # prints QPS, bandwidth, storage, cache size
```

A design document with no runnable artefact caps at the analysis criteria only.

---

## ⏱️ If You Run Out of Time

1. **Submit the working subset.** Comment out anything that does not run - a
   broken import forfeits every point in the file.
2. **Write down what is missing**, one line per requirement. Naming your own gap
   accurately is a senior skill and earns analysis credit.
3. **Keep your numbers.** Capacity math for the parts you finished outscores
   hand-waving about the parts you did not.

---

## 🔁 If You Score Below the Threshold

1. Identify the **rubric row** you lost the most points on.
2. Re-read: **Module 01's capacity formulas and Module 04's balancing algorithms**.
3. Work that module's `debug_lab/` - it drills the exact failure modes this
   exam punishes.
4. Re-take with the numbers changed (different DAU, different payload size) so
   you are re-deriving rather than recalling.

Re-taking a checkpoint is normal. Advancing past one you failed is not, because
every later phase assumes this one.

---

## 🎓 What This Checkpoint Measures

The modules in scope taught you a set of techniques. This exam tests
**whether you can put defensible numbers on a system before drawing a single box**.

That is deliberately different from the module quizzes, which check whether each
piece landed. Here nobody tells you which technique to reach for. Choosing well,
under a clock, with no answer key, is the closest this course gets to the real
thing.
