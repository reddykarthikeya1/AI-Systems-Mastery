# Module 00: Self-Assessment, Interview Questions & Practical Challenges

Evaluate your mastery of system design fundamentals, capacity estimation math, and whiteboard interview navigation.

---

## Part 1: Diagnostic Architectural Questions

### Question 1: Pacing & Ambiguity
In a 45-minute technical system design interview, your interviewer asks: *"Design YouTube."* What should be your immediate next action?
- A) Start drawing a multi-region CDN architecture and video transcoding queue.
- B) Clarify functional requirements (e.g., video upload and video viewing) and non-functional bounds (daily active users, resolution, global audience).
- C) Ask which database engine they prefer you use.
- D) Write the SQL schema for user accounts.

### Question 2: Latency Orders of Magnitude
A microservice architecture makes 15 synchronous serial database queries to PostgreSQL over an intra-datacenter network, and 5 external API calls across the public Internet to payment processors. Why will local in-memory CPU optimizations produce virtually zero perceived latency improvement for the end user?

### Question 3: Little's Law in Production
Explain why a 4x latency degradation in downstream database responses causes an immediate 4x surge in open socket connections and thread pool starvation at the API gateway tier, referencing Little's Law ($L = \lambda W$).

### Question 4: Amdahl's Law Constraints
If 95% of an e-commerce checkout request pipeline is parallelizable across 100 worker nodes, but 5% requires a serial lock on a central inventory counter, what is the maximum theoretical speedup possible according to Amdahl's Law?

### Question 5: Capacity Estimation (Storage vs RAM)
Why do high-scale architectures size RAM cache based on the **80/20 Pareto rule applied to daily read volume**, rather than total historical multi-year storage?

### Question 6: API Contract Specification
When defining an API for creating a resource in an interview, why is it vital to specify the `Idempotency-Key` header and status code semantics (e.g. 201 Created vs 200 OK vs 409 Conflict)?

### Question 7: Horizontal vs Vertical Ceilings
What is the primary operational risk of scaling a database vertically (e.g. upgrading to an AWS `u-24tb1.metal` instance with 24 TB RAM and 448 vCPUs) versus horizontally sharding across 10 smaller nodes?

### Question 8: CAP Theorem in Practice
During an optical fiber cut between US-East and EU-West, why is an architect forced to choose between returning an error/stale data (Availability) or blocking user writes until the link is restored (Consistency)?

### Question 9: Premature Microservice Optimization
Why is decomposing an application into 12 microservices on Day 1 considered a major architectural anti-pattern in both startups and interviews?

### Question 10: Single Point of Failure (SPOF) Detection
You have designed a high-throughput video platform with 50 web servers, 10 Redis cache replicas, and a primary-replica PostgreSQL cluster. The load balancer routing traffic to the 50 web servers is hosted on a single virtual machine with an Elastic IP. What is the fatal design flaw?

---

## Part 2: Answer Keys & Architectural Rationales

### Answer 1: B
**Rationale:** Interviewers intentionally give vague prompts like *"Design YouTube"* to evaluate how you handle ambiguity. Jumping straight into architecture without scoping guarantees failure. You must spend the first 5 minutes establishing constraints: upload size, viewing volume, read-to-write ratio, and whether search or live-streaming are in scope.

### Answer 2
**Rationale:** In-memory CPU operations run in nanoseconds ($0.5 - 7\text{ ns}$). An intra-datacenter network hop requires $\sim 500\text{ µs}$ ($500,000\text{ ns}$), and an external Internet roundtrip requires $\sim 100\text{ ms}$ ($100,000,000\text{ ns}$). The network waiting time dominates $99.999\%$ of the request lifecycle. Optimizing CPU execution yields negligible user-facing speedups compared to eliminating serial network hops via batching or caching.

### Answer 3
**Rationale:** By Little's Law ($L = \lambda W$), the number of concurrent in-flight requests ($L$) equals arrival rate ($\lambda$) multiplied by residency time ($W$). If $\lambda = 5,000\text{ req/sec}$ and latency jumps from $50\text{ ms}$ ($0.05\text{s}$) to $200\text{ ms}$ ($0.20\text{s}$), in-flight requests jump from $250$ to $1,000$. If server worker threads are capped at 500, the connection queue overflows, memory spikes, and the gateway drops incoming traffic with HTTP 504 Gateway Timeouts.

### Answer 4
**Rationale:** Amdahl's Law states $S = \frac{1}{(1-p) + \frac{p}{s}}$. With $p = 0.95$ and $1 - p = 0.05$:
$$\lim_{s \to \infty} S = \frac{1}{0.05} = 20\times$$
No matter how many hundreds or thousands of nodes you add, you can **never exceed a 20x overall speedup** because the 5% serial lock fundamentally bottlenecks total throughput.

### Answer 5
**Rationale:** Storing 5 years of historical data (petabytes) in RAM is cost-prohibitive and unnecessary. Because access patterns follow a power law (Pareto distribution), 80% of all user queries access the most recent or popular 20% of data. Sizing RAM to hold 20% of the *daily read volume* ensures an 80%+ cache hit rate at a fraction of hardware costs.

### Answer 6
**Rationale:** Distributed networks are inherently unreliable; timeouts can occur after the server processes the request but before the client receives the response. An `Idempotency-Key` allows clients to safely retry network calls without duplicating purchases or creating double entities.

