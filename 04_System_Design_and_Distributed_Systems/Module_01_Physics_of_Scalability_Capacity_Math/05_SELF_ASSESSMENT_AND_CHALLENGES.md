# Module 01: The Physics of Scalability & Capacity Math: Self-Assessment, Architectural Questions & Challenges

Evaluate your mastery of **Hardware Latencies, Amdahl's Law, Little's Law, and Capacity Planning** through diagnostic interview questions, architectural trade-off evaluations, and hands-on coding challenges.

---

## Part 1: Diagnostic Architectural & Scalability Questions

### Question 1
Why is a random read from an NVMe SSD (~100 µs) 1,000x slower than reading from main RAM memory (~100 ns)?

### Question 2
Explain Little's Law ($L = \lambda W$) and how a downstream 500ms database stall cascades into API gateway thread pool exhaustion.

### Question 3
Under Amdahl's Law, what is the maximum achievable speedup if 90% of a video processing pipeline is parallelized across 1,000 CPU cores?

### Question 4
Why is the 80/20 Pareto rule applied to daily read volume rather than total 5-year storage when sizing Redis RAM clusters?

### Question 5
Calculate the average and peak write QPS for a chat system with 200M DAU where each user sends 50 messages per day with a 3.0x peak multiplier.

### Question 6: Production Observability
What are the top 3 Golden Signals (Latency, Traffic, Errors, Saturation) you must monitor on Grafana dashboards for this engine?

### Question 7: Architectural Anti-Patterns
Describe a common rookie implementation mistake when deploying this architecture, and explain why it causes catastrophic failure under high load.

### Question 8: Security & Multi-Tenant Isolation
How does this architecture enforce strict tenant isolation, cryptographic integrity, or rate limiting against denial-of-service (DoS) attacks?

### Question 9: Alternative Comparison & Technology Trade-Offs
Compare this approach to an alternative architecture. When would you choose this design over simpler or more traditional approaches, and what complexity cost do you pay?

### Question 10: Evolution & Migration Strategy
How do you upgrade or migrate this component in production with zero downtime, backward-compatible schemas, and immediate rollback capability?

---

## Part 2: Detailed Answer Keys & Production Rationales

### Answers 1-5: Architectural Analysis
1. Mechanical Constraints: Hardware bus speeds, cache line sizes, and network packet roundtrips impose strict physical limits. Designs must prioritize in-memory batching and pipelining over synchronous disk/network hops.
2. Failure Modes: Systems employ heartbeat probes, lease timeouts, and leader election quorums to detect and isolate failures without data loss.
3. Concurrency: Atomic primitives, locks with TTLs, and lock-free data structures eliminate lost updates and starvation.
4. Consistency Models: Trade-offs between linearizable Strong Consistency and High Availability are chosen based on business failure tolerance.
5. Capacity Sizing: Proactive rate-limiting and circuit-breaking protect against cascading exhaustion during unexpected traffic spikes.

### Answers 6-10: SRE & Operational Standards
6. Observability: Monitor p99 latency, error rates, and queue/thread saturation.
7. Anti-Patterns: Never allow unbounded memory queues, missing remote call timeouts, or synchronous cascading dependencies.
8. Security: Enforce principle of least privilege, mutual TLS (mTLS), and cryptographic token verification.
9. Trade-offs: Accept distributed architectural complexity only when vertical scaling limits are fundamentally breached.
10. Migrations: Use canary deployments, feature flags, and expand-contract schema evolution.

---

## Part 3: Practical Design & Coding Challenges

### Challenge 1: Little's Law Gateway Queue Simulator
Write a simulator that monitors gateway thread saturation based on incoming arrival rate and average database response latency.

#### Solution:
```python
def evaluate_gateway_saturation(arrival_rate: int, latency_ms: float, max_threads: int) -> dict:
    latency_sec = latency_ms / 1000.0
    in_flight_tasks = arrival_rate * latency_sec
    is_saturated = in_flight_tasks > max_threads
    thread_utilization_pct = min(100.0, (in_flight_tasks / max_threads) * 100.0)
    return {
        "in_flight_tasks": round(in_flight_tasks),
        "is_saturated": is_saturated,
        "thread_utilization_pct": round(thread_utilization_pct, 1)
    }

res = evaluate_gateway_saturation(arrival_rate=5000, latency_ms=80, max_threads=600)
assert res["in_flight_tasks"] == 400
assert not res["is_saturated"]
assert res["thread_utilization_pct"] == 66.7
print("✅ Challenge 1 Passed!")
```

### Challenge 2: Exponential Backoff with Jitter
Implement a full-jitter exponential backoff calculation to prevent the Thundering Herd problem against downstream services.

#### Solution:
```python
import random

def calculate_backoff(attempt: int, base: float = 0.1, cap: float = 2.0) -> float:
    temp = min(cap, base * (2 ** attempt))
    return random.uniform(0, temp)

delays = [calculate_backoff(i) for i in range(5)]
assert all(0 <= d <= 2.0 for d in delays)
print("✅ Challenge 2 Passed!")
```
