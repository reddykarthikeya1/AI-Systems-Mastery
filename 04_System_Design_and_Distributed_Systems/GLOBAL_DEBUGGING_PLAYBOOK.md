# Global Debugging Playbook: Distributed Systems Incident Triage

When a distributed production system goes down, there is no single stack trace. Errors cascade across service boundaries, databases drown in query queues, and network timeouts ripple across tiers.

This playbook is your **operational emergency runbook** for diagnosing and resolving distributed failure modes.

---

## ?? Tier-1 Emergency Incident Triage Workflow

`
[ALERT FIRED: Latency Spiking / Error Rate > 5%]
                 �
                 ?
 1. TRIAGE BLAST RADIUS
    +-- Is it global or regional? (Check Route53 / Cloudflare DNS status)
    +-- Which tier is failing? (Edge Proxy -> API Gateway -> App Server -> Database)
    +-- Identify p50 vs p95 vs p99 latency disparity (Tail Latency Amplification)
                 �
                 ?
 2. MITIGATE IMMEDIATE IMPACT (Stop the Bleeding)
    +-- Shed non-critical load (Turn off recommendations, background analytics)
    +-- Activate Circuit Breakers (Fail fast instead of queuing threads)
    +-- Enable Rate Limiting (Throttle abusive IPs / unauthenticated traffic)
                 �
                 ?
 3. ISOLATE ROOT CAUSE
    +-- Check Red Signals: Rate, Errors, Duration (RED Method)
    +-- Check Utilization, Saturation, Errors (USE Method on CPU/RAM/Disk/IO)
    +-- Trace distributed spans (Find the slowest span in OpenTelemetry/Jaeger)
                 �
                 ?
 4. REMEDIATION & POST-MORTEM
    +-- Rollback recent deploy OR scale downstream capacity
    +-- Drain and restart degraded nodes
    +-- Execute Blameless Post-Mortem (5 Whys Analysis)
`

---

## ?? Common Distributed Failure Modes & Prescribed Cures

### 1. The Cascading Retry Storm (Thundering Herd)
- **Symptom**: Service B experiences a brief 2-second hiccup. Service A's requests time out, so Service A immediately retries all requests. The traffic to Service B doubles (\times$), causing it to collapse completely and never recover.
- **Diagnosis**: Upstream request rate spikes without any increase in external user traffic.
- **The Cure**:
  1. **Exponential Backoff with Full Jitter**:
     \text{sleep} = \text{random}(0, \, \min(M, \, B \cdot 2^{\text{attempt}}))
  2. **Circuit Breaker**: If error rate exceeds 50% over a 10s window, trip the breaker to OPEN state. Fail upstream requests instantly without touching the network.
  3. **Global Retry Budgets**: Cap total retries across the service to $\le 10\%$ of total outgoing requests.

---

### 2. Cache Pathologies (Avalanche, Breakdown, Penetration)

| Pathology | What Actually Happens | How to Diagnose | Production Cure |
| :--- | :--- | :--- | :--- |
| **Cache Avalanche** | Thousands of cached keys have the exact same 1-hour TTL. At minute 60, all keys expire simultaneously. Traffic slams the database directly. | DB CPU spikes from 15% to 100% in a 5-second window at periodic intervals. | **Add Random TTL Jitter**: Set expiration to $\text{base\_ttl} \pm \text{random}(0, 300\text{s})$. |
| **Cache Breakdown** | A single viral "hot key" (e.g. World Cup final score) expires. 100,000 concurrent requests miss the cache and all run the heavy DB query at once. | DB slow query logs dominated by a single identical query for a single ID. | **Single-Flight Mutex**: First request acquires an in-memory lock to query DB; all 99,999 others wait on that promise. |
| **Cache Penetration** | Malicious users query non-existent keys (e.g. user_id = -99999). Cache never finds it, so every request hits the DB. | Cache hit ratio drops to <10%; DB queries for non-existent IDs spike. | **Bloom Filter Guard**: Check Bloom filter first. If absent, reject before querying DB. Alternatively, cache NULL with short TTL (60s). |

---

### 3. Database Connection Pool Starvation & Deadlocks
- **Symptom**: Application endpoints hang indefinitely, timing out after 30 seconds (504 Gateway Timeout).
- **Diagnosis**:
  - Application threads are blocked in waiting for connection from pool.
  - Database active connections equal max_connections, but DB CPU is near 0% (threads are waiting on locks, not computing).
- **The Cure**:
  1. **Enforce Strict Query Timeouts**: Set statement_timeout = 2000 (2s max) to kill runaway queries before they hold pool connections.
  2. **Order Resource Acquisition**: Ensure all concurrent transactions acquire row-level locks in the same alphanumeric order to mathematically prevent circular deadlocks.
  3. **Dedicated Connection Pools**: Separate read-only query pools from write transaction pools.

---

### 4. Tail Latency Amplification ($ Trap)
- **Symptom**: In a microservice architecture where a single user request fans out to 100 backend services, the user-perceived $ latency is terrible even though each individual service has a 99% success/fast rate!
- **The Math**: The probability of at least one slow request among $ parallel sub-requests is:
  P(\text{at least one slow}) = 1 - (0.99)^N
  For  = 100$,  - (0.99)^{100} = 1 - 0.366 = \mathbf{63.4\%}$!
  *Over 63% of your users will experience the $ latency!*
- **The Cure**:
  1. **Hedged Requests**: Send a second duplicate request to another replica if the first request hasn't responded within the $ time threshold. Take whichever responds first.
  2. **Deadlines & Propagation**: Pass a context deadline timestamp (e.g. X-Request-Deadline) across all RPC hops. If the deadline expires, cancel all downstream in-flight work.