### Answer 7
**Rationale:** Vertical scaling creates a catastrophic **Single Point of Failure (SPOF)**. If that single massive machine experiences hardware failure, kernel panic, or routine maintenance, 100% of the platform goes offline. Furthermore, costs scale exponentially rather than linearly.

### Answer 8
**Rationale:** Under a network partition, the two datacenters cannot communicate. If a user in US-East writes data, EU-West cannot learn about it. You must either:
1. Accept the write in US-East and allow EU-West to serve stale data (Sacrifice Consistency to maintain Availability - AP).
2. Reject writes or block reads in EU-West until the partition heals (Sacrifice Availability to maintain Consistency - CP).

### Answer 9
**Rationale:** Microservices introduce distributed complexity: network serialization overhead, eventual consistency bugs, distributed tracing requirements, and multi-service deployments. Starting with a well-modularized monolith allows teams to iterate quickly and discover true domain boundaries before paying the distributed systems tax.

### Answer 10
**Rationale:** The single load balancer VM is a Single Point of Failure (SPOF). If that VM crashes or its network card fails, all 50 web servers and caches become unreachable. The fix is active-active DNS round-robin across multiple load balancers, or an anycast IP backed by BGP routing and redundant gateway appliances.

---

## Part 3: Practical Hands-On Design Challenges

### Challenge 1: Video-on-Demand Capacity Sizing
Write a Python script that calculates the infrastructure sizing for a global video streaming platform with:
- 100 Million Daily Active Users (DAU)
- Average user watches 3 videos per day (Average bitrate: 5 Mbps, average duration: 10 minutes)
- 1% of users upload 1 video per day (Average size: 500 MB)
- Compute:
  1. Average Video Egress Bandwidth in Gbps.
  2. Daily Video Storage Ingress in TB.
  3. 1-Year Storage Accumulation in PB.

#### Solution:
```python
def size_video_platform():
    dau = 100_000_000
    
    # 1. Video Egress Bandwidth
    # Total daily watch minutes: 100M * 3 * 10 = 3,000,000,000 minutes = 180,000,000,000 seconds
    # Average concurrent streams = (100M * 3 * 600s) / 86,400s ≈ 2,083,333 streams
    # Bandwidth = 2,083,333 * 5 Mbps ≈ 10,416,666 Mbps ≈ 10.42 Tbps!
    total_streams_day = dau * 3
    stream_duration_sec = 10 * 60
    avg_concurrent_streams = (total_streams_day * stream_duration_sec) / 86400
    bandwidth_gbps = (avg_concurrent_streams * 5) / 1000  # Mbps to Gbps
    
    # 2. Storage Ingress
    daily_uploads = dau * 0.01  # 1% upload
    daily_storage_tb = (daily_uploads * 500) / 1_000_000  # 1M MB = 1 TB
    
    # 3. 1-Year Storage Accumulation
    annual_storage_pb = (daily_storage_tb * 365) / 1000
    
    return {
        "avg_concurrent_streams": round(avg_concurrent_streams),
        "egress_bandwidth_gbps": round(bandwidth_gbps, 2),
        "daily_storage_tb": round(daily_storage_tb, 2),
        "annual_storage_pb": round(annual_storage_pb, 2),
    }

metrics = size_video_platform()
print("Video Platform Metrics:", metrics)
# Expected: ~10,416 Gbps (~10.4 Tbps), 500 TB/day, 182.5 PB/year
assert metrics["daily_storage_tb"] == 500.0
assert metrics["annual_storage_pb"] == 182.5
print("✅ Challenge 1 Passed!")
```

### Challenge 2: Amdahl's Law Speedup Optimizer
Implement an automated Amdahl's Law evaluator that takes a target speedup $S_{\text{target}}$ and parallel fraction $p$, and determines the minimum number of worker nodes $s$ required to achieve that speedup, or raises an error if the target exceeds the physical ceiling $\frac{1}{1-p}$.

#### Solution:
```python
def find_minimum_nodes(parallel_fraction: float, target_speedup: float) -> int:
    if not (0.0 < parallel_fraction < 1.0):
        raise ValueError("Parallel fraction must be between 0.0 and 1.0 exclusive.")
    
    max_speedup = 1.0 / (1.0 - parallel_fraction)
    if target_speedup >= max_speedup:
        raise ValueError(
            f"Target speedup {target_speedup}x is impossible. "
            f"Physical ceiling for p={parallel_fraction*100:.1f}% is {max_speedup:.2f}x."
        )
    
    # Derivation:
    # 1 / ((1 - p) + p / s) = S
    # (1 - p) + p / s = 1 / S
    # p / s = (1 / S) - (1 - p)
    # s = p / ((1 / S) - (1 - p))
    denominator = (1.0 / target_speedup) - (1.0 - parallel_fraction)
    nodes = parallel_fraction / denominator
    import math
    return math.ceil(nodes)

# If 90% is parallel, ceiling is 10x. To get 8x speedup:
nodes_needed = find_minimum_nodes(0.90, 8.0)
print(f"Nodes required for 8x speedup: {nodes_needed}")
assert nodes_needed == 36

# Assert exceeding ceiling raises ValueError
try:
    find_minimum_nodes(0.90, 10.5)
    assert False, "Should have raised ValueError"
except ValueError as e:
    print(f"Correctly caught impossible speedup: {e}")

print("✅ Challenge 2 Passed!")
```
